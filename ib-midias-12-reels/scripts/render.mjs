import fs from 'node:fs';import path from 'node:path';import {bundle} from '@remotion/bundler';import {openBrowser,selectComposition,renderMedia,renderStill} from '@remotion/renderer';
const mode=process.argv[2]||'stills';const ids=process.argv[3]?.split(',').map(Number);const tl=JSON.parse(fs.readFileSync('public/timings-aligned.json','utf8')).filter(v=>!ids||ids.includes(v.id));const cfg=JSON.parse(fs.readFileSync('campaign.json','utf8'));fs.mkdirSync('out',{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.tsx')});const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{for(const v of tl){const name=String(v.id).padStart(2,'0');const data=cfg.videos.find(c=>c.id===v.id);const output=`out/${data.slug}`;fs.mkdirSync(output,{recursive:true});const composition=await selectComposition({serveUrl,id:`Reel${name}`,puppeteerInstance:browser});
 if(mode==='all'||mode==='video'){
  if(fs.existsSync(`${output}/reel.mp4`)&&process.env.FORCE!=='1'){console.log('SKIP',name);continue;}
  let last=-1;await renderMedia({serveUrl,composition,codec:'h264',crf:19,pixelFormat:'yuv420p',audioCodec:'aac',audioBitrate:'192k',concurrency:3,puppeteerInstance:browser,outputLocation:`${output}/reel.mp4`,onProgress:({progress})=>{const p=Math.floor(progress*5);if(p!==last){last=p;console.log('REEL',name,p*20+'%')}}});console.log('COMPLETE',name);
 }else{
  const frames=mode==='all-stills'?v.scenes.map((s,i)=>Math.min(v.frames-1,Math.round((s.start+(i===v.scenes.length-1?.9:.7))*30))):[30,Math.round((v.scenes[Math.min(1,v.scenes.length-1)].start+.8)*30),Math.round(v.frames*.5),Math.round((v.scenes.at(-1).start+1)*30),v.frames-1];
  for(const [n,frame] of frames.entries()){await renderStill({serveUrl,composition,frame:Math.min(v.frames-1,frame),output:`${output}/still-${n}.jpg`,imageFormat:'jpeg',jpegQuality:92,puppeteerInstance:browser});}
  const cover=await selectComposition({serveUrl,id:`Cover${name}`,puppeteerInstance:browser});await renderStill({serveUrl,composition:cover,frame:0,output:`${output}/capa.jpg`,imageFormat:'jpeg',jpegQuality:95,puppeteerInstance:browser});console.log('STILLS',name);
 }
}}finally{await browser.close({silent:true});}
