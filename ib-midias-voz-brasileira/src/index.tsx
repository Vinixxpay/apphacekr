import React from 'react';
import {registerRoot,Composition} from 'remotion';
import {Film} from './Film';
import timeline from '../public/timeline.json';
registerRoot(()=> <Composition id="ReelsProjetos" component={Film} width={1080} height={1920} fps={30} durationInFrames={timeline.frames}/>);
