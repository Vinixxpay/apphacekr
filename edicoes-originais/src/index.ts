import React from 'react';
import {registerRoot} from 'remotion';
import {Root,ReviewRoot} from './Root';
registerRoot(()=>React.createElement(React.Fragment,null,React.createElement(Root),React.createElement(ReviewRoot)));
