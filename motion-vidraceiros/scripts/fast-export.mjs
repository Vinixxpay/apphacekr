import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
fs.mkdirSync('out',{recursive:true});
const speed=1.12,fade=.18,times=[0,5,11,18,25,33,42];
const filters=[];
for(let i=0;i<6;i++){
 filters.push(`[0:v]trim=start=${times[i]}:end=${times[i+1]},setpts=(PTS-STARTPTS)/${speed},framerate=fps=60:interp_start=0:interp_end=255:scene=8,settb=1/60,format=yuv420p[v${i}]`);
 filters.push(`[0:a]atrim=start=${times[i]}:end=${times[i+1]},asetpts=PTS-STARTPTS,atempo=${speed}[a${i}]`);
}
let video='v0',audio='a0',duration=(times[1]-times[0])/speed;
for(let i=1;i<6;i++){
 const nextV=`vx${i}`,nextA=`ax${i}`;
 filters.push(`[${video}][v${i}]xfade=transition=fade:duration=${fade}:offset=${(duration-fade).toFixed(6)}[${nextV}]`);
 filters.push(`[${audio}][a${i}]acrossfade=d=${fade}:c1=tri:c2=tri[${nextA}]`);
 duration+=(times[i+1]-times[i])/speed-fade;video=nextV;audio=nextA;
}
const args=['-v','error','-y','-filter_complex_threads','2','-i','out/ib-midias-motion.mp4','-filter_complex',filters.join(';'),'-map',`[${video}]`,'-map',`[${audio}]`,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','60','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','192k','-t',duration.toFixed(6),'-movflags','+faststart','out/ib-midias-vidraceiros-dinamico.mp4'];
const result=spawnSync('ffmpeg',args,{stdio:'inherit'});
if(result.error)throw result.error;
if(result.status!==0)process.exit(result.status??1);
console.log(`MP4 dinâmico: ${duration.toFixed(2)}s, 60fps, voz 12% mais rápida sem mudar o tom.`);
