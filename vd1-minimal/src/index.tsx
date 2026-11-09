import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,Composition,Img,OffthreadVideo,continueRender,delayRender,registerRoot,staticFile} from 'remotion';
import {config} from './config';
const B='#0131CD',G='#B9FC01';
export const Brand=()=>{
 const [handle]=useState(()=>delayRender('Montserrat'));useEffect(()=>{document.fonts.load('800 24px Montserrat').then(()=>continueRender(handle));},[handle]);
 return <AbsoluteFill style={{background:'transparent',fontFamily:'Montserrat'}}><style>{`@font-face{font-family:Montserrat;src:url('${staticFile('Montserrat.ttf')}');font-weight:100 900;}`}</style><div style={{position:'absolute',inset:2,background:'#FFFFFF',border:`2px solid ${B}`,borderRadius:14,display:'flex',alignItems:'center',padding:'10px 13px',gap:11,overflow:'hidden'}}><Img src={staticFile('logo.svg')} style={{height:53,width:63,objectFit:'contain'}}/><span style={{fontSize:25,fontWeight:800,color:B,whiteSpace:'nowrap'}}>iB Mídias</span><div style={{position:'absolute',right:0,top:12,bottom:12,width:5,borderRadius:3,background:G}}/></div></AbsoluteFill>;
};
const Film=()=> <AbsoluteFill style={{background:'white'}}><OffthreadVideo src={staticFile('video/picture.mp4')} muted style={{width:1080,height:1920}}/><Audio src={staticFile('video/voice.wav')}/><Audio src={staticFile('bed-original.wav')} loop volume={.025}/><div style={{position:'absolute',left:54,top:144,width:254,height:82}}><Brand/></div></AbsoluteFill>;
const Root=()=> <><Composition id="VD1" component={Film} durationInFrames={config.frames} fps={30} width={1080} height={1920}/><Composition id="Brand" component={Brand} durationInFrames={1} fps={30} width={254} height={82}/></>;
registerRoot(Root);
