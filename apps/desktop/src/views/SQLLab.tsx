import {useEffect,useState} from 'react';
import {request} from '../lib/api';
import {Panel,ErrorText} from '../components/Ui';
type Schema={tables:{table:string;columns:string[]}[];read_only:boolean;example:string};
type Result={columns:string[];rows:(string|number|null)[][];row_count:number;truncated:boolean;elapsed_ms:number;verified:string;dataset:string};
export function SQLLab(){
 const [schema,setSchema]=useState<Schema|null>(null),[query,setQuery]=useState('SELECT d.name AS department, COUNT(e.id) AS people\nFROM departments d\nLEFT JOIN employees e ON e.department_id = d.id\nGROUP BY d.id\nORDER BY people DESC;');
 const [result,setResult]=useState<Result|null>(null),[error,setError]=useState(''),[busy,setBusy]=useState(false);
 useEffect(()=>{request<Schema>('/api/sql/schema').then(setSchema).catch(e=>setError(String(e)))},[]);
 const execute=async()=>{setBusy(true);setError('');setResult(null);try{setResult(await request<Result>('/api/sql/query','POST',{query,max_rows:100}))}catch(e){setError(String(e))}finally{setBusy(false)}};
 return <div className="page"><div className="page-top"><div><div className="eyebrow">SAFE DATA PRACTICE</div><h1>SQL practice laboratory</h1><p>Execute read-only SQL against a built-in training dataset. No user or production database connections.</p></div></div>
 <div className="two-col"><Panel title="SQL query editor"><textarea className="code-editor" spellCheck={false} aria-label="SQL editor" rows={13} value={query} onChange={e=>setQuery(e.target.value)}/><div className="row wrap"><button className="btn primary" disabled={busy||!query.trim()} onClick={execute}>{busy?'Running…':'▶ Run read-only query'}</button><button className="btn secondary" onClick={()=>setQuery('SELECT e.name, SUM(s.amount) AS revenue\nFROM employees e JOIN sales s ON e.id=s.employee_id\nGROUP BY e.id ORDER BY revenue DESC;')}>Try JOIN example</button></div><ErrorText message={error}/>{result&&<div className="success" role="status">{result.row_count} rows · {result.elapsed_ms} ms · {result.verified}{result.truncated?' · first 100 rows only':''}</div>}</Panel>
 <Panel title="Practice schema">{schema?.tables.map(t=><div className="list-row" key={t.table}><div><strong>{t.table}</strong><small>{t.columns.join(' · ')}</small></div></div>)}<p className="muted">Queries are restricted by SQLite's authorizer, memory-backed fixture, a 300 ms execution deadline, and result limits. They never run against personal databases.</p></Panel></div>
 {result&&<Panel title="Query results"><div style={{overflowX:'auto'}}><table className="sql-results"><thead><tr>{result.columns.map((c,i)=><th key={i}>{c}</th>)}</tr></thead><tbody>{result.rows.map((r,i)=><tr key={i}>{r.map((v,j)=><td key={j}>{v===null?'NULL':String(v)}</td>)}</tr>)}</tbody></table></div></Panel>}</div>
}
