import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
const mode=process.argv[2]||'full';fs.mkdirSync('out',{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.tsx')});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{
 const composition=await selectComposition({serveUrl,id:'AltoValor',puppeteerInstance:browser});
 if(mode==='stills'){
  const timeline=JSON.parse(fs.readFileSync('timeline.json','utf8'));
  for(let i=0;i<timeline.scenes.length;i++){
   const s=timeline.scenes[i];const f=Math.round((s.start+Math.min(2.2,s.speechDuration*.55))*30);
   await renderStill({serveUrl,composition,frame:f,output:`out/scene-${i}.png`,imageFormat:'png',puppeteerInstance:browser});console.log('STILL',i,f);
  }
 }else{
  let last=-1;
  await renderMedia({serveUrl,composition,codec:'h264',crf:19,pixelFormat:'yuv420p',audioCodec:'aac',audioBitrate:'192k',concurrency:4,puppeteerInstance:browser,outputLocation:'out/ib-midias-alto-valor.mp4',onProgress:({progress})=>{const p=Math.floor(progress*10);if(p!==last){last=p;console.log('RENDER',p*10+'%');}}});
  console.log('FINAL MP4 READY');
 }
}finally{await browser.close({silent:true});}
