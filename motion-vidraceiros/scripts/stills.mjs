import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderStill} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';
fs.mkdirSync('out',{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts')});
const browser=await openBrowser('chrome',{browserExecutable:process.env.CHROME_BIN||'/usr/bin/chromium'});
try {
 const composition=await selectComposition({serveUrl,id:'IBMidias',puppeteerInstance:browser});
 const frames=[90,270,510,750,960,1170,1410];
 for (let i=0;i<frames.length;i++){
  await renderStill({serveUrl,composition,frame:frames[i],output:`out/scene-${i+1}.png`,imageFormat:'png',puppeteerInstance:browser});
  console.log(`Cena ${i+1}: quadro ${frames[i]} exportado`);
 }
} finally {await browser.close({silent:true});}
