import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film';
import timeline from '../public/timeline.json';
registerRoot(()=> <Composition id="Cartoon" component={Film} fps={30} width={1080} height={1920} durationInFrames={timeline.frames}/>);
