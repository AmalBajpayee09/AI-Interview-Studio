import {useEffect,useRef,useState} from 'react';
import {invoke,isTauri} from '@tauri-apps/api/core';
import {request,streamAnswer,type Session,type Turn} from './lib/api';
import './overlay.css';

type Layout='compact'|'teleprompter'|'split'|'feed';
type AnswerMode='short'|'hint'|'detailed'|'code'|'verify';
type HotkeyStatus={hotkey:string;hotkey_registered:boolean;tray_installed:boolean;visible:boolean};
const MODES:AnswerMode[]=['short','hint','detailed','code','verify'];
const LAYOUTS:{id:Layout;label:string}[]=[
 {id:'compact',label:'Compact'}, {id:'teleprompter',label:'Teleprompter'},
 {id:'split',label:'Split desk'}, {id:'feed',label:'Q&A feed'},
];
const HOTKEYS=['Ctrl+Alt+Shift+O','Ctrl+Alt+Shift+P','Ctrl+Alt+Shift+I'];

export default function Overlay(){
 const [layout,setLayout]=useState<Layout>('compact');
 const [sessions,setSessions]=useState<Session[]>([]);
 const [sid,setSid]=useState(localStorage.getItem('overlay-last-session')||'');
 const [turns,setTurns]=useState<Turn[]>([]);
 const [question,setQuestion]=useState('');
 const [answer,setAnswer]=useState('');
 const [mode,setMode]=useState<AnswerMode>('short');
 const [provider,setProvider]=useState('ollama');
 const [model,setModel]=useState('');
 const [models,setModels]=useState<string[]>([]);
 const [busy,setBusy]=useState(false);
 const [online,setOnline]=useState(false);
 const [error,setError]=useState('');
 const [status,setStatus]=useState('Connecting to local worker…');
 const [fontSize,setFontSize]=useState(20);
 const [lineHeight,setLineHeight]=useState(1.6);
 const [historySearch,setHistorySearch]=useState('');
 const [selectedIndex,setSelectedIndex]=useState(-1);
 const [hotkey,setHotkey]=useState('Ctrl+Alt+Shift+O');
 const [hotkeyRegistered,setHotkeyRegistered]=useState(false);
 const abort=useRef<AbortController|null>(null);
 const input=useRef<HTMLTextAreaElement>(null);
 const currentAnswer=answer||turns[turns.length-1]?.answer||'';
 const currentQuestion=question||turns[turns.length-1]?.question||'';
 const currentTurn=selectedIndex<0?undefined:turns[selectedIndex];

 const loadSessions=async()=>{
  try{
   const list=await request<Session[]>('/api/sessions');
   setSessions(list);
   if(sid&&!list.some(s=>s.id===sid)){setSid('');localStorage.removeItem('overlay-last-session');}
   return list;
  }catch{return [] as Session[]}
 };
 const loadTurns=async(id:string)=>{
  if(!id){setTurns([]);return}
  try{setTurns(await request<Turn[]>(`/api/sessions/${id}/turns`));}
  catch(e){setError('Could not restore session: '+String(e))}
 };
 useEffect(()=>{
  let active=true;
  const poll=async()=>{
   try{
    await request('/api/health');
    if(active){setOnline(true);setStatus('Local AI worker connected')}
   }catch{if(active){setOnline(false);setStatus('Worker offline · use workspace diagnostics')}}
  };
  void poll();
  const timer=setInterval(poll,5000);
  void loadSessions();
  if(sid)void loadTurns(sid);
  if(isTauri())void invoke<HotkeyStatus>('overlay_window_status')
   .then(s=>{if(active){setHotkey(s.hotkey);setHotkeyRegistered(s.hotkey_registered)}})
   .catch(()=>{});
  void request<{models?:Array<string|{name:string}>}>('/api/models')
   .then(r=>{if(active){setModels((r.models||[]).map(m=>typeof m==='string'?m:m.name).filter(Boolean))}})
   .catch(()=>{});
  return()=>{active=false;clearInterval(timer);abort.current?.abort()};
 // The initial session is intentionally read once; subsequent changes use selectSession.
 // eslint-disable-next-line react-hooks/exhaustive-deps
 },[]);
 const selectSession=(id:string)=>{
  setSid(id);setAnswer('');setQuestion('');setSelectedIndex(-1);
  if(id)localStorage.setItem('overlay-last-session',id);
  else localStorage.removeItem('overlay-last-session');
  void loadTurns(id);
 };
 const newSession=async()=>{
  try{
   const s=await request<Session>('/api/sessions','POST',{title:'Overlay interview practice'});
   selectSession(s.id);await loadSessions();setStatus('New session created');
  }catch(e){setError('Session could not be created: '+String(e))}
 };
 const ask=async()=>{
  if(!question.trim()||busy)return;
  let id=sid;
  try{
   if(!id){
    const session=await request<Session>('/api/sessions','POST',{title:question.slice(0,55)});
    id=session.id;setSid(id);localStorage.setItem('overlay-last-session',id);
    void loadSessions();
   }
   setBusy(true);setAnswer('');setError('');setStatus('Preparing streamed response…');
   const controller=new AbortController();abort.current=controller;
   for await(const event of streamAnswer({
     session_id:id,question:question.trim(),mode,provider,model:model||undefined
   },controller.signal)){
    if(event.type==='token')setAnswer(v=>v+(event.text||''));
    else if(event.type==='meta')setStatus('Streaming · '+(event.model||'local provider'));
    else if(event.type==='error')setError(event.message||'Model stream interrupted');
    else if(event.type==='done'){
     setStatus(`Answer ready · first token ${event.first_token_ms??'?'} ms`);
     void loadTurns(id);void loadSessions();
     setSelectedIndex(-1);
    }
   }
  }catch(e){if((e as Error).name!=='AbortError')setError(String(e))}
  finally{setBusy(false);abort.current=null}
 };
 const cancel=async()=>{
  if(!busy)return;
  try{if(sid)await request(`/api/ask/${sid}/cancel`,'POST',{});}
  catch(e){setError('Cancellation request failed: '+String(e))}
  abort.current?.abort();
  setStatus('Generation cancelled; incomplete answer is not saved');
 };
 const workspace=async()=>{if(isTauri())try{await invoke('open_workspace')}catch(e){setError(String(e))}else{window.location.href='?workspace=1'}};
 const hide=async()=>{if(isTauri())await invoke('hide_overlay_window');else setStatus('Hide is available in the installed desktop app')};
 const exit=async()=>{if(window.confirm('Exit AI Interview Studio and stop its worker?')&&isTauri())await invoke('exit_from_overlay')};
 const updateHotkey=async(next:string)=>{
  try{await invoke('set_overlay_hotkey',{hotkey:next});setHotkey(next);setHotkeyRegistered(true);setError('')}
  catch(e){setError('Shortcut not registered: '+String(e))}
 };
 const selectLayout=(id:Layout)=>{setLayout(id);setSelectedIndex(-1)};
 const filtered=turns.filter(t=>(t.question+' '+t.answer).toLowerCase().includes(historySearch.toLowerCase()));
 const activeAnswer=currentTurn?.answer||currentAnswer;
 const activeQuestion=currentTurn?.question||currentQuestion;
 return <div className="overlay-shell">
  <header className="overlay-header">
   <div className="overlay-brand"><span className="overlay-mark">✳</span><div><strong>Interview Studio</strong><small>Floating practice assistant</small></div></div>
   <div className="overlay-toolbar">
    <button aria-label="Open workspace and settings" title="Workspace & settings" onClick={workspace}>⚙</button>
    <button aria-label="Hide overlay" title="Hide to tray" onClick={hide}>−</button>
   </div>
  </header>
  <div className="overlay-status" role="status">
   <span className={'overlay-dot '+(online?'ok':'')}/>{status}
  </div>
  <nav className="overlay-layouts" aria-label="Overlay layouts">
   {LAYOUTS.map(x=><button key={x.id} className={layout===x.id?'selected':''} onClick={()=>selectLayout(x.id)} aria-pressed={layout===x.id}>{x.label}</button>)}
  </nav>
  <div className="overlay-session">
   <label htmlFor="overlay-session-select">Session</label>
   <select id="overlay-session-select" value={sid} onChange={e=>selectSession(e.target.value)}>
    <option value="">New / unsaved session</option>
    {sessions.map(s=><option key={s.id} value={s.id}>{s.title}</option>)}
   </select>
   <button onClick={newSession} title="New session" aria-label="New session">＋</button>
  </div>
  {(layout==='compact'||layout==='split')&&<section className="overlay-question">
   <label htmlFor="overlay-question-input">Question / latest transcript</label>
   <textarea ref={input} id="overlay-question-input" value={question} onChange={e=>setQuestion(e.target.value)}
    placeholder="Type a practice question or paste verified transcript text…" rows={layout==='compact'?3:4}/>
  </section>}
  <div className="overlay-settings">
   <select aria-label="Answer mode" value={mode} onChange={e=>setMode(e.target.value as AnswerMode)}>
    {MODES.map(x=><option key={x} value={x}>{x} answer</option>)}
   </select>
   <select aria-label="AI provider" value={provider} onChange={e=>setProvider(e.target.value)}>
    <option value="ollama">Local Ollama</option><option value="cloud">Cloud (consent required)</option>
   </select>
   {models.length>0&&provider==='ollama'&&<select aria-label="Local model" value={model} onChange={e=>setModel(e.target.value)}>
    <option value="">Default model</option>{models.map(m=><option key={m} value={m}>{m}</option>)}
   </select>}
  </div>
  <div className="overlay-actions">
   <button className="overlay-primary" disabled={busy||!online||!question.trim()} onClick={ask}>{busy?'Streaming…':'✦ Ask AI'}</button>
   <button disabled={!busy} onClick={cancel}>Cancel</button>
  </div>
  {error&&<div className="overlay-error" role="alert">{error}</div>}
  <main className={'overlay-body overlay-'+layout}>
   {layout==='teleprompter'?<>
    <div className="overlay-body-title">Teleprompter · speaking cues</div>
    <p className="overlay-muted">{activeQuestion||'Ask a question to start.'}</p>
    <div className="overlay-font-controls"><button onClick={()=>setFontSize(v=>Math.max(15,v-2))}>A−</button><button onClick={()=>setFontSize(v=>Math.min(34,v+2))}>A+</button><label>Spacing <input aria-label="Line spacing" type="range" min="1.2" max="2.2" step="0.1" value={lineHeight} onChange={e=>setLineHeight(Number(e.target.value))}/></label></div>
    <div className="overlay-answer overlay-teleprompter-text" style={{fontSize,lineHeight}}>{activeAnswer||'Answer will stream here. Use it as speaking points and verify before repeating.'}</div>
    <div className="overlay-feed-nav"><button disabled={turns.length===0} onClick={()=>setSelectedIndex(i=>i<0?Math.max(0,turns.length-2):Math.max(0,i-1))}>Previous</button><button disabled={turns.length===0} onClick={()=>setSelectedIndex(i=>i<0?-1:i>=turns.length-1?-1:i+1)}>Next</button></div>
   </>:layout==='split'?<div className="overlay-columns">
    <div><strong>Question and context</strong><div className="overlay-answer">{activeQuestion||'No question yet'}</div><small>{turns.length} saved answers in this session</small></div>
    <div><strong>Suggested response</strong><div className="overlay-answer" aria-live="polite">{activeAnswer||'Waiting for a question'}</div></div>
   </div>:layout==='feed'?<>
    <div className="overlay-body-title">Chronological Q&A feed</div>
    <input aria-label="Search question and answer history" placeholder="Search session answers…" value={historySearch} onChange={e=>setHistorySearch(e.target.value)}/>
    {filtered.length?filtered.map((t,i)=><article className="overlay-feed-card" key={t.id}>
     <small>Turn {i+1} · {t.mode}</small><strong>{t.question}</strong><p>{t.answer}</p><button onClick={()=>{setQuestion(t.question);setAnswer(t.answer);setLayout('compact')}}>Open this answer</button>
    </article>):<p className="overlay-muted">No saved turns match your search.</p>}
   </>:<>
    <div className="overlay-body-title">Suggested answer</div>
    <div className="overlay-answer" aria-live="polite">{activeAnswer||'Your local AI response will appear here when you ask a question.'}</div>
    <p className="overlay-muted">{turns.length} saved turn(s) · Keep follow-ups in the same session.</p>
   </>}
  </main>
  <footer className="overlay-footer">
   <span>Practice only · No recording unless enabled in workspace</span>
   <div><select aria-label="Global overlay shortcut" value={hotkey} onChange={e=>void updateHotkey(e.target.value)} title="Global shortcut">
    {HOTKEYS.map(x=><option key={x} value={x}>{x}</option>)}
   </select><span title={hotkeyRegistered?'Global shortcut registered':'Global shortcut unavailable'}>{hotkeyRegistered?'⌨ ✓':'⌨ !'}</span>
   <button onClick={exit} title="Exit application and stop worker">Exit</button></div>
  </footer>
 </div>
}
