import React from 'react';
import {staticFile} from 'remotion';
export const INK='#071321',BLUE='#FFB300',LIME='#FFB300',SKIN='#EDBC8C';
export const T=({x,y,size=34,fill=INK,children,anchor='middle'}:{x:number;y:number;size?:number;fill?:string;children:React.ReactNode;anchor?:'middle'|'start'|'end'})=><text x={x} y={y} textAnchor={anchor} fontFamily="Montserrat" fontSize={size} fontWeight={800} fill={fill} stroke="none">{children}</text>;
export const Coin=({x,y,s=1}:{x:number;y:number;s?:number})=><g transform={`translate(${x} ${y}) scale(${s})`} stroke={INK} strokeWidth={7}><ellipse ry={26} rx={45} cy={12} fill="#C89024"/><ellipse ry={26} rx={45} fill="#F7CE5A"/><path d="M-17 0h34" strokeWidth={5}/></g>;
export const Hero=({x,y,s=1,t=0,mouth=0,emotion='happy',pose='calm',woman=false,shirt=BLUE,look=0,brand=false,run=false,skin=SKIN,cap=false,cleanShaven=false}:{x:number;y:number;s?:number;t?:number;mouth?:number;emotion?:string;pose?:string;woman?:boolean;shirt?:string;look?:number;brand?:boolean;run?:boolean;skin?:string;cap?:boolean;cleanShaven?:boolean})=>{
 const bob=run?-Math.abs(Math.sin(t*10))*18:Math.sin(t*2.8)*3,blink=t%3.2>3.04;const worried=emotion==='worried'||emotion==='tired';
 const r=pose==='point'?{x:235,y:50+Math.sin(t*5)*9}:pose==='work'?{x:220,y:320+Math.sin(t*6)*25}:pose==='shrug'?{x:242,y:190+Math.sin(t*4)*12}:pose==='phone'?{x:200,y:195}:{x:170,y:380};
 const l=pose==='work'?{x:-180,y:345}:pose==='shrug'?{x:-240,y:190}:pose==='point'?{x:-170,y:370}:{x:-168,y:385};
 return <g transform={`translate(${x} ${y+bob}) scale(${s})`} stroke={INK} strokeWidth={11} strokeLinecap="round" strokeLinejoin="round">
 <ellipse cx={0} cy={665} rx={150} ry={24} fill="#1B2132" opacity={.15} stroke="none"/>
 {run?<><path d={`M-63 457q${Math.sin(t*10)*100} 95 ${Math.sin(t*10)*120-12} 186M63 457q${-Math.sin(t*10)*100} 95 ${-Math.sin(t*10)*120+14} 186`} stroke="#3B4654" strokeWidth={32}/><g transform={`translate(${Math.sin(t*10)*120} 0)`}><path d="M-115 646h75v28h-88q-15-12 13-28" fill={INK}/></g><g transform={`translate(${-Math.sin(t*10)*120} 0)`}><path d="M37 646h77q28 16 11 28H37Z" fill={INK}/></g></>:<><path d="M-63 457l-12 186M63 457l14 186" stroke="#3B4654" strokeWidth={32}/><path d="M-115 646h75v28h-88q-15-12 13-28M37 646h77q28 16 11 28H37Z" fill={INK}/></>}
 <path d={`M-104 200Q-170 235 ${l.x} ${l.y}M104 200Q190 260 ${r.x} ${r.y}`} fill="none" strokeWidth={22}/>
 <path d="M-102 175q-43 15-50 74M102 175q42 15 48 69" fill="none" stroke={shirt} strokeWidth={58}/>
 <ellipse cx={l.x} cy={l.y} rx={25} ry={28} fill={skin}/><ellipse cx={r.x} cy={r.y} rx={25} ry={28} fill={skin}/>
 {pose==='point'&&<path d={`M${r.x+4} ${r.y-14}l-4-58q0-22 15-11l5 65`} fill={skin} strokeWidth={8}/>}
 <path d="M-101 158Q-139 185-127 316l14 157Q0 505 113 473l13-157q13-131-27-158Z" fill={shirt}/>
 {woman?<path d="M-106 350l-40 166q143 39 292 0l-40-166" fill={shirt}/>:<><rect x={-126} y={406} width={252} height={51} rx={10} fill="#34414E"/><rect x={-19} y={412} width={43} height={39} rx={5} fill="#FFB300"/><g transform="translate(70 438)"><rect x="0" y="20" width="44" height="65" rx="10" fill="#FFB300" stroke="#071321" strokeWidth="6"/><path d="M13 20V5h35v10H30v5" fill="#FFFFFF" stroke="#071321" strokeWidth="5"/></g></>}
 <path d="M-35 158l35 39 35-39" fill="none" stroke="#F7FAFE" strokeWidth={9}/>
 {brand&&<image href={staticFile('logo-lavai.png')} x={-43} y={238} width={86} height={74} />}
 {pose==='phone'&&<g transform={`translate(${r.x-45} ${r.y-127}) rotate(-8)`}><rect width={86} height={155} rx={17} fill="#263A5E"/><rect x={11} y={20} width={64} height={110} rx={5} fill={LIME}/></g>}
 {woman&&<path d="M-153-53q-15-146 154-143 170-9 164 153l14 248q-46 36-68-2H-103q-36 38-72-5Z" fill="#69412D"/>}
 <ellipse cx={-151} cy={10} rx={28} ry={35} fill={skin}/><ellipse cx={151} cy={10} rx={28} ry={35} fill={skin}/>
 <ellipse cx={0} cy={0} rx={151} ry={154} fill={skin}/>
 {woman?<path d="M-148-18q-42-178 124-169 170-25 179 165-56-5-88-81-59 69-215 85Z" fill="#69412D"/>:<><path d="M-149-12q-32-137 102-155-7-39 24-30 90 2 131 79 62 22 42 115-26-63-74-71-69 39-148 20-49 24-77 42Z" fill="#4B302E"/>{!cleanShaven&&<path d="M-131 65q8 96 128 108 124-10 136-109-32 24-60 31-72-34-138 0-34-7-66-30Z" fill="#67402F" strokeWidth={7}/>}</>}
 {cap&&<g><path d="M-157-80q0-148 145-143 130 0 163 133Z" fill="#FFB300"/><path d="M-157-80q175-40 365-5l-12 31q-174-26-349-3Z" fill="#FFB300"/></g>}
 <g transform={`translate(0 -2) scale(1 ${blink?.10:emotion==='tired'?.72:1})`}><ellipse cx={-57} rx={34} ry={40} fill="white" strokeWidth={8}/><ellipse cx={57} rx={34} ry={40} fill="white" strokeWidth={8}/><ellipse cx={-57+look} cy={2} rx={13} ry={18} fill={INK} stroke="none"/><ellipse cx={57+look} cy={2} rx={13} ry={18} fill={INK} stroke="none"/></g>
 <path d={worried?'M-94-62l63 17M31-45l64-17':'M-92-62l62-7M31-69l62 7'} strokeWidth={12}/>
 <path d="M-3 16l-11 28h20" fill="none" strokeWidth={6}/>
 {mouth>.15?<g><path d={`M-43 73Q0 84 43 73Q43 ${87+mouth*30} 0 ${98+mouth*30}Q-43 ${87+mouth*30}-43 73Z`} fill="#52233A" strokeWidth={7}/><path d="M-28 82q28 8 56 0" fill="none" stroke="white" strokeWidth={11}/></g>:worried?<path d="M-35 104q35-33 70 0" fill="none" strokeWidth={8}/>:<path d="M-52 80Q0 99 52 80Q46 124 0 130-46 124-52 80Z" fill="white" strokeWidth={8}/>}
 </g>
};

export const Owner=({id,...props}:React.ComponentProps<typeof Hero>&{id:number})=><Hero {...props} woman={id===2} skin={id===1?'#D4A174':id===2?'#E1AE80':'#F0C294'} shirt={id===2?'#FFFFFF':id===3?'#344451':'#FFB300'} cap={id===3} cleanShaven={id===3}/>;
