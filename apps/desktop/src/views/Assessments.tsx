import {useEffect,useRef,useState} from 'react';
import {request,type Assessment,type QuizAnswer} from '../lib/api';
import {Panel,Empty,ErrorText} from '../components/Ui';
export function Assessments(){
 const [items,setItems]=useState<Assessment[]>([]),[current,setCurrent]=useState<Assessment|null>(null),[answers,setAnswers]=useState<Record<string,QuizAnswer>>({}),[index,setIndex]=useState(0),[remaining,setRemaining]=useState(0),[started,setStarted]=useState(0),[result,setResult]=useState<any>(null),[error,setError]=useState(''),[review,setReview]=useState<string[]>([]),[saveMessage,setSaveMessage]=useState(''),[create,setCreate]=useState(false),[json,setJson]=useState(''),[title,setTitle]=useState('Custom quiz'),[minutes,setMinutes]=useState(5),[penalty,setPenalty]=useState(.25),[cutoff,setCutoff]=useState('');
 const deadline=useRef(0),submitting=useRef(false),autoSubmitted=useRef(false),saveChain=useRef<Promise<void>>(Promise.resolve());
 const refresh=()=>request<Assessment[]>('/api/assessments').then(setItems).catch(e=>setError(String(e)));
 useEffect(()=>{refresh()},[]);
 useEffect(()=>{if(!current||result)return;const id=window.setInterval(()=>{const s=Math.max(0,Math.ceil((deadline.current-Date.now())/1000));setRemaining(s);if(!s&&!submitting.current){finish(true)}},500);return()=>clearInterval(id)},[current,result,answers,started]);
 const start=async(a:Assessment)=>{
  setError('');setSaveMessage('Loading saved progress…');
  try{
   const x=await request<{draft:{answers:Record<string,QuizAnswer>;review:string[];started:number;recovered:boolean}|null}>(`/api/assessments/${a.id}/start`,'POST');
   const at=x.draft?.started??Date.now()/1000;
   setCurrent(a);setIndex(0);setAnswers(x.draft?.answers??{});setResult(null);setReview(x.draft?.review??[]);
   submitting.current=false;autoSubmitted.current=false;saveChain.current=Promise.resolve();setStarted(at);deadline.current=at*1000+a.duration_seconds*1000;
   setRemaining(Math.max(0,Math.ceil((deadline.current-Date.now())/1000)));
   setSaveMessage(x.draft?.recovered?'Restored locally saved answers':'New assessment started');
  }catch(e){setError(String(e));setSaveMessage('')}
 };
 useEffect(()=>{
  if(!current||result||!started||submitting.current)return;
  // Serialize draft saves so a slow older response cannot overwrite newer answers.
  const timer=setTimeout(()=>{
   saveChain.current=saveChain.current.catch(()=>{}).then(async()=>{
    await request(`/api/assessments/${current.id}/draft`,'POST',{answers,review,started});
    setSaveMessage('Answers saved locally');
   }).catch(e=>{setSaveMessage('Autosave error: '+String(e));});
  },350);
  return ()=>clearTimeout(timer);
 },[current,answers,review,started,result]);
 const finish=async(auto=false)=>{
  if(!current||submitting.current||(auto&&autoSubmitted.current))return;
  if(!auto&&!window.confirm('Submit your assessment now?'))return;
  if(auto)autoSubmitted.current=true;
  submitting.current=true;setError('');
  try{
   await saveChain.current;
   // Persist latest answers before an on-time manual submission.
   // At expiry the server grades only previously saved answers.
   if(!auto&&Date.now()<deadline.current){
    await request(`/api/assessments/${current.id}/draft`,'POST',{answers,review,started});
   }
   setResult(await request(`/api/assessments/${current.id}/submit`,'POST',{answers,started}));
  }catch(e){
   setError('Submission failed. Saved answers remain available for retry: '+String(e));
   submitting.current=false;
  }
 };
 const make=async()=>{try{const q=JSON.parse(json);await request('/api/assessments','POST',{title,duration_seconds:Math.round(minutes*60),questions:q,require_start:true,negative_marking:penalty,cutoff_pct:cutoff===''?null:Number(cutoff)});setCreate(false);setJson('');refresh()}catch(e){setError('Check JSON question format: '+String(e))}};
 if(!current)return <div className="page"><div className="page-top"><div><div className="eyebrow">ASSESSMENT LAB</div><h1>Timed assessments</h1><p>Timed quizzes with automatic saving and transparent scoring.</p></div><button className="btn secondary" onClick={()=>setCreate(!create)}>＋ Create assessment</button></div><div className="cards-grid">{items.map(a=><Panel key={a.id}><span className="chip">{a.require_start?'SERVER-TIMED':'PRACTICE'}</span><h2>{a.title}</h2><p>{a.questions.length} questions · {Math.ceil(a.duration_seconds/60)} min · -{a.negative_marking??.25} penalty · {a.cutoff_pct===null||a.cutoff_pct===undefined?'No cutoff':a.cutoff_pct+'% cutoff'}</p><button className="btn primary" onClick={()=>start(a)}>Begin assessment →</button></Panel>)}</div>{items.length===0&&<Empty title="No assessments found" detail="Ensure the backend is online to load the sample assessment."/>}
 {create&&<Panel title="Custom assessment"><p>Provide a JSON array of questions with id, stem, kind (single/multiple/numerical), correct, and options for choice questions. Numerical questions may define tolerance.</p><input value={title} onChange={e=>setTitle(e.target.value)} placeholder="Title"/><div className="row wrap"><label>Duration (minutes)<input type="number" min={1} max={240} value={minutes} onChange={e=>setMinutes(Number(e.target.value))}/></label><label>Penalty per wrong answer (0–1)<input type="number" min={0} max={1} step={.05} value={penalty} onChange={e=>setPenalty(Number(e.target.value))}/></label><label>Pass cutoff % (optional)<input type="number" min={0} max={100} value={cutoff} onChange={e=>setCutoff(e.target.value)} placeholder="None"/></label></div><p className="muted">The server controls the clock, penalty and cutoff after the attempt begins. These are local practice assessments, not remote-proctored examinations.</p><textarea rows={9} value={json} onChange={e=>setJson(e.target.value)} placeholder='[{"id":"q1","stem":"Question?","options":[{"label":"A","text":"Yes"},{"label":"B","text":"No"}],"correct":"A"}]'/><button className="btn primary" onClick={make}>Save assessment</button></Panel>}<ErrorText message={error}/></div>;
 const q=current.questions[index];
 return <div className="page"><div className="page-top"><div><div className="eyebrow">ACTIVE ASSESSMENT</div><h1>{current.title}</h1></div><div className="timer">◷ {Math.floor(remaining/60).toString().padStart(2,'0')}:{(remaining%60).toString().padStart(2,'0')}</div></div>
 {result?<Panel title="Your results"><div className="score-hero">{result.percent}%</div><p>{result.correct} correct · {result.incorrect} incorrect · {result.unanswered} unanswered</p><p>Raw score {result.score} / {result.maximum}. Recorded elapsed time {result.elapsed_seconds}s.</p>{result.timed_out&&<p role="status" className="muted">Time expired. The server graded answers saved before the deadline; later edits were not counted.</p>}{result.timing_enforcement==='legacy_unstarted_practice'&&<p className="muted">Legacy untimed practice submission. Start an assessment first for server-bound timing.</p>}{result.passed_cutoff!==null&&<p role="status"><strong>{result.passed_cutoff?'Cutoff reached':'Below cutoff'}</strong> · Required {result.cutoff_pct}%</p>}<h3>Section results</h3>{Object.entries(result.sections||{}).map(([name,value])=>{const v=value as {score:number;maximum:number;correct:number;incorrect:number;unanswered:number;accuracy_pct:number|null};return <p key={name}><strong>{name}:</strong> {v.score}/{v.maximum} points · {v.correct} correct · {v.incorrect} incorrect · {v.unanswered} unanswered</p>})}{result.explanations.map((x:any)=><div className="explain" key={x.id}><strong>{x.id} · {x.correct}</strong><p>{x.explanation}</p></div>)}<button className="btn primary" onClick={()=>setCurrent(null)}>← Back to assessments</button></Panel>:<div className="two-col"><Panel title={`Question ${index+1} of ${current.questions.length}`} extra={<span className="tiny">{q.section||'General'}</span>}><h2 className="question-title">{q.stem}</h2>{q.kind==='numerical' ? <div><label htmlFor={'numerical-'+q.id}>Numerical answer</label><input id={'numerical-'+q.id} inputMode="decimal" value={typeof answers[q.id]==='string'?answers[q.id] as string:''} onChange={e=>setAnswers(a=>({...a,[q.id]:e.target.value}))} placeholder="Enter a number"/></div> : <div className="choices">{(q.options||[]).map(o=>{const multiple=q.kind==='multiple'; const chosen=multiple?Array.isArray(answers[q.id])&& (answers[q.id] as string[]).includes(o.label):answers[q.id]===o.label;return <label key={o.label} className={'choice '+(chosen?'chosen':'')}><input type={multiple?'checkbox':'radio'} name={q.id} checked={chosen} onChange={()=>setAnswers(a=>{if(!multiple)return {...a,[q.id]:o.label};const previous=Array.isArray(a[q.id])?a[q.id] as string[]:[];return {...a,[q.id]:previous.includes(o.label)?previous.filter(x=>x!==o.label):[...previous,o.label]}})}/><b>{o.label}</b><span>{o.text}</span></label>})}</div>}<div className="row wrap"><button className="btn secondary" onClick={()=>setReview(r=>r.includes(q.id)?r.filter(x=>x!==q.id):[...r,q.id])}>{review.includes(q.id)?'✓ Reviewed':'☆ Mark for review'}</button><button className="btn secondary" disabled={index===0} onClick={()=>setIndex(i=>i-1)}>Previous</button><button className="btn primary" disabled={index>=current.questions.length-1} onClick={()=>setIndex(i=>i+1)}>Next →</button></div></Panel><Panel title="Question navigator"><div className="question-nav">{current.questions.map((x,i)=><button key={x.id} onClick={()=>setIndex(i)} className={(i===index?'selected ':'')+(answers[x.id]?'answered':'')}>{i+1}{review.includes(x.id)?'★':''}</button>)}</div><p className="muted">{Object.keys(answers).length} answered · {review.length} marked for review.</p><button className="btn primary wide" onClick={()=>finish()}>Submit assessment</button></Panel></div>}<p className="muted" role="status">{saveMessage}</p><ErrorText message={error}/></div>
}
