import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,staticFile,useCurrentFrame,delayRender,continueRender} from 'remotion';
import timeline from '../public/timeline.json';
import captions from '../public/captions.json';
import mouth from '../public/mouth.json';
import {Scene} from './Scenes';
export const Film=()=>{
 const [handle]=useState(()=>delayRender('Cartoon fonts'));useEffect(()=>{Promise.all([document.fonts.load('800 64px Montserrat'),document.fonts.load('800 80px StorySerif')]).then(()=>continueRender(handle))},[handle]);
 const f=useCurrentFrame(),t=f/30,s=timeline.scenes.find(s=>t>=s.start&&t<s.end)||timeline.scenes[0];const group=captions.find(c=>t>=c.start&&t<c.end);
 return <AbsoluteFill style={{background:'#AEC9D9',overflow:'hidden'}}>
 <style>{`@font-face{font-family:Montserrat;src:url('${staticFile('fonts/Montserrat-ExtraBold.ttf')}');font-weight:800}@font-face{font-family:StorySerif;src:url('${staticFile('fonts/StorySerif.ttf')}');font-weight:800}*{box-sizing:border-box}`}</style>
 <Audio src={staticFile('audio/mix.wav')}/><Scene kind={s.kind} t={Math.max(0,t-s.start)} mouth={mouth[f]||0}/>
 <AbsoluteFill style={{pointerEvents:'none',backgroundImage:`url('${staticFile('paper.png')}')`,backgroundRepeat:'repeat',opacity:.09,mixBlendMode:'multiply'}}/>
 {group&&<div style={{position:'absolute',top:180,left:55,right:55,minHeight:220,display:'flex',alignItems:'center',justifyContent:'center'}}><div style={{fontFamily:'StorySerif',fontWeight:800,fontSize:80,lineHeight:1.13,textAlign:'center',color:'white',maxWidth:950,WebkitTextStroke:'3px #292139',paintOrder:'stroke fill',textShadow:'0 7px 1px #292139, 3px 0 1px #292139, -3px 0 1px #292139',transform:`scale(${.98+.02*Math.min(1,(t-group.start)/.1)})`}}>{group.words.map(w=>w.text).join(' ')}</div></div>}
 </AbsoluteFill>
};
