import React from 'react';import {B,L,W,E,T} from './Art';
export const Behind=({phase,t}:{phase:string;t:number})=>{
 if(phase==='problem')return <g opacity={.7}>{[0,1].map(i=><g key={i} transform={`translate(${18*(1-E((t-i*.12)/.4))} ${12*(1-E((t-i*.12)/.4))}) rotate(${-5+i*9} 540 980)`}><rect x={170+i*24} y={752+i*12} width={675} height={490} rx={18} fill="#17284B" stroke={B} strokeWidth={3} opacity={E((t-i*.12)/.35)}/></g>)}</g>;
 if(phase==='black')return <g opacity={1-E(t/.7)}><path d={`M${-520+1700*E(t/.6)} 310l-270 1080`} stroke="#597CFF" strokeWidth={40} opacity={.45}/><path d={`M${-620+1700*E(t/.6)} 310l-270 1080`} stroke={W} strokeWidth={2} opacity={.4}/></g>;
 if(phase==='price')return <g opacity={Math.max(0,1-t/.85)}><circle cx={540} cy={960} r={180+270*E(t/.7)} fill="none" stroke={B} strokeWidth={5} opacity={.65}/>{Array.from({length:12},(_,i)=>{const a=i*Math.PI/6,inner=330+75*E(t/.5),outer=inner+45;return <path key={i} d={`M${540+inner*Math.sin(a)} ${960+inner*Math.cos(a)}L${540+outer*Math.sin(a)} ${960+outer*Math.cos(a)}`} stroke={B} strokeWidth={5} strokeLinecap="round"/>})}</g>;
 return null;
};
export const Overlay=({phase,t,global,id,start,stop}:{phase:string;t:number;global:number;id:number;start:number;stop:number})=>{
 if(phase==='hook'&&id===1){const p=E((t-.45)/.35);return <g opacity={p} transform={`translate(0 ${12*(1-p)})`}><circle cx={564} cy={918} r={8} fill={B}/><circle cx={578} cy={889} r={12} fill={B}/><circle cx={605} cy={849} r={34} fill="#17284B" stroke={B} strokeWidth={3}/><T text="?" x={605} y={868} size={53}/></g>}
 if(phase==='price'){const a=E((t-.1)/.35);return <g opacity={.8*a}><path d={`M190 ${775+12*(1-a)}v-34h44M846 741h44v34M190 1127v34h44M846 1161h44v-34`} stroke={B} strokeWidth={4} fill="none"/></g>}
 if(phase==='clock'){const done=global>=stop;const p=Math.max(0,Math.min(1,(global-start)/Math.max(.1,stop-start)));const angle=(done?0:p*p*1080)*Math.PI/180;return <g>{[0,1,2].map(i=>{const a=angle+i*Math.PI*2/3;return <circle key={i} cx={540+295*Math.sin(a)} cy={1000-295*Math.cos(a)} r={done?7:5+i} fill={done?L:W} opacity={done?.85:.55}/>})}{done&&<g transform={`translate(784 1205) scale(${E((global-stop)/.15)})`}><circle r={31} fill={L}/><path d="M-14 0l10 11 21-25" stroke="#10141C" strokeWidth={8} fill="none" strokeLinecap="round" strokeLinejoin="round"/></g>}</g>}
 if(phase==='final')return <g><path d={`M${540-110*E(t/.45)} 592h${220*E(t/.45)}`} stroke={B} strokeWidth={3}/><rect x={155} y={1090} width={770} height={150} rx={16} fill="none" stroke={W} strokeWidth={2} strokeDasharray="100 1740" strokeDashoffset={-t*280} opacity={.38}/></g>;
 return null;
};
