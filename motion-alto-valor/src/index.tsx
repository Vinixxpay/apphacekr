import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film';
import timeline from '../public/timeline.json';
const Root=()=> <Composition id="AltoValor" component={Film} durationInFrames={timeline.frames} fps={30} width={1080} height={1920}/>;
registerRoot(Root);
