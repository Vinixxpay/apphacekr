import React,{useState,useEffect} from 'react';
import {AbsoluteFill,Audio,staticFile,useCurrentFrame,delayRender,continueRender} from 'remotion';
import cfg from '../campaign.json';
import timelines from '../public/timings-aligned.json';
import captions from '../public/captions.json';
import {B,L,W,PALE,ease,Text,Lines,Product,Outro,Panel,measure,Person,MiniPhone} from './Art';
import Scene from './Scenes';
type Word={text:string;start:number;end:number;hot:boolean};type Caption={start:number;end:number;words:Word[]};
const Background=({t}:{t:number})=><g><rect width={1080} height={1920} fill={B}/><circle cx={100} cy={1040} r={590} fill="#163FDC"/><path d="M0 1750L1080 360M0 1840L1080 450" stroke={W} strokeOpacity={.04} strokeWidth={70}/>{Array.from({length:15},(_,i)=>{const x=(i*173+35)%1080,y=(i*359+t*(7+i%3))%1920;return <circle key={i} cx={x} cy={y} r={i%3+2} fill={W} opacity={.12}/>;})}</g>;
export const Film=({id,cover=false}:{id:number;cover?:boolean})=>{
 const [h]=useState(()=>delayRender('Brand font'));useEffect(()=>{document.fonts.load('800 64px Montserrat').then(()=>continueRender(h))},[h]);
 const frame=useCurrentFrame(),t=frame/30,v=cfg.videos.find(v=>v.id===id)!;const time=timelines.find(v=>v.id===id)!;const caps=(captions as Record<string,Caption[]>)[id];const cap=caps?.find(c=>t>=c.start&&t<c.end);
 const index=time.scenes.reduce((n,s,i)=>s.start<=t?i:n,0),scene=time.scenes[index],local=t-scene.start;const final=scene.layout==='final'||scene.layout==='offer';const mouth=time.mouth[frame]||0;
 return <AbsoluteFill style={{background:B,fontFamily:'Montserrat',overflow:'hidden'}}><style>{`@font-face{font-family:Montserrat;src:url('${staticFile('fonts/Montserrat-ExtraBold.ttf')}');font-weight:800}*{box-sizing:border-box}`}</style>{!cover&&<Audio src={staticFile(`audio/${String(id).padStart(2,'0')}/mix.wav`)}/>}
 <svg width={1080} height={1920} viewBox="0 0 1080 1920"><Background t={t}/><Text x={130} y={266} anchor="start" size={30} width={300}>iB Mídias</Text><Text x={950} y={266} anchor="end" size={23} width={320} color={L}>{cover?'PARA VIDRACEIROS':`${String(id).padStart(2,'0')} / VIDRAÇARIAS`}</Text>
 {cover?<><Lines text={v.cover.toUpperCase()} y={655} size={79} width={820} accentLast/><Panel x={220} y={980} w={640} h={450}>{[1,2,9,11].includes(id)?<><Person x={430} y={1165} s={.65} t={0} pose="point"/><MiniPhone x={650} y={1070} t={0}/></>:id===8?<><Text y={1090} size={43} color={B}>MARKETING</Text><Text y={1200} size={43} color={B}>VENDAS</Text><Text y={1310} size={43} color={B}>PÓS-VENDA</Text></>:id===10?<><Text y={1110} size={40} color={B}>INVESTIMENTO</Text><Text y={1220} size={80} color={B}>÷</Text><Text y={1335} size={40} color={B}>VENDAS ATRIBUÍDAS</Text></>:<Product kind={id===3||id===12?'gate':id===4?'box':id===5?'house':'window'} x={270} y={1030} s={.9} t={0}/>}</Panel></>:<>
 {final?<Outro cta={v.cta} offer={v.offer} t={local}/>:<g opacity={ease(local/.23)} transform={`translate(${18*(1-ease(local/.35))} 0)`}><Scene layout={scene.layout} t={local} global={t} mouth={mouth} id={id}/></g>}
 {time.pauses.map((p,j)=>t>=p.start&&t<p.end?<g key={j}><Text y={1305} size={31} color={L}>{`SUA RESPOSTA? ${Math.ceil(p.end-t)}`}</Text></g>:null)}
 <g>{time.scenes.map((s,i)=><rect key={i} x={140+i*(800/time.scenes.length)} y={1367} width={800/time.scenes.length-8} height={5} rx={2.5} fill={i<=index?L:W} opacity={i<=index?1:.25}/>)}</g>
 </>}
 </svg>
 {!cover&&cap&&<div style={{position:'absolute',left:120,right:120,top:1410,height:150,display:'flex',justifyContent:'center',alignItems:'center'}}><div style={{maxWidth:840,background:W,border:'3px solid #0131CD',borderRadius:19,padding:'17px 24px',boxShadow:'0 7px 0 rgba(7,22,67,.22)',fontWeight:800,textAlign:'center',lineHeight:1.2,fontSize:Math.min(49,780/measure(cap.words.map(w=>w.text.toUpperCase()).join(' '),1)),transform:`scale(${.96+.04*ease((t-cap.start)/.12)})`}}>{cap.words.map((w,i)=><React.Fragment key={i}><span style={{color:t>=w.start?B:'#728BDB',background:t>=w.start&&w.hot?L:'transparent',borderRadius:6,padding:w.hot?'0 3px':0}}>{w.text.toUpperCase()}</span>{i<cap.words.length-1?' ':''}</React.Fragment>)}</div></div>}
 </AbsoluteFill>
};
