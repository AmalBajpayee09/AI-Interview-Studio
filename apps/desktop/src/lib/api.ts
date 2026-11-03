import {invoke,isTauri} from '@tauri-apps/api/core';
export interface Turn {id:string;session_id:string;question:string;answer:string;mode:string;provider:string;created:number;elapsed_ms:number}
export interface Session {id:string;title:string;created:number;updated:number}
export interface Option {label:string;text:string}
export type QuizAnswer=string|string[];
export interface Question {id:string;stem:string;options?:Option[];kind?:'single'|'multiple'|'numerical';section?:string;points?:number;tolerance?:number}
export interface Assessment {id:string;title:string;questions:Question[];duration_seconds:number;require_start?:number|boolean;negative_marking?:number;cutoff_pct?:number|null}
export interface Stats {sessions:number;questions:number;average_answer_ms:number;assessments_completed:number;average_score_pct:number|null}
interface WorkerConnection {base:string;token:string}
let conn:Promise<WorkerConnection>|undefined;
async function connection():Promise<WorkerConnection>{
  if(!conn){conn=(isTauri()?invoke<WorkerConnection>('worker_connection'):Promise.resolve({base:'http://127.0.0.1:8765',token:''})).catch(e=>{conn=undefined;throw e})}
  return await conn;
}
export async function apiFetch(path:string, options:RequestInit={}):Promise<Response>{
 const auth=await connection();
 const headers=new Headers(options.headers);
 if(auth.token)headers.set('X-Studio-Token',auth.token);
 return fetch(auth.base+path,{...options,headers});
}
export async function request<T>(path:string,method='GET',payload?:unknown):Promise<T>{
 const r=await apiFetch(path,{method,headers:{'Content-Type':'application/json'},body:payload===undefined?undefined:JSON.stringify(payload)});
 if(!r.ok){let msg=`HTTP ${r.status}`;try{const data=await r.json();msg=data.detail||msg}catch{}throw new Error(msg)}
 return r.json() as Promise<T>;
}
export async function extractFile(file:File):Promise<{filename:string;text:string;extraction:string;truncated:boolean}>{
 const form=new FormData();form.append('file',file);
 const r=await apiFetch('/api/files/extract',{method:'POST',body:form});
 if(!r.ok){const e=await r.json();throw new Error(e.detail||'Extraction failed')}
 return r.json();
}
export async function* streamAnswer(body:object,signal:AbortSignal):AsyncGenerator<{type:string;text?:string;message?:string;elapsed_ms?:number;first_token_ms?:number;category?:string;model?:string}>{
 const r=await apiFetch('/api/ask/stream',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),signal});
 if(!r.ok)throw new Error((await r.json()).detail||`HTTP ${r.status}`);
 if(!r.body)throw new Error('Streaming unsupported by this runtime');
 const reader=r.body.getReader(),decoder=new TextDecoder();let buffer='';
 try{
 while(true){const {done,value}=await reader.read();if(done)break;buffer+=decoder.decode(value,{stream:true});
 let pos;while((pos=buffer.indexOf('\n\n'))>=0){const piece=buffer.slice(0,pos);buffer=buffer.slice(pos+2);if(piece.startsWith('data: '))yield JSON.parse(piece.slice(6))}}
 }finally{reader.releaseLock()}
}
export const fmtTime=(n:number)=>new Date(n*1000).toLocaleString();
