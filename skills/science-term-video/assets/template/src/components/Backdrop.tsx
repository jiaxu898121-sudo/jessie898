import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {COLOR} from '../theme';

// 远层：深蓝灰底 + 极缓慢漂移的柔光 + 一道地平弧。不做密集粒子、不做强光晕。
const DUST = [
  {x: 300, y: 620, r: 2.4, sp: 0.055, ph: 0},
  {x: 640, y: 300, r: 1.7, sp: 0.04, ph: 1.7},
  {x: 900, y: 210, r: 1.6, sp: 0.048, ph: 3.1},
  {x: 1240, y: 330, r: 2.0, sp: 0.035, ph: 4.4},
  {x: 1520, y: 240, r: 1.8, sp: 0.045, ph: 2.2},
  {x: 1780, y: 430, r: 2.2, sp: 0.05, ph: 5.6},
  {x: 260, y: 860, r: 1.9, sp: 0.03, ph: 0.9},
  {x: 1740, y: 800, r: 2.5, sp: 0.038, ph: 3.8},
];

export const Backdrop: React.FC = () => {
  const frame = useCurrentFrame();

  const driftX = Math.sin(frame / 130) * 16;
  const driftY = Math.cos(frame / 170) * 10;
  const coolX = Math.cos(frame / 150) * 12;

  return (
    <AbsoluteFill style={{backgroundColor: COLOR.bgDeep}}>
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(1500px 980px at 54% 38%, #2A3947 0%, #1E2A36 46%, #141E27 100%)',
        }}
      />

      {/* 暖层柔光：压在角色身后的中景，不抢主句的注意力 */}
      <div
        style={{
          position: 'absolute',
          left: 1120 + driftX,
          top: 180 + driftY,
          width: 980,
          height: 980,
          borderRadius: '50%',
          background:
            'radial-gradient(circle, rgba(227,184,124,0.075) 0%, rgba(227,184,124,0) 60%)',
        }}
      />

      {/* 冷层柔光：托住中景概念图形 */}
      <div
        style={{
          position: 'absolute',
          left: 520 + coolX,
          top: 300,
          width: 1000,
          height: 700,
          borderRadius: '50%',
          background:
            'radial-gradient(circle, rgba(150,190,210,0.055) 0%, rgba(150,190,210,0) 66%)',
        }}
      />

      {/* 地平面：一个大椭圆的内部就是地面，顶边成为地平弧。
          给角色一个真实站立的位置，而不是浮在黑底上。 */}
      <svg
        width={1920}
        height={1080}
        style={{position: 'absolute', left: 0, top: 0}}
      >
        <defs>
          <linearGradient id="floorGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={COLOR.warmWhite} stopOpacity="0.012" />
            <stop offset="45%" stopColor={COLOR.warmWhite} stopOpacity="0.032" />
            <stop offset="100%" stopColor={COLOR.warmWhite} stopOpacity="0.055" />
          </linearGradient>
          <linearGradient id="floorLine" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor={COLOR.gold} stopOpacity="0" />
            <stop offset="22%" stopColor={COLOR.gold} stopOpacity="0.20" />
            <stop offset="64%" stopColor={COLOR.gold} stopOpacity="0.30" />
            <stop offset="100%" stopColor={COLOR.gold} stopOpacity="0.12" />
          </linearGradient>
        </defs>
        <ellipse cx="1560" cy="1600" rx="1400" ry="740" fill="url(#floorGrad)" />
        <ellipse
          cx="1560"
          cy="1600"
          rx="1400"
          ry="740"
          fill="none"
          stroke="url(#floorLine)"
          strokeWidth={1.8}
        />
        {/* 第二道更宽更淡的地平线，制造浅景深的层次 */}
        <ellipse
          cx="1560"
          cy="1660"
          rx="1520"
          ry="760"
          fill="none"
          stroke="rgba(246,241,231,0.055)"
          strokeWidth={1.2}
        />
      </svg>

      {/* 微尘：8 颗，极慢上浮，透明度 0.10–0.20 */}
      <svg
        width={1920}
        height={1080}
        style={{position: 'absolute', left: 0, top: 0}}
      >
        {DUST.map((d, i) => {
          const rise = (frame * d.sp + d.ph * 30) % 220;
          const op = interpolate(rise, [0, 60, 160, 220], [0, 0.2, 0.16, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const sway = Math.sin(frame / 90 + d.ph) * 5;
          return (
            <circle
              key={i}
              cx={d.x + sway}
              cy={d.y - rise}
              r={d.r}
              fill={COLOR.warmWhite}
              opacity={op}
            />
          );
        })}
      </svg>

      {/* 顶部与底部压边，把注意力收到中间带 */}
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(to bottom, rgba(10,16,22,0.36) 0%, rgba(10,16,22,0) 24%, rgba(10,16,22,0) 70%, rgba(10,16,22,0.34) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
