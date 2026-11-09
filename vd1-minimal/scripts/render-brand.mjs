import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderStill} from '@remotion/renderer';
import path from 'node:path';
const serveUrl=await bundle({entryPoint:path.resolve('src/index.tsx')});const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{const composition=await selectComposition({serveUrl,id:'Brand',puppeteerInstance:browser});await renderStill({serveUrl,composition,frame:0,output:'public/brand.png',imageFormat:'png',puppeteerInstance:browser});console.log('BRAND READY');}finally{await browser.close({silent:true});}
