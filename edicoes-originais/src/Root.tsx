import React from 'react';
import {Composition} from 'remotion';
import {Film} from './Film';
import {films} from './data';
export const Root=()=> <>{films.map((film:any)=><Composition key={film.id} id={'Film'+film.id.slice(0,2)} component={Film} durationInFrames={film.frames} width={1080} height={1920} fps={30} defaultProps={{film}}/>)}</>;
