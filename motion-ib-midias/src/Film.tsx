import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Audio, cancelRender, continueRender, delayRender, Easing, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';

const L='#C6FF00', W='#F6F7F3', M='#A9B0A7', BG='#090B0A';
const ease=Easing.bezier(.2,.8,.2,1);
const p=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:ease});
const enter=(f:number,at=0)=>({opacity:p(f,at,at+14),transform:`translateY(${(1-p(f,at,at+18))*45}px) scale(${.98+.02*p(f,at,at+18)})`,clipPath:`inset(${(1-p(f,at,at+16))*100}% 0 0 0)`});
const text:React.CSSProperties={margin:0,fontWeight:800,letterSpacing:'-0.055em',lineHeight:1.12};
const box:React.CSSProperties={position:'absolute',left:84,width:862};

function Icon({kind,size=64,color=L}:{kind:string;size?:number;color?:string}){
 return <svg width={size} height={size} viewBox="0 0 100 100" fill="none" stroke={color} strokeWidth="4.5" strokeLinecap="round" strokeLinejoin="round">
 {kind==='moto'?<><circle cx="23" cy="69" r="17"/><circle cx="78" cy="69" r="17"/><path d="M23 69l17-30 18 30H23m17-30h20l18 30M55 26h13l10 43M29 34h18M39 39l-8 16M27 78h30l7-8"/><path d="M37 42l9-8 14 6-5 12H39z" fill={color}/><rect x="40" y="54" width="15" height="11" rx="3" fill={color}/></>:kind==='pin'?<><path d="M50 91S20 62 20 37a30 30 0 0160 0c0 25-30 54-30 54z"/><circle cx="50" cy="36" r="10"/></>:kind==='pay'?<><rect x="9" y="23" width="82" height="57" rx="9"/><path d="M9 41h82M23 62h20"/></>:kind==='chat'?<><path d="M17 16h66v54H44L20 89V70h-3z"/><path d="M32 34h36M32 49h24"/></>:kind==='arrow'?<><path d="M14 50h70M58 23l27 27-27 27"/></>:<><path d="M20 50l21 21 40-43"/></>}
 </svg>;
}

const Tag:React.FC<{children:React.ReactNode}>=({children})=><div style={{display:'inline-flex',alignItems:'center',gap:14,fontSize:28,letterSpacing:'.12em',fontWeight:600,color:L,textTransform:'uppercase'}}><span style={{width:9,height:9,background:L,borderRadius:9}}/>{children}</div>;
const Mark:React.FC<{size?:number}>=({size=42})=><span style={{fontWeight:800,fontSize:size,letterSpacing:'-.065em'}}>iB <span style={{color:L}}>Mídias</span></span>;

function Background(){const f=useCurrentFrame();return <AbsoluteFill style={{background:BG}}>
 <AbsoluteFill style={{background:'radial-gradient(ellipse at 85% 16%, #22310e88, transparent 52%), radial-gradient(ellipse at 5% 90%, #18211c88, transparent 45%)'}}/>
 <AbsoluteFill style={{opacity:.16,backgroundImage:'linear-gradient(#53604b38 1px,transparent 1px),linear-gradient(90deg,#53604b38 1px,transparent 1px)',backgroundSize:'96px 96px',transform:`translateY(${f*.03%96}px)`}}/>
 <div style={{position:'absolute',left:84,right:134,top:169,height:1,background:'#ffffff25'}}/>
 <div style={{position:'absolute',left:84,top:102}}><Mark size={34}/></div>
 <div style={{position:'absolute',right:134,top:116,fontSize:20,letterSpacing:'.12em',color:M}}>LOJAS DE MOTOS</div>
 <div style={{position:'absolute',left:84,top:1515,width:862,height:3,background:'#ffffff16'}}><div style={{width:`${f/1349*100}%`,height:3,background:L}}/></div>
 </AbsoluteFill>}

