import {useEffect,useRef,useState} from 'react';
import {request,apiFetch,streamAnswer,extractFile,type Session,type Turn} from '../lib/api';
import {Panel,Empty,ErrorText} from '../components/Ui';
import {LiveAudioControls} from './LiveAudioControls';
const MODES=['short','hint','detailed','code','diagram','verify','follow-up'] as const;
export function Live({sessions,refresh,seed,initialSid}:{sessions:Session[];refresh:()=>void;seed?:string;initialSid?:string}){
 const [sid,setSid]=useState(initialSid||''),[question,setQuestion]=useState(seed||''),[mode,setMode]=useState<string>('short'),[provider,setProvider]=useState('ollama'),[model,setModel]=useState(''),[answer,setAnswer]=useState(''),[turns,setTurns]=useState<Turn[]>([]),[busy,setBusy]=useState(false),[error,setError]=useState(''),[meta,setMeta]=useState(''),[audioBusy,setAudioBusy]=useState(false);
 const abort=useRef<AbortController|null>(null),recorder=useRef<MediaRecorder|null>(null),micStream=useRef<MediaStream|null>(null);
 useEffect(()=>{if(seed)setQuestion(seed)},[seed]);
 useEffect(()=>{if(sid)request<Turn[]>(`/api/sessions/${sid}/turns`).then(setTurns).catch(e=>setError(String(e)))},[sid]);
 useEffect(()=>()=>{abort.current?.abort();recorder.current?.stop();micStream.current?.getTracks().forEach(t=>t.stop())},[]);
 const newSession=async()=>{try{const s=await request<Session>('/api/sessions','POST',{title:'Interview practice'});setSid(s.id);setTurns([]);setAnswer('');refresh()}catch(e){setError(String(e))}};
 const ask=async()=>{
 if(!question.trim())return;
 let session=sid;
 try{
 if(!session){const s=await request<Session>('/api/sessions','POST',{title:question.slice(0,58)});session=s.id;setSid(session);refresh()}
 setBusy(true);setAnswer('');setError('');setMeta('Starting…');const controller=new AbortController();abort.current=controller;
 for await(const chunk of streamAnswer({session_id:session,question:question.trim(),mode,provider,model:model.trim()||undefined},controller.signal)){
 if(chunk.type==='token')setAnswer(a=>a+(chunk.text||''));
 else if(chunk.type==='meta')setMeta(`${chunk.category} · ${chunk.model} · verification not performed`);
 else if(chunk.type==='error')setError(chunk.message||'Provider failed');
 else if(chunk.type==='done'){setMeta(`Completed in ${chunk.elapsed_ms} ms · not independently verified`);request<Turn[]>(`/api/sessions/${session}/turns`).then(setTurns);refresh()}
 }
 }catch(e){if((e as Error).name!=='AbortError')setError(String(e))}finally{setBusy(false);abort.current=null}
 };
 const record=async()=>{
 if(recorder.current){recorder.current.stop();setAudioBusy(false);return}
 try{
 const stream=await navigator.mediaDevices.getUserMedia({audio:true});micStream.current=stream;
 const chunks:BlobPart[]=[];
 const rec=new MediaRecorder(stream);recorder.current=rec;
 rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
 rec.onstop=async()=>{
 recorder.current=null;stream.getTracks().forEach(t=>t.stop());setAudioBusy(false);
 try{const blob=new Blob(chunks,{type:rec.mimeType});const form=new FormData();form.append('file',blob,'practice.webm');const r=await apiFetch('/api/transcribe',{method:'POST',body:form});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Audio transcription failed');setQuestion(q=>q ? q+' '+d.text : d.text);setMeta(`Transcribed (${d.language}). Please verify text before asking.`)}catch(e){setError(String(e))}
 };
 rec.start();setAudioBusy(true);setMeta('Recording microphone locally; stop to transcribe.');
 }catch(e){setError('Microphone permission/device error: '+String(e))}
 };
 const file=async(e:React.ChangeEvent<HTMLInputElement>)=>{const f=e.target.files?.[0];if(!f)return;try{setError('');const x=await extractFile(f);setQuestion(q=>q? q+'\n'+x.text:x.text);setMeta(x.extraction+' · Please verify extracted text.')}catch(x){setError(String(x))}e.target.value=''};
 return <div className="page"><div className="page-top"><div><div className="eyebrow">PRACTICE WORKSPACE</div><h1>Live interview coach</h1><p>Ask, explore, and build confidence with context-aware practice.</p></div><button className="btn secondary" onClick={newSession}>＋ New session</button></div>
 <div className="two-col"><div className="stack"><Panel title="Question input" extra={<span className="tiny">Consent-based inputs only</span>}>
 <select aria-label="Session" value={sid} onChange={e=>setSid(e.target.value)}><option value="">New session</option>{sessions.map(s=><option key={s.id} value={s.id}>{s.title}</option>)}</select>
 <textarea className="question-input" value={question} onChange={e=>setQuestion(e.target.value)} placeholder="e.g. Explain the trade-offs between SQL and NoSQL for a high-traffic service…" rows={8}/>
 <div className="row between wrap"><div className="row wrap"><label className="file-btn">↑ Upload screenshot / document<input type="file" accept="image/*,.pdf,.docx,.txt,.py,.ts,.js,.md" onChange={file}/></label><button className={'btn secondary '+(audioBusy?'recording':'')} onClick={record}>{audioBusy?'■ Stop microphone':'◉ Record question'}</button></div><span className="tiny">Audio is not stored</span></div>
 <div className="form-grid"><div><label>Answer depth</label><select value={mode} onChange={e=>setMode(e.target.value)}>{MODES.map(x=><option key={x} value={x}>{x}</option>)}</select></div><div><label>AI provider</label><select value={provider} onChange={e=>setProvider(e.target.value)}><option value="ollama">Local · Ollama</option><option value="cloud">Cloud · opt-in</option></select></div></div>
 <input aria-label="Model name override" value={model} onChange={e=>setModel(e.target.value)} placeholder="Optional model name override"/>
 <div className="row"><button className="btn primary grow" disabled={busy||!question.trim()} onClick={ask}>{busy?'Generating…':'✦ Generate practice answer'}</button><button className="btn secondary" disabled={!busy} onClick={()=>abort.current?.abort()}>Cancel</button></div><ErrorText message={error}/>
 </Panel><Panel title="Continuous audio transcription · optional"><LiveAudioControls onTranscript={text=>setQuestion(q=>q? q+' '+text:text)}/></Panel></div><div className="stack"><Panel title="AI response" extra={<span className={'status '+(busy?'active':'')}>{busy?'Streaming':'Practice mode'}</span>}>
 {answer?<><div className="answer" aria-live="polite">{answer}</div><div className="soft-line">{meta}</div></>:<Empty title="Your answer will appear here" detail="Select a provider, write a question and generate an answer. You can change depth or follow up in the same session."/>}
 </Panel><Panel title="Session context" extra={<span className="tiny">{turns.length} saved answers</span>}>
 {turns.length ? <div className="history-list">{turns.slice().reverse().slice(0,8).map(t=><div className="history-item" key={t.id}><strong>{t.question}</strong><span>{t.mode} · {t.elapsed_ms} ms</span><button className="linklike" onClick={()=>{setQuestion(t.question);setAnswer(t.answer)}}>View answer</button></div>)}</div>:<p className="muted">Answers from this session will appear here and inform follow-up questions.</p>}
 </Panel></div></div></div>
}
