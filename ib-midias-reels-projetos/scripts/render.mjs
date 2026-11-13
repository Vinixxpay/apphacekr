import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
const mode=process.argv[2]||'full';fs.mkdirSync('out',{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.tsx')});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{
 const composition=await selectComposition({serveUrl,id:'ReelsProjetos',puppeteerInstance:browser});
 if(mode==='stills'){
  const timeline=JSON.parse(fs.readFileSync('timeline.json','utf8'));
  for(let i=0;i<timeline.scenes.length;i++){
   const sc=timeline.scenes[i];const offsets=sc.kind==='agency'?[1.0,5.2,8.4]:sc.kind==='cta'?[2.1,5.2,9.8]:sc.kind==='value'?[1.8,5.2,8.6]:sc.kind==='search'?[1.2,4.2,7.4]:[1.1,Math.min(sc.speechDuration-.2,4.5)];
   for(let j=0;j<offsets.length;j++){
    const f=Math.round((sc.start+offsets[j])*30);
    await renderStill({serveUrl,composition,frame:f,output:`out/scene-${i}-${j}.png`,imageFormat:'png',puppeteerInstance:browser});console.log('STILL',i,j,f);
   }
  }
 }else{
  let last=-1;
  await renderMedia({serveUrl,composition,codec:'h264',crf:19,pixelFormat:'yuv420p',audioCodec:'aac',audioBitrate:'192k',concurrency:4,puppeteerInstance:browser,outputLocation:'out/ib-midias-reels-projetos.mp4',onProgress:({progress})=>{const p=Math.floor(progress*10);if(p!==last){last=p;console.log('RENDER',p*10+'%');}}});
  console.log('FINAL MP4 READY');
 }
}finally{await browser.close({silent:true});}
