import {useEffect,useState} from 'react';
import {request,fmtTime,type Session,type Stats} from './lib/api';
import {Panel,Metric,Empty} from './components/Ui';
import {Live} from './views/Live';
import {Assessments} from './views/Assessments';
import {SQLLab} from './views/SQLLab';
import {CodePractice,Documents,Communication,History,Analytics,Settings} from './views/Tools';
import {invoke,isTauri} from '@tauri-apps/api/core';
type Page='dashboard'|'live'|'assessments'|'coding'|'sql'|'system'|'ml'|'documents'|'communication'|'history'|'analytics'|'settings';
const NAV:{section:string;items:{id:Page;label:string;icon:string}[]}[]=[
 {section:'WORKSPACE',items:[{id:'dashboard',label:'Overview',icon:'◫'},{id:'live',label:'Live practice',icon:'◉'},{id:'assessments',label:'Assessments',icon:'▦'},{id:'coding',label:'Code workshop',icon:'⌘'},{id:'sql',label:'SQL lab',icon:'▤'}]},
 {section:'DEEP PRACTICE',items:[{id:'system',label:'System design',icon:'◇'},{id:'ml',label:'Machine learning',icon:'❖'},{id:'documents',label:'Resume & projects',icon:'▤'},{id:'communication',label:'Communication',icon:'◎'}]},
 {section:'YOUR PROGRESS',items:[{id:'history',label:'Session history',icon:'▣'},{id:'analytics',label:'Analytics',icon:'▥'},{id:'settings',label:'Settings',icon:'⚙'}]}
];
function Dashboard({go,sessions,stats,online}:{go:(p:Page)=>void;sessions:Session[];stats:Stats|null;online:boolean}){
 return <div className="page dashboard"><div className="page-top"><div><div className="eyebrow">YOUR PERSONAL INTERVIEW WORKSPACE</div><h1>Practice smarter.<br/><span>Interview with confidence.</span></h1><p>One focused space for coding, technical rounds, assessments, and communication.</p></div><div className="hero-orb">✳</div></div>
 <div className="hero-card"><div><span className="eyebrow">START HERE</span><h2>Ready for your next round?</h2><p>Get feedback, explore answer modes and keep every follow-up in context.</p><button className="btn bright" onClick={()=>go('live')}>✦ Begin practice session <b>↗</b></button></div><div className="hero-art" aria-hidden="true"><div className="orbit circle-one"/><div className="orbit circle-two"/><div className="art-core">AI</div></div></div>
 <div className="metric-grid four"><Metric label="Practice sessions" value={stats?.sessions??'—'} detail="Locally saved"/><Metric label="Questions explored" value={stats?.questions??'—'} detail="Across all sessions"/><Metric label="Assessments done" value={stats?.assessments_completed??'—'} detail="Scored practice"/><Metric label="Worker status" value={online?'Online':'Offline'} detail={online?'Ready for practice':'Start AI worker first'}/></div>
 <div className="two-col"><Panel title="Explore practice modes" extra={<span className="tiny">FOCUS AREAS</span>}><div className="launch-grid">{[{p:'assessments',icon:'▦',name:'Timed quizzes',desc:'Practice under a clock'},{p:'coding',icon:'⌘',name:'Coding & DSA',desc:'Learn optimal approaches'},{p:'system',icon:'◇',name:'System design',desc:'Architect and explain'},{p:'communication',icon:'◎',name:'Communication',desc:'Improve delivery'}].map(x=><button key={x.p} onClick={()=>go(x.p as Page)} className="launch"><span>{x.icon}</span><strong>{x.name}</strong><small>{x.desc}</small></button>)}</div></Panel><Panel title="Recent practice" extra={<button className="linklike" onClick={()=>go('history')}>View all</button>}>{sessions.length?sessions.slice(0,5).map(s=><div className="list-row" key={s.id}><div><strong>{s.title}</strong><small>{fmtTime(s.updated)}</small></div><span className="arrow">↗</span></div>):<Empty title="A fresh start" detail="Your completed practice sessions will appear here."/>}</Panel></div>
 </div>
}
export default function App(){const [page,setPage]=useState<Page>('dashboard'),[sessions,setSessions]=useState<Session[]>([]),[stats,setStats]=useState<Stats|null>(null),[online,setOnline]=useState(false),[theme,setTheme]=useState(localStorage.getItem('studio-theme')||'dark'),[compact,setCompact]=useState(false),[seed,setSeed]=useState(''),[openSid,setOpenSid]=useState('');
 const refresh=()=>{request<Session[]>('/api/sessions').then(setSessions).catch(()=>{});request<Stats>('/api/stats').then(setStats).catch(()=>{})};
 useEffect(()=>{refresh();request('/api/health').then(()=>setOnline(true)).catch(()=>setOnline(false))},[]);
 useEffect(()=>{document.documentElement.dataset.theme=theme;localStorage.setItem('studio-theme',theme)},[theme]);
 const go=(p:Page)=>{setPage(p);setCompact(false);refresh()};
 const goLive=(q:string)=>{setSeed(q);go('live')};
 const [workerStage,setWorkerStage]=useState('initializing'),[diagnosticExport,setDiagnosticExport]=useState('');
 useEffect(()=>{let alive=true;
   const check=async()=>{
     try {
       if(isTauri()){
         const status=await invoke<{ready:boolean;stage:string}>('worker_status');
         if(alive){setWorkerStage(status.stage);setOnline(status.ready)}
       }else{
         await request('/api/health');if(alive){setOnline(true);setWorkerStage('ready')}
       }
     }catch{if(alive){setOnline(false);setWorkerStage('unavailable')}}
   };
   void check();const timer=setInterval(check,5000);
   return()=>{alive=false;clearInterval(timer)};
 },[]);
 const recoverWorker=async()=>{
   try{
     if(isTauri()){await invoke('restart_worker');await invoke('worker_connection')}
     await request('/api/health');
     setOnline(true);setWorkerStage('ready');refresh();
   }catch(e){setOnline(false);setWorkerStage('unavailable');alert('Worker failed authenticated readiness: '+String(e))}
 };
 const exportDiagnostics=async()=>{
   try{setDiagnosticExport(await invoke<string>('export_worker_diagnostics'))}
   catch(e){setDiagnosticExport('Diagnostic export unavailable: '+String(e))}
 };
 const overlay=async()=>{try{await invoke('set_compact',{compact:!compact});setCompact(x=>!x)}catch(e){alert('Compact mode requires the Tauri desktop shell: '+String(e))}};
 const content=page==='dashboard'?<Dashboard go={go} sessions={sessions} stats={stats} online={online}/>:page==='live'?<Live key={openSid+seed} sessions={sessions} seed={seed} initialSid={openSid} refresh={refresh}/>:page==='assessments'?<Assessments/>:page==='coding'?<CodePractice goLive={goLive}/>:page==='sql'?<SQLLab/>:page==='documents'?<Documents goLive={goLive}/>:page==='communication'?<Communication/>:page==='history'?<History sessions={sessions} refresh={refresh} onOpen={id=>{setOpenSid(id);go('live')}}/>:page==='analytics'?<Analytics/>:page==='settings'?<Settings theme={theme} setTheme={setTheme}/>:<div className="page"><div className="page-top"><div><div className="eyebrow">SPECIALIST PRACTICE</div><h1>{page==='ml'?'Machine learning interviews':'System design interviews'}</h1><p>{page==='ml'?'Reason about evaluation, generalization, algorithms, and ML architectures.':'Practice requirements, trade-offs, scaling, APIs and technical diagrams.'}</p></div></div><Panel title="Guided sessions"><p>Pick a prompt and explore it with the AI practice coach.</p><div className="practice-topics">{(page==='ml'?['Explain bias versus variance','Design a recommendation engine','Derive logistic regression','Explain ROC-AUC vs PR-AUC','ML model monitoring']:['Design a URL shortener','Design a high-scale chat system','Design a payment system','Design a video streaming service','Design a distributed cache']).map(t=><button key={t} onClick={()=>goLive(t+'; give requirements, alternatives, trade-offs, and follow-up interview questions.')}>{t} ↗</button>)}</div><button className="btn primary" onClick={()=>go('live')}>Open practice workspace</button></Panel></div>;
 return <div className={'shell '+(compact?'compact':'')}><aside className="sidebar"><div className="brand"><div className="brand-mark">✳</div><div><strong>INTERVIEW<span>STUDIO</span></strong><small>AI-powered practice</small></div></div><nav>{NAV.map(group=><div key={group.section} className="nav-group"><div className="nav-label">{group.section}</div>{group.items.map(x=><button key={x.id} onClick={()=>go(x.id)} className={'nav-item '+(page===x.id?'active':'')}><span>{x.icon}</span>{x.label}{page===x.id&&<i>●</i>}</button>)}</div>)}</nav><div className="sidebar-bottom"><div className="connection"><span className={'connection-dot '+(online?'yes':'')}/><div><strong>{online?'AI worker connected':'Worker offline'}</strong><small>{online?'Local secure workspace':'Run scripts/dev.ps1'}</small></div></div><p>AI Interview Studio<br/><span>Version 1.0.0 RC4 · Overlay-first preview</span></p></div></aside><main className="main"><header className="topbar"><div className="breadcrumb">WORKSPACE <span>/</span> {NAV.flatMap(g=>g.items).find(x=>x.id===page)?.label}</div><div className="top-actions"><span className="top-hint">Practice only</span><button className="icon-button" title="Toggle theme" onClick={()=>setTheme(theme==='dark'?'light':'dark')}>{theme==='dark'?'☼':'☾'}</button><button className="btn secondary compact-btn" onClick={overlay}>{compact?'Expand':'▣ Compact'}</button><span className="avatar">IS</span></div></header>{!online&&<div className="offline-warning">⚠ AI worker: {workerStage}. AI and practice features may be unavailable. <button onClick={recoverWorker}>Restart / Retry</button> {isTauri()&&<button onClick={exportDiagnostics}>Export diagnostics</button>} {diagnosticExport&&<span className="tiny">{diagnosticExport}</span>}</div>}{content}<footer>Designed for authorized interview preparation · Local-first storage · Model outputs may be incorrect</footer></main></div>
}
