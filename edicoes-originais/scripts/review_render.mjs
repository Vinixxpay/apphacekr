import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
fs.mkdirSync('out/review',{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts')});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{
 const ids=process.argv[3]?process.argv[3].split(','):['ReviewClient','Review2203','Review2200','Review2197','Review2196'];
 for(const id of ids){
  const c=await selectComposition({serveUrl,id,puppeteerInstance:browser});
  if(process.argv[2]==='still'){
   await renderStill({serveUrl,composition:c,frame:Math.min(90,c.durationInFrames-1),output:`out/review/${id}-check.png`,imageFormat:'png',puppeteerInstance:browser});console.log(id,'captura concluída');continue;
  }
  if(fs.existsSync(`out/review/${id}-master.mp4`))continue;
  let last=-1;
  await renderMedia({serveUrl,composition:c,codec:'h264',pixelFormat:'yuv420p',audioCodec:'aac',audioBitrate:'192k',crf:19,concurrency:2,puppeteerInstance:browser,outputLocation:`out/review/${id}-master.mp4`,onProgress:({progress})=>{const n=Math.floor(progress*10);if(n!==last){last=n;console.log(id,`${n*10}%`)}}});
  console.log(id,'render completo');
 }
}finally{await browser.close({silent:true});}
