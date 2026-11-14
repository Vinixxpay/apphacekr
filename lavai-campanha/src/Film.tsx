import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,staticFile,useCurrentFrame,delayRender,continueRender} from 'remotion';
import timings from '../public/timings.json';
import caps1 from '../public/captions-1.json';
import caps2 from '../public/captions-2.json';
import caps3 from '../public/captions-3.json';
import {Owner,T,Coin} from './Actors';
import {Y,D,W,E,Bay,Car,Notebook,Calculator,Receipt,Phone,Offer} from './Art';
const Head=({lines,t=1}:{lines:string[];t?:number})=><g opacity={E(t/.35)} transform={`translate(0 ${25*(1-E(t/.4))})`}>{lines.map((line,i)=><T key={line} x={540} y={275+i*88} size={lines.length>2?69:78} fill={i===lines.length-1?Y:W}>{line}</T>)}</g>;
const Banner=({text,y=1435,size=43}:{text:string;y?:number;size?:number})=><g><rect x={85} y={y-70} width={910} height={105} rx={20} fill={Y}/><T x={540} y={y} size={size} fill={D}>{text}</T></g>;
const PaperStorm=({t=0}:{t?:number})=><g>{Array.from({length:6},(_,n)=>{const p=(t*.38+n*.18)%1;return <Receipt key={n} x={65+(n*173)%950+Math.sin(t*2+n)*35} y={620+p*820} s={.37} angle={-24+n*9+Math.sin(t*3+n)*12}/>})}</g>;
const Tap=({x,y,t}:{x:number;y:number;t:number})=><g transform={`translate(${x} ${y})`}><circle r={22+16*(.5+.5*Math.sin(t*5))} fill="none" stroke={Y} strokeWidth={6} opacity={.6}/><path d="M8 60V-25q-1-34-22-27l-1 59q-45-30-54-8-3 28 32 60Z" fill="#E8B989" stroke={D} strokeWidth={7}/></g>;
export const Film=({id}:{id:number})=>{
 const [handle]=useState(()=>delayRender('Lavaí font'));useEffect(()=>{document.fonts.load('800 64px Montserrat').then(()=>continueRender(handle))},[handle]);
 const frame=useCurrentFrame(),t=frame/30;const v=timings.find(v=>v.id===id)!;const allCaps=id===1?caps1:id===2?caps2:caps3;const group=allCaps.find(c=>t>=c.start&&t<c.end);const c:any=v.cues;const intro=id===2?Math.max(5.2,c.imagine):c.intro;const offer=t>=c.price-.1;const app=t>=intro;
 const mouth=v.mouth[frame]||0;let page='clients';const local=t-intro;
 if(id===1)page=t<c.services?'clients':'services';
 if(id===2)page=t<c.demoServices?'clients':t<c.receipt?'services':t<c.receipt+1.4?'receipt':'share';
 if(id===2&&t>c.intro+4){const cycle=Math.floor((t-(c.intro+4))/2.2)%3;page=cycle===0?'clients':cycle===1?'services':'share';}
 if(id===3)page=t<c.services?'clients':t<c.receipt?'services':t<c.receipt+1?'receipt':'share';
 const isSplit=id===2&&t>=4.5&&t<intro+.5;
 return <AbsoluteFill style={{fontFamily:'Montserrat',background:D,overflow:'hidden'}}><style>{`@font-face{font-family:Montserrat;src:url('${staticFile('fonts/Montserrat-ExtraBold.ttf')}');font-weight:800}*{box-sizing:border-box}`}</style><Audio src={staticFile(`audio/v${id}/mix.wav`)}/>
 <svg width={1080} height={1920} viewBox="0 0 1080 1920">
 {offer?<Offer t={t-(c.price-.1)}/>:<><Bay t={t} desk={id===2}/><T x={80} y={154} size={28} fill={W} anchor="start">LAVAÍ APP</T>
 {!app&&<>
 {id===1&&<><Head lines={t<6?['VOCÊ SABE','QUANTO FATURA?']:['CLIENTE CHEGANDO.','CADÊ O CONTROLE?']} t={t}/><g transform={`translate(${t<2.5?0:-22*E((t-2.5)/.5)} 0) scale(${t<2.5?1:1.04})`}><Owner id={id} x={300} y={970} s={1.1} t={t} pose={t<5?'work':'shrug'} emotion="worried"/><Car x={340+350*(1-E(t/1.2))} y={1240} s={.9} t={t} foam/></g>{t>5&&<><Car x={700-220*E((t-5)/1.2)} y={920} s={.66} t={t} color={Y}/><Notebook x={510} y={1130} s={.85} angle={Math.sin(t*3)*7}/><Coin x={900} y={1250+Math.sin(t*4)*16} s={.8}/><Receipt x={730} y={740+Math.sin(t*2)*35} s={.47} angle={-12}/></>}{t>9.5&&<Banner text="CHEGA DE DESORGANIZAÇÃO" size={41}/>}</>}
 {id===2&&<><Head lines={['AINDA USA','CADERNO?']} t={t}/>{!isSplit?<><Owner id={id} x={315} y={975} s={1.05} t={t} pose="shrug" emotion="worried"/><Notebook x={590+Math.sin(t*3)*30} y={820+Math.cos(t*2)*22} s={.95} angle={-12+Math.sin(t*2)*8}/><Calculator x={720} y={1170} s={.85} angle={10+Math.sin(t*3)*9}/><PaperStorm t={t}/></>:<><path d="M540 510v950" stroke={Y} strokeWidth={8} strokeDasharray="18 15"/><Notebook x={100} y={840} s={.9} angle={-12}/><Calculator x={255} y={1210} s={.7}/><Phone x={590} y={720} s={.65} t={t}/><T x={275} y={720} size={35} fill={W}>PAPEL</T><T x={800} y={650} size={35} fill={Y}>ORGANIZAÇÃO</T></>}</>}
 {id===3&&<><Head lines={['VOCÊ É DONO','OU REFÉM DO','SEU NEGÓCIO?']} t={t}/>{t<2.5?<Owner id={id} x={540} y={970} s={1.5} t={t} mouth={mouth} pose="point" emotion="worried"/>:<><Owner id={id} x={230+430*(.5+.5*Math.sin(t*1.7))} y={1020} s={.96} t={t} pose="work" emotion="tired" run/><Car x={340} y={1250} s={.9} t={t} foam/><PaperStorm t={t}/><g transform={`translate(820 900) rotate(${Math.sin(t*29)*9})`}><rect width={125} height={195} rx={25} fill="#5C7180" stroke={D} strokeWidth={10}/><rect x={15} y={28} width={95} height={135} fill={Y}/></g></>}</>}
 </>}
 {app&&<><Head lines={id===1?['CONTROLE SEUS','SERVIÇOS']:id===2?['MENOS PAPEL.','MAIS CONTROLE.']:['TUDO NA','PALMA DA MÃO']} t={local}/><g opacity={E(local/.4)} transform={`translate(${id===2?0:30*(1-E(local/.6))} ${35*(1-E(local/.45))})`}><Phone x={270} y={485} s={.93} t={Math.max(0,local)} page={page}/></g><Owner id={id} x={140} y={1265} s={.48} t={t} pose="point"/>{(page==='clients'||page==='services')&&local>.5&&<Tap x={790} y={1150} t={local}/>}<g opacity={E((local-1)/.5)}><rect x={820} y={805} width={175} height={70} rx={18} fill={Y}/><T x={907} y={853} size={27} fill={D}>{page==='share'?'WHATSAPP':page==='receipt'?'PDF / PNG':page==='clients'?'CLIENTES':'SERVIÇOS'}</T><path d="M855 900l30 32 65-82" fill="none" stroke={W} strokeWidth={13} strokeLinecap="round"/></g>{id===2&&page==='share'&&<Banner text="RECIBOS PELO WHATSAPP" y={1450} size={43}/>}<rect width={1080} height={1920} fill={Y} opacity={Math.max(0,1-local/.28)} pointerEvents="none"/></>}
 </>}
 </svg>
 {group&&<div style={{position:'absolute',top:1560,left:65,right:65,height:135,display:'flex',alignItems:'center',justifyContent:'center'}}><div style={{fontSize:57,fontWeight:800,lineHeight:1.17,textAlign:'center',color:W,WebkitTextStroke:'2px #071321',paintOrder:'stroke fill',textShadow:'0 4px 1px #071321',maxWidth:940,transform:`scale(${.97+.03*E((t-group.start)/.1)})`}}>{group.words.map((w,i)=><React.Fragment key={i}><span style={{color:t>=w.start&&w.hot?Y:W}}>{w.text}</span>{i<group.words.length-1?' ':''}</React.Fragment>)}</div></div>}
 </AbsoluteFill>
};