function Scene({children}:{children:React.ReactNode}){const f=useCurrentFrame();return <AbsoluteFill style={{opacity:Math.min(p(f,0,8),1-p(f,9999,10000))}}>{children}</AbsoluteFill>}

function Hook(){const f=useCurrentFrame();const fade=1-p(f,60,80);return <Scene>
 <div style={{...box,top:246,...enter(f,3)}}><Tag>Para donos de lojas de motos</Tag></div>
 {['Qual o valor?','Ainda está disponível?'].map((v,i)=><div key={v} style={{position:'absolute',top:350+i*106,left:110+i*110,width:635,background:'#252b25',border:'1px solid #ffffff20',borderRadius:24,padding:'22px 28px',fontSize:36,color:W,opacity:p(f,9+i*14,22+i*14)*fade,transform:`translateX(${(1-p(f,9+i*14,26+i*14))*100+(1-fade)*(i?160:-160)}px)`,display:'flex',gap:18,alignItems:'center'}}><Icon kind="chat" size={37}/>{v}<span style={{marginLeft:'auto',color:'#75816e',fontSize:24}}>•••</span></div>)}
 <div style={{...box,top:650}}>
  <h1 style={{...text,fontSize:84,...enter(f,7)}}>Sua loja<br/>anuncia…</h1>
  <div style={{height:50}}/>
  <h2 style={{...text,fontSize:70,...enter(f,30)}}>mas o cliente só<br/>pergunta o preço<br/>e <span style={{color:L,display:'inline-block',transform:`scale(${1+.035*Math.sin(Math.min(1,p(f,54,90))*Math.PI)})`}}>some?</span></h2>
  <div style={{width:140*p(f,55,90),height:7,background:L,marginTop:36}}/>
 </div>
 </Scene>}

function Need(){const f=useCurrentFrame();return <Scene>
 <div style={{...box,top:250,...enter(f)}}><Tag>Mais direção para seus anúncios</Tag></div>
 <div style={{...box,top:400,display:'flex',gap:18}}>{[0,1,2].map((i)=><div key={i} style={{flex:1,height:100+80*p(f,4+i*6,30+i*6),border:'1px solid #c6ff0055',background:'#1b2415',borderRadius:52-28*p(f,4+i*6,30+i*6),padding:24,...enter(f,i*7)}}><Icon kind={f<15+i*6?'chat':i===0?'chat':i===1?'moto':'check'} size={48}/><div style={{marginTop:15,fontSize:29,fontWeight:600,color:L,opacity:p(f,20+i*6,36+i*6)}}>{['Contato','Interesse','Oportunidade'][i]}</div></div>)}</div>
 <div style={{...box,top:680}}><h1 style={{...text,fontSize:78,...enter(f,12)}}>Sua loja precisa de<br/><span style={{color:L}}>oportunidades<br/>reais de venda.</span></h1>
 <p style={{fontSize:49,lineHeight:1.3,color:M,marginTop:65,...enter(f,47)}}>E clareza sobre o<br/><span style={{color:W}}>retorno dos anúncios.</span></p></div>
 </Scene>}

function Brand(){const f=useCurrentFrame();return <Scene>
 <div style={{...box,top:250,...enter(f)}}><Tag>Especialização faz diferença</Tag></div>
 <div style={{...box,top:545,...enter(f,5)}}><Mark size={134}/><p style={{fontSize:58,lineHeight:1.2,fontWeight:600,color:W,marginTop:55}}>Anúncios para lojas<br/>e concessionárias<br/><span style={{color:L}}>de motos.</span></p></div>
 <svg style={{position:'absolute',left:84,top:1080}} width="862" height="260" viewBox="0 0 862 260"><path d="M-40 210H240Q320 210 370 135T520 60H900" fill="none" stroke="#39402f" strokeWidth="28"/><path d="M-40 210H240Q320 210 370 135T520 60H900" fill="none" stroke={L} strokeWidth="3" pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(f,10,95)}/><path d="M-40 210H240Q320 210 370 135T520 60H900" fill="none" stroke="#c6ff0044" strokeWidth="2" strokeDasharray="15 20"/></svg>
 <div style={{position:'absolute',left:84+520*p(f,20,105),top:1070-65*p(f,20,105),opacity:p(f,10,25)}}><Icon kind="moto" size={150}/></div>
 </Scene>}

