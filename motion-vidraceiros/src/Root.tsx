import React from 'react';
import {Composition} from 'remotion';
import {Film} from './Film';
export const Root:React.FC=()=> <Composition id="IBMidias" component={Film} durationInFrames={1530} fps={30} width={1080} height={1920}/>;
