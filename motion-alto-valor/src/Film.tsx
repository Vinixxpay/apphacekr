import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,Img,staticFile,useCurrentFrame,delayRender,continueRender} from 'remotion';
import raw from '../public/timeline.json';
import captions from '../public/captions.json';
import {Art,B,G,ease} from './Art';
const titles:Record<string,string[]>={hook:['VIDROS, PORTÕES','OU ESQUADRIAS?'],busy:['AGENDA CHEIA.','E O RETORNO?'],price:['ATRAINDO SÓ','QUEM BUSCA PREÇO?'],four:['E SE 1 PROJETO','VALESSE POR 4?'],value:['ATRAIA QUEM','VALORIZA SEU TRABALHO.'],ads:['ANÚNCIOS COM','ESTRATÉGIA.'],work:['VOCÊ CUIDA','DA EXECUÇÃO.'],cta:['MAIS VALOR PARA','O SEU TRABALHO.']};
export const Film=()=>{
 const [handle]=useState(()=>delayRender('Montserrat'));useEffect(()=>{document.fonts.load('800 64px Montserrat').then(()=>continueRender(handle))},[handle]);
 const frame=useCurrentFrame(),t=frame/30;const s=raw.scenes.find(s=>t>=s.start&&t<s.end)||raw.scenes[0];const local=Math.max(0,t-s.start);const dark=['hook','four','ads','cta'].includes(s.kind);const progress=ease(local/.45);const group=captions.find(c=>t>=c.start&&t<c.end);const ink=dark?'white':B;const lines=titles[s.kind];
 return <AbsoluteFill style={{fontFamily:'Montserrat',background:dark?'#071632':'#F4F7FF',overflow:'hidden'}}>
 <style>{`@font-face{font-family:Montserrat;src:url('${staticFile('fonts/Montserrat-ExtraBold.ttf')}');font-weight:800;}*{box-sizing:border-box}`}</style>
 <Audio src={staticFile('audio/mix.wav')}/>
 <AbsoluteFill style={{background:dark?'radial-gradient(ellipse at 85% 15%, #0131CD 0%, transparent 58%)':'radial-gradient(ellipse at 90% 10%, #D9E7FF 0%, transparent 60%)'}}/>
 <AbsoluteFill style={{opacity:dark?.09:.30,backgroundImage:`linear-gradient(${dark?'#6B9DFF':'#D1E0FB'} 1px,transparent 1px),linear-gradient(90deg,${dark?'#6B9DFF':'#D1E0FB'} 1px,transparent 1px)`,backgroundSize:'100px 100px',transform:`translateY(${(frame%300)/10}px)`}}/>
 <div style={{position:'absolute',top:138,left:80,right:80,display:'flex',alignItems:'center',justifyContent:'space-between',color:ink}}><div style={{fontSize:28,letterSpacing:3}}>iB MÍDIAS</div><div style={{background:G,color:B,fontSize:23,borderRadius:22,padding:'11px 20px'}}>ESTRATÉGIA DIGITAL</div></div>
 <div style={{position:'absolute',left:78,right:65,top:242,color:ink,opacity:progress,transform:`translateY(${26*(1-progress)}px)`}}>
 {lines.map((line,i)=><div key={line} style={{fontSize:line.length>23?57:line.length>20?65:78,lineHeight:1.15,fontWeight:800,letterSpacing:-2,whiteSpace:'nowrap',color:i===1&&dark?G:ink}}>{line}</div>)}
 <div style={{fontSize:31,marginTop:30,lineHeight:1.3,opacity:.85}}>{s.subtitle}</div>
 </div>
 {s.kind!=='cta'?<div style={{position:'absolute',top:590,left:90,opacity:progress,transform:`translateY(${25*(1-progress)}px)`}}><Art kind={s.kind} t={local} dark={dark}/></div>:<>
 <Img src={staticFile('logo.svg')} style={{position:'absolute',top:600,left:340,width:400,height:335,objectFit:'contain',filter:'brightness(0) invert(1)',opacity:progress,transform:`scale(${.94+.06*progress})`}}/>
 <div style={{position:'absolute',top:1010,left:0,right:0,textAlign:'center',color:'white',fontSize:58}}>iB Mídias</div>
 <div style={{position:'absolute',top:1130,left:140,right:140,height:146,background:G,borderRadius:28,display:'flex',alignItems:'center',justifyContent:'center',gap:30,color:B,fontSize:64,boxShadow:'0 18px 45px #00113866',transform:`scale(${1+.012*Math.sin(Math.min(local,3)*Math.PI)})`}}>SAIBA MAIS <span style={{fontSize:73}}>↗</span></div>
 <div style={{position:'absolute',top:1320,left:40,right:40,color:'white',textAlign:'center',fontSize:30}}>FALE COM NOSSA EQUIPE PELO WHATSAPP</div>
 </>}
 {group&&<div style={{position:'absolute',top:1470,left:50,right:50,height:120,display:'flex',alignItems:'center',justifyContent:'center'}}><div style={{display:'flex',gap:12,padding:'14px 24px',background:'white',border:`3px solid ${B}`,borderRadius:19,boxShadow:'0 7px 0 #001B5733',fontSize:group.fontSize,fontWeight:800,lineHeight:1.18,whiteSpace:'nowrap',transform:`scale(${.975+.025*ease((t-group.start)/.12)})`}}>{group.words.map((w,i)=><span key={i} style={{color:t>=w.start?B:'#8CA7E9',background:t>=w.start&&w.hot?G:'transparent',borderRadius:7,padding:'2px 4px'}}>{w.text.toLocaleUpperCase('pt-BR')}</span>)}</div></div>}
 <div style={{position:'absolute',top:1680,left:82,right:82,display:'flex',gap:12}}>{raw.scenes.map((scene,i)=><div key={i} style={{height:5,flex:1,borderRadius:3,background:t>=scene.start?(dark?G:B):(dark?'#36508C':'#CBD9F3')}}/>)}</div>
 </AbsoluteFill>
};
