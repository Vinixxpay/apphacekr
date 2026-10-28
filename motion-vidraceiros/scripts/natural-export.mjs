import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
fs.mkdirSync('out',{recursive:true});
const remux=spawnSync('ffmpeg',['-v','error','-y','-i','out/ib-midias-motion.mp4','-i','public/audio/mix.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t','51','-movflags','+faststart','out/ib-midias-natural-base.mp4'],{stdio:'inherit'});
if(remux.error)throw remux.error;
if(remux.status!==0)process.exit(remux.status??1);
const speed=1.0,fade=.10;
const narration=JSON.parse(fs.readFileSync('public/audio/narracao.json','utf8'));
const windows=narration.map(item=>[Math.max(0,item.start-.16),Math.min(51,item.start+item.spoken_seconds+.24)]);
const filters=[];
for(let i=0;i<narration.length;i++){
 filters.push(`[0:v]trim=start=${windows[i][0]}:end=${windows[i][1]},setpts=(PTS-STARTPTS)/${speed},framerate=fps=60:interp_start=0:interp_end=255:scene=8,settb=1/60,format=yuv420p[v${i}]`);
 filters.push(`[0:a]atrim=start=${windows[i][0]}:end=${windows[i][1]},asetpts=PTS-STARTPTS[a${i}]`);
}
let video='v0',audio='a0',duration=(windows[0][1]-windows[0][0])/speed;
for(let i=1;i<narration.length;i++){
 const nextV=`vx${i}`,nextA=`ax${i}`;
 filters.push(`[${video}][v${i}]xfade=transition=fade:duration=${fade}:offset=${(duration-fade).toFixed(6)}[${nextV}]`);
 filters.push(`[${audio}][a${i}]acrossfade=d=${fade}:c1=tri:c2=tri[${nextA}]`);
 duration+=(windows[i][1]-windows[i][0])/speed-fade;video=nextV;audio=nextA;
}
const args=['-v','error','-y','-filter_complex_threads','2','-i','out/ib-midias-natural-base.mp4','-filter_complex',filters.join(';'),'-map',`[${video}]`,'-map',`[${audio}]`,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','60','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','192k','-t',duration.toFixed(6),'-movflags','+faststart','out/ib-midias-vidraceiros-voz-natural.mp4'];
const result=spawnSync('ffmpeg',args,{stdio:'inherit'});
if(result.error)throw result.error;
if(result.status!==0)process.exit(result.status??1);
console.log(`MP4 sem pausas: ${duration.toFixed(2)}s, 60fps, narração sem aceleração nem compressão temporal.`);
