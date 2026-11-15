import React,{useState,useEffect} from 'react';
import {AbsoluteFill,Audio,staticFile,useCurrentFrame,delayRender,continueRender} from 'remotion';
import cfg from '../campaign.json';
import timelines from '../public/timings-aligned.json';
import captions from '../public/captions.json';
import {B,L,W,PALE,ease,Text,Lines,Car,Final,Panel,measure,Person} from './Art';
import Scene from './Scenes';
type Word={text:string;start:number;end:number;hot:boolean};type Caption={start:number;end:number;words:Word[]};
const Background=({t}:{t:number})=><g><rect width={1080} height={1920} fill={B}/><circle cx={80} cy={1100} r={630} fill="#1E293B"/><path d="M0 1860L1080 480" stroke={L} strokeOpacity={.025} strokeWidth={250}/>{Array.from({length:13},(_,i)=><circle key={i} cx={(i*173+25)%1080} cy={(i*317+t*(6+i%3))%1920} r={i%3+2} fill={W} opacity={.12}/>)}</g>;
export const Film=({id,cover=false}:{id:number;cover?:boolean})=>{
 const [h]=useState(()=>delayRender('Brand font'));useEffect(()=>{Promise.all([document.fonts.load('700 64px Poppins'),document.fonts.load('600 48px Inter')]).then(()=>continueRender(h))},[h]);
 const frame=useCurrentFrame(),t=frame/30,v=cfg.videos.find(v=>v.id===id)!;const time=timelines.find(v=>v.id===id)!;const caps=(captions as Record<string,Caption[]>)[id];const cap=caps?.find(c=>t>=c.start&&t<c.end);
 const index=time.scenes.reduce((n,s,i)=>s.start<=t?i:n,0),scene=time.scenes[index],local=t-scene.start;const final=scene.layout==='final';const mouth=time.mouth[frame]||0;
 return <AbsoluteFill style={{background:B,fontFamily:'Inter',overflow:'hidden'}}><style>{`@font-face{font-family:Poppins;src:url('${staticFile('fonts/Poppins-Bold.ttf')}');font-weight:700}@font-face{font-family:Inter;src:url('${staticFile('fonts/Inter-SemiBold.woff2')}');font-weight:600}*{box-sizing:border-box}`}</style>{!cover&&<Audio src={staticFile(`audio/${String(id).padStart(2,'0')}/mix.wav`)}/>}
 <svg width={1080} height={1920} viewBox="0 0 1080 1920"><Background t={t}/><Text x={130} y={266} anchor="start" size={34} width={300} heading>Lavaí</Text><Text x={950} y={266} anchor="end" size={23} width={320} color={L}>{cover?'LAVA-RÁPIDOS E ESTÉTICAS':`${String(id).padStart(2,'0')} / GESTÃO PELO CELULAR`}</Text>
 {!cover&&!final&&<Text x={950} y={312} anchor="end" size={23} width={550} color="#A9B5C6">Demonstração ilustrativa</Text>}
 {cover?<><Lines text={v.cover.toUpperCase()} y={625} size={76} width={820} heading accentLast/><Panel x={170} y={985} w={740} h={390}><Car x={225} y={1095} s={.95} kind={id===3||id===5?'suv':'car'} mud={id===3} foam={id!==3}/></Panel><Text y={1465} size={27} color={L}>ORGANIZAÇÃO PELO CELULAR</Text></>:<>
 {final?<Final t={local}/>:<g opacity={ease(local/.23)} transform={`translate(${18*(1-ease(local/.35))} 0)`}><Scene layout={scene.layout} t={local} global={t} mouth={mouth}/></g>}
 {time.pauses.map((p,j)=>t>=p.start&&t<p.end?<g key={j}><Text y={1320} size={31} color={L}>{`SUA RESPOSTA? ${Math.ceil(p.end-t)}`}</Text></g>:null)}
 <g>{time.scenes.map((s,i)=><rect key={i} x={140+i*(800/time.scenes.length)} y={1367} width={800/time.scenes.length-8} height={5} rx={2.5} fill={i<=index?L:W} opacity={i<=index?1:.25}/>)}</g>
 </>}
 </svg>
 {!cover&&cap&&<div style={{position:'absolute',left:120,right:120,top:1410,height:150,display:'flex',justifyContent:'center',alignItems:'center'}}><div style={{maxWidth:840,background:W,border:'3px solid #0F172A',borderRadius:19,padding:'17px 24px',boxShadow:'0 7px 0 rgba(7,22,67,.22)',fontWeight:600,textAlign:'center',lineHeight:1.2,fontSize:Math.min(49,780/measure(cap.words.map(w=>w.text.toUpperCase()).join(' '),1)),transform:`scale(${.96+.04*ease((t-cap.start)/.12)})`}}>{cap.words.map((w,i)=><React.Fragment key={i}><span style={{color:t>=w.start?B:'#7D8B9D',background:t>=w.start&&w.hot?L:'transparent',borderRadius:6,padding:w.hot?'0 3px':0}}>{w.text.toUpperCase()}</span>{i<cap.words.length-1?' ':''}</React.Fragment>)}</div></div>}
 </AbsoluteFill>
};