function Strategy(){const f=useCurrentFrame();return <Scene>
 <div style={{...box,top:250,...enter(f)}}><Tag>Estratégia sob medida</Tag></div>
 <h1 style={{...box,...text,top:338,fontSize:76,...enter(f,3)}}>Campanhas<br/>pensadas para:</h1>
 {['Seu estoque.','Sua região.','Suas condições\nde pagamento.'].map((s,i)=><div key={s} style={{...box,top:575+i*180,height:156,background:'#171b17',border:`1px solid ${f>i*48+17?'#c6ff0066':'#ffffff11'}`,borderRadius:24,display:'flex',alignItems:'center',gap:29,padding:'0 34px',...enter(f,14+i*48)}}><Icon kind={['moto','pin','pay'][i]} size={68}/><span style={{fontSize:i===2?49:58,fontWeight:600,lineHeight:1.12,whiteSpace:'pre-line',letterSpacing:'-.035em'}}>{s}</span></div>)}
 <p style={{...box,top:1165,fontSize:48,lineHeight:1.2,fontWeight:600,color:L,...enter(f,173)}}>Para atrair quem tem<br/>interesse em comprar.</p>
 </Scene>}

function Tracking(){const f=useCurrentFrame();const phase=f<64?0:f<130?1:2;const lines=[<>Saiba quanto<br/><span style={{color:L}}>investiu.</span></>,<>Quantas conversas<br/><span style={{color:L}}>gerou.</span></>,<>E quais contatos<br/><span style={{color:L}}>avançaram.</span></>];const move=p(f,140,190);return <Scene>
 <div style={{...box,top:250,...enter(f)}}><Tag>Visibilidade da operação</Tag></div>
 <h1 style={{...box,...text,top:360,fontSize:75,...enter(f,[4,64,130][phase])}}>{lines[phase]}</h1>
 <div style={{...box,top:640,fontSize:27,color:M,letterSpacing:'.09em',...enter(f,15)}}>PAINEL ILUSTRATIVO</div>
 <div style={{...box,top:700,display:'flex',gap:15}}>{['Investimento','Conversas','Negociações'].map((s,i)=><div key={s} style={{flex:1,height:180,background:'#1b201b',border:'1px solid #ffffff22',borderRadius:22,padding:'30px 18px',...enter(f,15+i*10)}}><div style={{fontSize:30,fontWeight:600,color:M,letterSpacing:'-.04em'}}>{s}</div><div style={{fontSize:63,color:L,marginTop:6}}>—</div></div>)}</div>
 <div style={{...box,top:965,display:'flex',gap:46,...enter(f,90)}}>{['Novo contato','Em negociação'].map((s,i)=><div key={s} style={{width:408,height:300,border:'1px solid #ffffff22',borderRadius:24,padding:25,background:i?'#1d2714':'#141914'}}><div style={{fontSize:33,color:i?L:M,fontWeight:600,letterSpacing:'-.035em'}}>{s}</div><div style={{height:1,background:'#ffffff20',marginTop:23}}/></div>)}</div>
 <div style={{position:'absolute',left:110+move*452,top:1094,width:352,height:120,background:move>.9?L:'#293026',color:move>.9?BG:W,borderRadius:18,padding:24,display:'flex',alignItems:'center',gap:19,opacity:p(f,95,110),boxShadow:'0 18px 30px #0005'}}><Icon kind={move>.9?'check':'chat'} size={48} color={move>.9?BG:L}/><span style={{fontSize:33,fontWeight:600}}>Contato</span></div>
 <div style={{...box,top:1330,fontSize:35,lineHeight:1.25,color:M,...enter(f,130)}}>Acompanhamento junto à<br/><span style={{color:W}}>sua equipe comercial.</span></div>
 </Scene>}

