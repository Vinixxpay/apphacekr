import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
const mode=process.argv[2]||'stills';const timeline=JSON.parse(fs.readFileSync('timings.json','utf8'));fs.mkdirSync('out',{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.tsx')});const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{
 const selected=mode==='stills'?timeline:timeline.filter(v=>v.id===Number(mode));
 for(const v of selected){
  const composition=await selectComposition({serveUrl,id:`Video0${v.id}Lavai`,puppeteerInstance:browser});
  if(mode==='stills'){
   for(const [j,t] of [1.7,Math.max(6,v.cues.intro-1),v.cues.intro+2.4,v.cues.price+1.5,Math.min(v.duration-.5,v.cues.receipt+1)].entries()){
    const f=Math.min(v.frames-1,Math.round(t*30));await renderStill({serveUrl,composition,frame:f,output:`out/v${v.id}-${j}.png`,imageFormat:'png',puppeteerInstance:browser});console.log('STILL',v.id,j,t);
   }
  }else{
   let last=-1;await renderMedia({serveUrl,composition,codec:'h264',crf:19,pixelFormat:'yuv420p',audioCodec:'aac',audioBitrate:'192k',concurrency:3,puppeteerInstance:browser,outputLocation:`out/video_0${v.id}_lavai.mp4`,onProgress:({progress})=>{const p=Math.floor(progress*10);if(p!==last){last=p;console.log('VIDEO',v.id,p*10+'%');}}});console.log('FINAL READY',v.id);
  }
 }
}finally{await browser.close({silent:true});}
