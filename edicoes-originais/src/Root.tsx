import React from 'react';
import {Composition} from 'remotion';
import {Film} from './Film';
import {films} from './data';
export const Root=()=> <>{films.map((film:any)=><Composition key={film.id} id={'Film'+film.id.slice(0,2)} component={Film} durationInFrames={film.frames} width={1080} height={1920} fps={30} defaultProps={{film}}/>)}</>;
import {reviewFilms,clientFilm} from './review-data';
import {Client} from './Client';
export const ReviewRoot=()=> <>{reviewFilms.map((film:any)=><Composition key={film.id} id={'Review'+film.id.slice(-4)} component={Film} durationInFrames={film.frames} width={1080} height={1000} fps={30} defaultProps={{film,graphicsOnly:true}}/>)}<Composition id="ReviewClient" component={Client} durationInFrames={clientFilm.frames} width={1080} height={1920} fps={30} defaultProps={{film:clientFilm}}/></>;
