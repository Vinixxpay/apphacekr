import React from 'react';import {Composition,registerRoot} from 'remotion';import {Film} from './Film';import timings from '../public/timings-aligned.json';
const Root=()=><>{timings.map(v=><React.Fragment key={v.id}><Composition id={`BlackFriday0${v.id}`} component={Film} fps={30} width={1080} height={1920} durationInFrames={v.frames} defaultProps={{id:v.id,cover:false}}/><Composition id={`Cover0${v.id}`} component={Film} fps={30} width={1080} height={1920} durationInFrames={1} defaultProps={{id:v.id,cover:true}}/></React.Fragment>)}</>;
registerRoot(Root);
