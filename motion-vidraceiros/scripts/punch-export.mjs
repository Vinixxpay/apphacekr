import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
fs.mkdirSync('out',{recursive:true});
const speed=1.12,fade=.08;
const narration=JSON.parse(fs.readFileSync('public/audio/narracao.json','utf8'));
const windows=narration.map(item=>[Math.max(0,item.start-.08),Math.min(42,item.start+item.spoken_seconds+.12)]);
const filters=[];
for(let i=0;i<6;i++){
 filters.push(`[0:v]trim=start=${windows[i][0]}:end=${windows[i][1]},setpts=(PTS-STARTPTS)/${speed},framerate=fps=60:interp_start=0:interp_end=255:scene=8,settb=1/60,format=yuv420p[v${i}]`);
 filters.push(`[0:a]atrim=start=${windows[i][0]}:end=${windows[i][1]},asetpts=PTS-STARTPTS,atempo=${speed}[a${i}]`);
}
let video='v0',audio='a0',duration=(windows[0][1]-windows[0][0])/speed;
for(let i=1;i<6;i++){
 const nextV=`vx${i}`,nextA=`ax${i}`;
 filters.push(`[${video}][v${i}]xfade=transition=fade:duration=${fade}:offset=${(duration-fade).toFixed(6)}[${nextV}]`);
 filters.push(`[${audio}][a${i}]acrossfade=d=${fade}:c1=tri:c2=tri[${nextA}]`);
 duration+=(windows[i][1]-windows[i][0])/speed-fade;video=nextV;audio=nextA;
}
const args=['-v','error','-y','-filter_complex_threads','2','-i','out/ib-midias-motion.mp4','-filter_complex',filters.join(';'),'-map',`[${video}]`,'-map',`[${audio}]`,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','60','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','192k','-t',duration.toFixed(6),'-movflags','+faststart','out/ib-midias-vidraceiros-intenso.mp4'];
const result=spawnSync('ffmpeg',args,{stdio:'inherit'});
if(result.error)throw result.error;
if(result.status!==0)process.exit(result.status??1);
console.log(`MP4 sem pausas: ${duration.toFixed(2)}s, 60fps, voz 12% mais rápida sem mudar o tom.`);
