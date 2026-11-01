import {useEffect,useRef,useState} from 'react';
import {request,type Assessment} from '../lib/api';
import {Panel,Empty,ErrorText} from '../components/Ui';
export function Assessments(){
 const [items,setItems]=useState<Assessment[]>([]),[current,setCurrent]=useState<Assessment|null>(null),[answers,setAnswers]=useState<Record<string,string>>({}),[index,setIndex]=useState(0),[remaining,setRemaining]=useState(0),[started,setStarted]=useState(0),[result,setResult]=useState<any>(null),[error,setError]=useState(''),[review,setReview]=useState<string[]>([]),[saveMessage,setSaveMessage]=useState(''),[create,setCreate]=useState(false),[json,setJson]=useState(''),[title,setTitle]=useState('Custom quiz');
 const deadline=useRef(0),submitting=useRef(false);
 const refresh=()=>request<Assessment[]>('/api/assessments').then(setItems).catch(e=>setError(String(e)));
 useEffect(()=>{refresh()},[]);
 useEffect(()=>{if(!current||result)return;const id=window.setInterval(()=>{const s=Math.max(0,Math.ceil((deadline.current-Date.now())/1000));setRemaining(s);if(!s&&!submitting.current){submitting.current=true;finish()}},500);return()=>clearInterval(id)},[current,result,answers,started]);
 const start=async(a:Assessment)=>{
  setError('');setSaveMessage('Loading saved progress…');
  try{
   const x=await request<{draft:{answers:Record<string,string>;review:string[];started:number}|null}>(`/api/assessments/${a.id}/draft`);
   const at=x.draft?.started??Date.now()/1000;
   setCurrent(a);setIndex(0);setAnswers(x.draft?.answers??{});setResult(null);setReview(x.draft?.review??[]);
   submitting.current=false;setStarted(at);deadline.current=at*1000+a.duration_seconds*1000;
   setRemaining(Math.max(0,Math.ceil((deadline.current-Date.now())/1000)));
   setSaveMessage(x.draft?'Restored locally saved answers':'New assessment started');
  }catch(e){setError(String(e));setSaveMessage('')}
 };
 useEffect(()=>{
  if(!current||result||!started||submitting.current)return;
  const timer=setTimeout(()=>request(`/api/assessments/${current.id}/draft`,'POST',{answers,review,started})
   .then(()=>setSaveMessage('Answers saved locally')).catch(e=>setSaveMessage('Autosave error: '+String(e))),350);
  return ()=>clearTimeout(timer);
 },[current,answers,review,started,result]);
 const finish=async()=>{if(!current)return;submitting.current=true;try{setResult(await request(`/api/assessments/${current.id}/submit`,'POST',{answers,started,negative_marking:.25}))}catch(e){setError(String(e));submitting.current=false}};
 const make=async()=>{try{const q=JSON.parse(json);await request('/api/assessments','POST',{title,duration_seconds:300,questions:q});setCreate(false);setJson('');refresh()}catch(e){setError('Check JSON question format: '+String(e))}};
 if(!current)return <div className="page"><div className="page-top"><div><div className="eyebrow">ASSESSMENT LAB</div><h1>Timed assessments</h1><p>Timed quizzes with automatic saving and transparent scoring.</p></div><button className="btn secondary" onClick={()=>setCreate(!create)}>＋ Create assessment</button></div><div className="cards-grid">{items.map(a=><Panel key={a.id}><span className="chip">SELF-PACED</span><h2>{a.title}</h2><p>{a.questions.length} questions · {Math.ceil(a.duration_seconds/60)} min · -0.25 negative marking</p><button className="btn primary" onClick={()=>start(a)}>Begin assessment →</button></Panel>)}</div>{items.length===0&&<Empty title="No assessments found" detail="Ensure the backend is online to load the sample assessment."/>}
 {create&&<Panel title="Custom assessment"><p>Provide a JSON array of questions with id, stem, options (label and text), correct, and optional explanation.</p><input value={title} onChange={e=>setTitle(e.target.value)} placeholder="Title"/><textarea rows={9} value={json} onChange={e=>setJson(e.target.value)} placeholder='[{"id":"q1","stem":"Question?","options":[{"label":"A","text":"Yes"}],"correct":"A"}]'/><button className="btn primary" onClick={make}>Save assessment</button></Panel>}<ErrorText message={error}/></div>;
 const q=current.questions[index];
 return <div className="page"><div className="page-top"><div><div className="eyebrow">ACTIVE ASSESSMENT</div><h1>{current.title}</h1></div><div className="timer">◷ {Math.floor(remaining/60).toString().padStart(2,'0')}:{(remaining%60).toString().padStart(2,'0')}</div></div>
 {result?<Panel title="Your results"><div className="score-hero">{result.percent}%</div><p>{result.correct} correct · {result.incorrect} incorrect · {result.unanswered} unanswered</p><p>Raw score {result.score} / {result.maximum}. Recorded elapsed time {result.elapsed_seconds}s.</p>{result.explanations.map((x:any)=><div className="explain" key={x.id}><strong>{x.id} · {x.correct}</strong><p>{x.explanation}</p></div>)}<button className="btn primary" onClick={()=>setCurrent(null)}>← Back to assessments</button></Panel>:<div className="two-col"><Panel title={`Question ${index+1} of ${current.questions.length}`} extra={<span className="tiny">{q.section||'General'}</span>}><h2 className="question-title">{q.stem}</h2><div className="choices">{q.options.map(o=><label key={o.label} className={'choice '+(answers[q.id]===o.label?'chosen':'')}><input type="radio" name={q.id} checked={answers[q.id]===o.label} onChange={()=>setAnswers(a=>({...a,[q.id]:o.label}))}/><b>{o.label}</b><span>{o.text}</span></label>)}</div><div className="row wrap"><button className="btn secondary" onClick={()=>setReview(r=>r.includes(q.id)?r.filter(x=>x!==q.id):[...r,q.id])}>{review.includes(q.id)?'✓ Reviewed':'☆ Mark for review'}</button><button className="btn secondary" disabled={index===0} onClick={()=>setIndex(i=>i-1)}>Previous</button><button className="btn primary" disabled={index>=current.questions.length-1} onClick={()=>setIndex(i=>i+1)}>Next →</button></div></Panel><Panel title="Question navigator"><div className="question-nav">{current.questions.map((x,i)=><button key={x.id} onClick={()=>setIndex(i)} className={(i===index?'selected ':'')+(answers[x.id]?'answered':'')}>{i+1}{review.includes(x.id)?'★':''}</button>)}</div><p className="muted">{Object.keys(answers).length} answered · {review.length} marked for review.</p><button className="btn primary wide" onClick={finish}>Submit assessment</button></Panel></div>}<p className="muted" role="status">{saveMessage}</p><ErrorText message={error}/></div>
}