function Benefits(){const f=useCurrentFrame();const items=[['Acompanhamento','próximo.'],['Resultados','transparentes.'],['Valor justo','pelo serviço.']];return <Scene>
 <div style={{...box,top:250,...enter(f)}}><Tag>O jeito iB Mídias</Tag></div>
 {items.map((s,i)=>{const at=i*45;const opacity=p(f,at,at+9)*(i<2?1-p(f,at+43,at+48):1);return <div key={s[0]} style={{...box,top:590,opacity,transform:`translateY(${(1-p(f,at,at+15))*35}px)`}}><div style={{width:100,height:100,borderRadius:28,display:'flex',alignItems:'center',justifyContent:'center',background:L,marginBottom:65}}><Icon kind="check" size={60} color={BG}/></div><h1 style={{...text,fontSize:i===1?76:78}}>{s[0]}<br/><span style={{color:L}}>{s[1]}</span></h1><div style={{width:150,height:6,background:L,marginTop:60}}/></div>})}
 </Scene>}

function CTA(){const f=useCurrentFrame();return <Scene>
 <div style={{...box,top:250,...enter(f)}}><Tag>Vamos olhar para sua operação?</Tag></div>
 <h1 style={{...box,...text,top:425,fontSize:80,...enter(f,3)}}>Onde sua loja<br/>está perdendo<br/><span style={{color:L}}>oportunidades?</span></h1>
 <p style={{...box,top:815,fontSize:49,fontWeight:600,lineHeight:1.3,color:W,...enter(f,18)}}>Preencha o formulário<br/>e agende uma conversa.</p>
 <div style={{...box,top:1060,height:170,padding:'28px 32px',borderRadius:25,background:L,color:BG,display:'flex',alignItems:'center',justifyContent:'space-between',gap:20,...enter(f,35)}}><span style={{fontSize:42,fontWeight:800,letterSpacing:'-.035em',lineHeight:1.2}}>QUERO UMA ANÁLISE<br/>DA MINHA LOJA</span><Icon kind="arrow" color={BG} size={65}/></div>
 <div style={{...box,top:1325,...enter(f,44)}}><Mark size={47}/><div style={{fontSize:31,color:M,marginTop:16,fontWeight:600}}>Anúncios para lojas de motos</div></div>
 </Scene>}

export const Film:React.FC=()=>{
 const [fontsHandle]=useState(()=>delayRender('Carregando fontes locais'));
 useEffect(()=>{
  Promise.all([600,800].map(weight=>new FontFace('Inter',`url('${staticFile(weight===600?'inter-semibold.woff2':'inter-extrabold.woff2')}')`,{weight:String(weight)}).load()))
   .then(fonts=>{fonts.forEach(font=>document.fonts.add(font));continueRender(fontsHandle);}).catch(cancelRender);
 },[fontsHandle]);
 const scenes:[React.FC,number,number][]=[[Hook,0,180],[Need,180,150],[Brand,330,150],[Strategy,480,240],[Tracking,720,240],[Benefits,960,150],[CTA,1110,240]];
 return <AbsoluteFill style={{fontFamily:'Inter, sans-serif',color:W}}>
 <style>{`@font-face{font-family:Inter;src:url('${staticFile('inter-semibold.woff2')}');font-weight:600}@font-face{font-family:Inter;src:url('${staticFile('inter-extrabold.woff2')}');font-weight:800}*{box-sizing:border-box}`}</style>
 <Background/>{scenes.map(([C,from,duration])=><Sequence key={from} from={from} durationInFrames={duration}><C/></Sequence>)}
 <Audio src={staticFile('audio/mix.wav')}/>
 </AbsoluteFill>
};
