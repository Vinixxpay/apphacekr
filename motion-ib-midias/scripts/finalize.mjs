import {spawnSync} from 'node:child_process';
const args=['-v','error','-y','-i','out/remotion-master.mp4','-vf','scale=in_color_matrix=bt601:out_color_matrix=bt709:in_range=pc:out_range=tv,format=yuv420p','-c:v','libx264','-preset','fast','-crf','18','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','copy','-t','45','-movflags','+faststart','out/ib-midias-motion.mp4'];
const result=spawnSync('ffmpeg',args,{stdio:'inherit'});
if(result.error)throw result.error;
if(result.status!==0)process.exit(result.status??1);
console.log('MP4 finalizado: H.264, 1080x1920, 30 fps, YUV420p/BT.709, AAC.');
