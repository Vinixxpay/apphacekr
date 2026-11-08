import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';
const mode=process.argv[2]||'preview';fs.mkdirSync('out',{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.tsx')});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{
 const composition=await selectComposition({serveUrl,id:'Stage',puppeteerInstance:browser});
 if(mode==='still'){
  for(const frame of [35,180,255,420,1000,1450,1750,2100]){
   await renderStill({serveUrl,composition,frame,output:`out/check-${frame}.png`,imageFormat:'png',puppeteerInstance:browser});console.log('Still',frame);
  }
 }else{
  let last=-1;await renderMedia({serveUrl,composition,codec:'h264',crf:17,pixelFormat:'yuv420p',concurrency:2,puppeteerInstance:browser,frameRange:mode==='preview'?[0,299]:undefined,outputLocation:`out/stage-${mode}.mp4`,onProgress:({progress})=>{let p=Math.floor(progress*10);if(last!==p){last=p;console.log(mode,p*10+'%');}}});
 }
}finally{await browser.close({silent:true});}
