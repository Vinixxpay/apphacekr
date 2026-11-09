import React from 'react';
import {registerRoot,Composition} from 'remotion';
import {Film} from './Film';
import {edit} from './data';
const Root=()=> <><Composition id="VidracariasVideo2" component={Film} fps={30} width={1080} height={1920} durationInFrames={edit.frames}/><Composition id="Stage" component={Film} fps={30} width={1080} height={1080} durationInFrames={edit.frames} defaultProps={{stageOnly:true}}/></>;
registerRoot(Root);
