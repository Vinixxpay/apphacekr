import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,Img,OffthreadVideo,staticFile,useCurrentFrame,Sequence,delayRender,continueRender} from 'remotion';
import {B,G,P,Illustration,ease} from './Illustrations';
import {edit} from './data';
export type Word={text:string;start:number;end:number;highlight?:boolean};
export type Scene={kind:string;start:number;end:number;title:string;cues:Record<string,number>};
const normalize=(s:string)=>s.toLocaleLowerCase('pt-BR').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9 ]/g,'');
const keyword=new Set(['vidraceiro','desconto','lucro','acabamento','confiar','whatsapp']);
export const Film=({stageOnly=false}:{stageOnly?:boolean})=>{
 const [fontHandle]=useState(()=>delayRender('Montserrat'));useEffect(()=>{document.fonts.load('800 56px Montserrat').then(()=>continueRender(fontHandle));},[fontHandle]);
 const frame=useCurrentFrame(),t=frame/30;
 const scene=edit.scenes.find(s=>t>=s.start&&t<s.end)||edit.scenes.at(-1)!;
 const group=edit.captions.find(c=>t>=c.start&&t<c.end);
 const local=t-scene.start;
 const previous=edit.scenes[edit.scenes.indexOf(scene)-1];
 const slide=scene.kind==='trust'&&local<.65;const travel=ease(local/.65);
 const cue=(s:string)=>scene.cues[s]??0;
 const dur=edit.frames/30;
 return <AbsoluteFill style={{background:stageOnly?'black':'white',fontFamily:'Montserrat',color:B}}>
  <style>{`@font-face{font-family:Montserrat;src:url('${staticFile('Montserrat.ttf')}') format('truetype');font-weight:100 900;font-display:block;}*{box-sizing:border-box}`}</style>
  {!stageOnly&&<><OffthreadVideo src={staticFile('video/presenter.mp4')} muted style={{position:'absolute',top:884,width:1080,height:1036}}/><Audio src={staticFile('video/voice.wav')}/><Audio src={staticFile('bed-original.wav')} loop volume={.045}/></>}
  <svg width={1080} height={934} viewBox="0 0 1080 934" style={{position:'absolute',top:0,left:0,overflow:'visible'}}>
   <defs><pattern id="grid" width={56} height={56} patternUnits="userSpaceOnUse"><path d="M56 0H0V56" stroke="#E6EFFF" fill="none" strokeWidth={1}/></pattern></defs>
   <path d="M0 0H1080V883L1048 897L1016 884L988 901L952 884L922 896L887 885L853 902L821 885L782 897L745 881L705 899L670 886L636 901L601 886L565 898L530 883L498 901L460 884L428 899L390 885L354 902L319 884L285 898L251 887L213 901L179 884L144 899L108 884L72 901L36 886L0 897Z" fill="white"/>
   <rect width={1080} height={879} fill="url(#grid)"/>
   <rect x={50} y={35} width={237} height={47} rx={23} fill={G}/><text x={168} y={67} fontSize={23} fontWeight={800} textAnchor="middle" fill={B}>VIDRAÇARIAS</text>
   <text x={1028} y={67} textAnchor="end" fontSize={22} fontWeight={800} fill={B}>iB MÍDIAS</text>
   <text x={540} y={133} textAnchor="middle" fill={B} fontSize={scene.title.length>31?35:39} fontWeight={800}>{scene.title}</text>
   {slide&&previous&&<g transform={`translate(${-1080*travel} 0)`}><Illustration kind={previous.kind} t={previous.end-previous.start} cue={s=>previous.cues[s]??0}/></g>}
   <g opacity={ease(local/.22)} transform={`translate(${slide?1080*(1-travel):0} ${8*(1-ease(local/.35))})`}><Illustration kind={scene.kind} t={local} cue={cue}/></g>
   {scene.kind==='cta'&&<image href={staticFile('logo.svg')} x={413} y={203} width={254} height={255} style={{filter:'brightness(0) invert(1)'}}/>}
   <g>{edit.scenes.map((s,i)=><rect key={i} x={450+i*27} y={854} width={18} height={5} rx={2} fill={t>=s.start?B:P}/>)}</g>
  </svg>
  {group&&<div style={{position:'absolute',top:850,left:32,right:32,height:106,display:'flex',alignItems:'center',justifyContent:'center'}}>
    <div style={{display:'flex',gap:12,alignItems:'center',padding:'13px 22px',background:'white',border:`3px solid ${B}`,borderRadius:18,boxShadow:'0 5px 0 rgba(1,49,205,.12)',whiteSpace:'nowrap',fontWeight:800,fontSize:group.words.map(w=>w.text).join(' ').length>25?46:56,lineHeight:1.18}}>
    {group.words.map((w,i)=>{const spoken=t>=w.start;const n=normalize(w.text);const hot=keyword.has(n)||w.highlight;return <span key={i} style={{display:'inline-block',color:spoken?B:'#8CA7E9',background:spoken&&hot?G:'transparent',borderRadius:7,padding:'2px 5px',transform:`scale(${spoken&&t-w.start<.14?1.025:1})`}}>{w.text.toLocaleUpperCase('pt-BR')}</span>})}
    </div>
  </div>}
  <div style={{position:'absolute',left:34,top:964,display:'flex',alignItems:'center',gap:11,background:'rgba(255,255,255,.96)',borderRadius:12,padding:'6px 13px 6px 9px',border:`2px solid ${B}`}}><Img src={staticFile('logo.svg')} style={{height:47,width:51,objectFit:'contain'}}/><span style={{fontSize:23,fontWeight:800,color:B}}>iB Mídias</span></div>
 </AbsoluteFill>
};
