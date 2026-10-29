import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';
const mode=process.argv[2]||'render';
fs.mkdirSync('out',{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts')});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{
 const ids=process.argv[3]?process.argv[3].split(','):['Film01','Film02','Film03','Film04'];
 for(const id of ids){
  const comp=await selectComposition({serveUrl,id,puppeteerInstance:browser});
  const film=comp.props.film;
  const patch=mode==='patch'||(mode==='finish'&&id==='Film01');
  const suffix=patch?'-patch':'';
  const patchStart=Math.round(film.segments.at(-1).from*30);
  if(mode==='still'){
   const frame=Math.min(comp.durationInFrames-1,Number(process.argv[4]||90));
   await renderStill({serveUrl,composition:comp,frame,output:`out/${film.id}-check.png`,imageFormat:'png',puppeteerInstance:browser});
   console.log(id,'captura concluída');continue;
  }
  let last=-1;
  await renderMedia({serveUrl,composition:comp,codec:'h264',pixelFormat:'yuv420p',audioCodec:'aac',audioBitrate:'192k',crf:19,concurrency:3,puppeteerInstance:browser,frameRange:patch?[patchStart,comp.durationInFrames-1]:undefined,outputLocation:`out/${film.id}${suffix}-master.mp4`,onProgress:({progress})=>{const now=Math.floor(progress*10);if(now!==last){last=now;console.log(id,`${now*10}%`);}}});
  const args=['-v','error','-y','-i',`out/${film.id}${suffix}-master.mp4`,'-vf','scale=in_color_matrix=bt601:out_color_matrix=bt709:in_range=pc:out_range=tv,format=yuv420p','-c:v','libx264','-preset','fast','-crf','18','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','copy','-movflags','+faststart',`out/${film.id}${suffix}.mp4`];
  const result=spawnSync('ffmpeg',args,{stdio:'inherit'});if(result.status!==0)throw new Error(`FFmpeg ${id}: ${result.status}`);
  if(patch){
   const join=spawnSync('ffmpeg',['-v','error','-y','-i',`out/${film.id}.mp4`,'-i',`out/${film.id}-patch.mp4`,'-filter_complex',`[0:v]trim=end_frame=${patchStart},setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]`,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',`out/${film.id}-joined.mp4`],{stdio:'inherit'});
   if(join.status!==0)throw new Error('Falha no acabamento do CTA');
   fs.renameSync(`out/${film.id}-joined.mp4`,`out/${film.id}.mp4`);
  }
  console.log(id,'MP4 finalizado');
 }
}finally{await browser.close({silent:true});}
