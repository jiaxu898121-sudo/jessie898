import React from 'react';
import {AbsoluteFill,Composition} from 'remotion';
import {StandaloneScene} from './Scene';
export const RemotionRoot=()=> <Composition id="Template" component={StandaloneScene} defaultProps={{index:1}} width={1920} height={1080} fps={30} durationInFrames={180}/>;
