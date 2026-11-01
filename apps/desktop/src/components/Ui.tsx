import type {ReactNode} from 'react';
export function Panel({children,title,extra,className=''}:{children:ReactNode;title?:string;extra?:ReactNode;className?:string}){
 return <section className={'panel '+className}>{(title||extra)&&<div className="panel-heading"><h3>{title}</h3>{extra}</div>}{children}</section>
}
export function Empty({title,detail}:{title:string;detail:string}){return <div className="empty"><div className="empty-icon">✧</div><strong>{title}</strong><p>{detail}</p></div>}
export function Label({children}:{children:ReactNode}){return <label className="field-label">{children}</label>}
export function ErrorText({message}:{message:string}){return message?<div className="error" role="alert">{message}</div>:null}
export function Metric({value,label,detail}:{value:ReactNode;label:string;detail?:string}){return <div className="metric"><span>{label}</span><strong>{value}</strong>{detail&&<small>{detail}</small>}</div>}
