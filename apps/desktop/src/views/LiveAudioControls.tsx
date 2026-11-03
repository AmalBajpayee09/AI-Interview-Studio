import {useEffect,useRef,useState} from 'react';
import {request,apiFetch} from '../lib/api';
import {ErrorText} from '../components/Ui';
interface Device {id:string;name:string;source_type:string}
interface Event {id:number;kind:string;at:number;source_id?:string;text?:string;speaker?:string;start_at?:number;end_at?:number;language?:string;latency_ms?:number;error?:string}
export function LiveAudioControls({onTranscript,sessionId}:{onTranscript:(text:string)=>void;sessionId?:string}){
 const [devices,setDevices]=useState<Device[]>([]),[sourceOne,setSourceOne]=useState(''),[sourceTwo,setSourceTwo]=useState(''),
 [language,setLanguage]=useState('auto'),[running,setRunning]=useState(false),[paused,setPaused]=useState(false),[events,setEvents]=useState<Event[]>([]),
 [problem,setProblem]=useState(''),[info,setInfo]=useState(''),[autoAppend,setAutoAppend]=useState(false);
 const [saveToSession,setSaveToSession]=useState(false);
 const [wavResult,setWavResult]=useState<{duration_seconds:number;channels:number;sample_rate:number;segments:{start_seconds:number;end_seconds:number;speaker:string}[];note:string}|null>(null);
 const cursor=useRef(0), autoRef=useRef(autoAppend), saveRef=useRef(saveToSession), sessionRef=useRef(sessionId);
 useEffect(()=>{autoRef.current=autoAppend},[autoAppend]);
 useEffect(()=>{saveRef.current=saveToSession;sessionRef.current=sessionId},[saveToSession,sessionId]);
 const refresh=async()=>{
   try {
     const d=await request<{available:boolean;devices:Device[];reason?:string}>('/api/audio/devices');
     setDevices(d.devices);setInfo(d.reason||`${d.devices.length} recording source(s) available`);
     const status=await request<{status:string}>('/api/audio/status');setRunning(status.status==='running');
   }catch(e){setProblem(String(e))}
 };
 useEffect(()=>{refresh();
   const poll=setInterval(async()=>{
     try{
       const r=await request<{events:Event[]}>(`/api/audio/events?since=${cursor.current}`);
       for (const e of r.events){
         cursor.current=Math.max(cursor.current,e.id);
         if(e.kind==='transcript_final'&&e.text){
           if(autoRef.current)onTranscript(e.text);
           if(saveRef.current&&sessionRef.current)request(`/api/sessions/${sessionRef.current}/transcripts`,'POST',{text:e.text,source_id:e.source_id||'unknown',speaker:'unknown',language:e.language||null,started_at:e.start_at||null,ended_at:e.end_at||null}).catch(err=>setProblem('Transcript save failed: '+String(err)));
         }
         if(e.kind==='audio_error'||e.kind==='stt_error'){setProblem(e.error||'Audio capture failed');setRunning(false)}
       }
       if(r.events.length)setEvents(prev=>[...prev,...r.events].slice(-20));
     }catch{/* The offline banner and retry controls provide the connection state. */}
   },900);
   return ()=>clearInterval(poll);
 },[]);
 const inspectWav=async(file:File|undefined)=>{
   if(!file)return;setProblem('');setWavResult(null);
   try{
     const body=new FormData();body.append('file',file);
     const response=await apiFetch('/api/audio/analyze-wav',{method:'POST',body});
     if(!response.ok){const error=await response.json();throw new Error(error.detail||'WAV inspection failed')}
     setWavResult(await response.json());
   }catch(e){setProblem(String(e))}
 };
 const start=async()=>{
   setProblem('');
   try{const selected=[sourceOne,sourceTwo].filter(Boolean);
     await request('/api/audio/start','POST',{source_ids:selected,language});setRunning(true)
   }catch(e){setProblem(String(e))}
 };
 const togglePause=async()=>{try{await request(paused?'/api/audio/resume':'/api/audio/pause','POST',{});setPaused(!paused)}catch(e){setProblem(String(e))}};
 const stop=async()=>{try{await request('/api/audio/stop','POST',{});setRunning(false);setPaused(false)}catch(e){setProblem(String(e))}};
 return <div className="stack" style={{gap:12}}>
   <div className="notice">Live recording is opt-in. Captured audio is processed locally; source IDs are not proof of speaker identity. Transcripts may contain errors.</div>
   <div className="form-grid"><div><label>Input 1</label><select aria-label="Primary audio source" disabled={running} value={sourceOne} onChange={e=>setSourceOne(e.target.value)}><option value="">Select source</option>{devices.map(d=><option key={d.id} value={d.id}>{d.source_type}: {d.name}</option>)}</select></div><div><label>Input 2 (optional)</label><select aria-label="Secondary audio source" disabled={running} value={sourceTwo} onChange={e=>setSourceTwo(e.target.value)}><option value="">None</option>{devices.filter(d=>d.id!==sourceOne).map(d=><option key={d.id} value={d.id}>{d.source_type}: {d.name}</option>)}</select></div></div>
   <div className="row wrap"><select aria-label="Transcription language" disabled={running} value={language} onChange={e=>setLanguage(e.target.value)}><option value="auto">Auto language</option><option value="en">English</option><option value="hi">Hindi</option></select><button className="btn secondary" disabled={running} onClick={refresh}>Refresh devices</button><button className={"btn "+(running?'danger':'primary')} onClick={running?stop:start} disabled={!running&&!sourceOne}>{running?'■ Stop live transcription':'◉ Start live transcription'}</button>{running&&<button className="btn secondary" onClick={togglePause}>{paused?'▶ Resume capture':'Ⅱ Pause capture'}</button>}</div>
   <div className="notice"><b>Recorded WAV check (offline)</b> · Select a mono/stereo 16-bit PCM WAV to inspect channel settings and sound-activity timestamps. This does not transcribe or identify speakers.
     <input type="file" accept=".wav,audio/wav" aria-label="Inspect recorded WAV" onChange={e=>inspectWav(e.currentTarget.files?.[0])}/>
     {wavResult&&<div className="tiny" role="status">{wavResult.duration_seconds}s · {wavResult.channels} channel(s) · {wavResult.sample_rate}Hz · {wavResult.segments.length} sound segment(s): {wavResult.segments.map(s=>s.start_seconds+'–'+s.end_seconds+'s').join(', ')||'none'} · Speaker unknown</div>}
   </div>
   <label className="row" style={{gap:8}}><input type="checkbox" checked={autoAppend} onChange={e=>setAutoAppend(e.target.checked)}/> Auto-append finalized transcript to question (never auto-send to cloud)</label>
   <label className="row" style={{gap:8}}><input type="checkbox" disabled={!sessionId} checked={saveToSession&&!!sessionId} onChange={e=>setSaveToSession(e.target.checked)}/> Save finalized transcript text to this session (opt-in; no raw audio){!sessionId?' · create/select session first':''}</label>
   <div className="tiny">{running?(paused?'Recording paused':'Recording active'):'Not recording'} · {info}</div>
   <ErrorText message={problem}/>
   <div style={{maxHeight:170,overflowY:'auto'}}>{events.filter(e=>e.kind==='transcript_final').slice(-5).reverse().map(e=><div className="list-row" key={e.id}><div><small>{e.source_id} · speaker unknown · {e.latency_ms}ms STT</small><p>{e.text}</p></div><button className="btn small secondary" onClick={()=>e.text&&onTranscript(e.text)}>Use text</button></div>)}</div>
 </div>
}
