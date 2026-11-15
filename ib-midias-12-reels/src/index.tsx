import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film';
import timings from '../public/timings-aligned.json';
const Root=()=><>{timings.map(v=><React.Fragment key={v.id}><Composition id={`Reel${String(v.id).padStart(2,'0')}`} component={Film} durationInFrames={v.frames} fps={30} width={1080} height={1920} defaultProps={{id:v.id,cover:false}}/><Composition id={`Cover${String(v.id).padStart(2,'0')}`} component={Film} durationInFrames={1} fps={30} width={1080} height={1920} defaultProps={{id:v.id,cover:true}}/></React.Fragment>)}</>;
registerRoot(Root);
