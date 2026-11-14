import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film';
import timings from '../public/timings.json';
registerRoot(()=> <>{timings.map(v=><Composition key={v.id} id={`Video0${v.id}Lavai`} component={Film} defaultProps={{id:v.id}} width={1080} height={1920} fps={30} durationInFrames={v.frames}/>)}</>);
