import React from 'react';
import {COLOR} from '../theme';

export type HatVariant = 'A' | 'B';

export type CharacterSoftProps = {
  /** A：圆顶软帽，顶部轻微偏斜；B：短垂尖软帽，帽尖贴近帽体自然下垂 */
  hat: HatVariant;
  /** 左臂角度（0=自然下垂，正值为向观者左侧抬起） */
  armL: number;
  armR: number;
  /** 头部倾角，负值向左侧（看向概念图形） */
  headTilt: number;
  /** 眼球横移，负值向左看 */
  look: number;
  /** 0=闭眼，1=睁眼 */
  blink: number;
  /** 呼吸位移 px */
  breathe: number;
  /** 头部横向位移（单位同本地坐标），用于表达转头而非单纯歪头 */
  headShift?: number;
  /** 帽子动作跟随（后续动画用，静帧为 0） */
  hatLag?: number;
};

/**
 * 角色 v2「安静的小体块」。
 * 本地坐标 200×258，脚底正好落在 y=258，帽顶在 y=0，因此外部按“可见高度”等比缩放即可。
 *
 * 设计约束（A/B 共用）：
 * - 无嘴、无腮红、无眉毛、无鼻子、无睫毛；只有两个小而简洁的深色眼睛。
 * - 头大身短，四肢短而简洁，无胸前缝线、无外套翻领。
 * - 哑光色块 + 单向柔和明暗，无高光斑、无塑料反光。
 * - A/B 仅在帽子路径上不同，其余像素完全一致。
 */
export const CharacterSoft: React.FC<CharacterSoftProps> = ({
  hat,
  armL,
  armR,
  headTilt,
  look,
  blink,
  breathe,
  headShift = 0,
  hatLag = 0,
}) => {
  const uid = hat === 'A' ? 'ha' : 'hb';
  const SLEEVE = '#42586F';

  return (
    <svg viewBox="0 0 200 258" width="100%" height="100%">
      <defs>
        <radialGradient id={`${uid}-shadow`} cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#070C12" stopOpacity="0.42" />
          <stop offset="100%" stopColor="#070C12" stopOpacity="0" />
        </radialGradient>
        {/* 帽子：自上而下的单向柔和明暗，哑光，不做高光斑 */}
        <linearGradient
          id={`${uid}-hat`}
          gradientUnits="userSpaceOnUse"
          x1="0"
          y1="0"
          x2="0"
          y2="95"
        >
          <stop offset="0%" stopColor="#C4556A" />
          <stop offset="58%" stopColor="#B4475B" />
          <stop offset="100%" stopColor="#9E3A4C" />
        </linearGradient>
        <linearGradient
          id={`${uid}-body`}
          gradientUnits="userSpaceOnUse"
          x1="0"
          y1="136"
          x2="0"
          y2="230"
        >
          <stop offset="0%" stopColor="#3C5069" />
          <stop offset="100%" stopColor="#2B3C51" />
        </linearGradient>
      </defs>

      {/* 落地阴影 */}
      <ellipse cx="100" cy="252" rx="66" ry="12" fill={`url(#${uid}-shadow)`} />

      <g transform={`translate(0, ${breathe})`}>
        {/* 腿：短、粗、圆，减少成人长腿感 */}
        <rect x="78" y="208" width="20" height="42" rx="10" fill="#27364A" />
        <rect x="102" y="208" width="20" height="42" rx="10" fill="#27364A" />
        <ellipse cx="88" cy="251" rx="15" ry="6.5" fill="#22303F" />
        <ellipse cx="112" cy="251" rx="15" ry="6.5" fill="#22303F" />

        {/* 左臂（观者左侧）：可抬起举手。位置略探出身体轮廓，缩小后仍能看出手臂 */}
        <g transform={`rotate(${armL} 60 168)`}>
          <rect x="51" y="160" width="22" height="42" rx="11" fill={SLEEVE} />
          <circle cx="62" cy="205" r="9.5" fill={COLOR.skin} />
        </g>

        {/* 右臂 */}
        <g transform={`rotate(${armR} 140 168)`}>
          <rect x="127" y="160" width="22" height="42" rx="11" fill={SLEEVE} />
          <circle cx="138" cy="205" r="9.5" fill={COLOR.skin} />
        </g>

        {/* 身体：短圆的整体块，无胸前缝线 */}
        <path
          d="M100 134 C 72 134 58 152 56 178 L 54 202 C 54 216 74 224 100 224 C 126 224 146 216 146 202 L 144 178 C 142 152 128 134 100 134 Z"
          fill={`url(#${uid}-body)`}
        />

        {/* 头 */}
        <g transform={`translate(${headShift}, 0) rotate(${headTilt} 100 150)`}>
          <circle cx="100" cy="88" r="62" fill={COLOR.skin} />

          {/* 两个小而简洁的深色眼睛，无高光点 */}
          <ellipse cx={80 + look} cy="96" rx="6.4" ry={6.4 * blink} fill="#2A3542" />
          <ellipse cx={120 + look} cy="96" rx="6.4" ry={6.4 * blink} fill="#2A3542" />

          {/* 帽子 */}
          <g transform={`rotate(${hatLag} 100 60)`}>
            {hat === 'A' ? (
              <>
                {/* A：圆顶软帽。帽体比头略宽 5 个单位、向下包住两侧；
                    帽沿是一条中间略高、两侧下压的柔和弧线，压在额头上但不遮眼睛。 */}
                <path
                  d="M 31 76 C 23 40 54 12 100 12 C 146 12 177 40 169 76 Q 100 60 31 76 Z"
                  fill={`url(#${uid}-hat)`}
                />
              </>
            ) : (
              <>
                {/* B：短垂尖软帽。帽尖从帽顶向右下自然垂落，末端收在帽沿上方，
                    外缘不超出帽体轮廓，避免成为向侧面伸出的独立小结 */}
                <path
                  d="M 31 76 C 23 40 54 12 100 12 C 146 12 177 40 169 76 Q 100 60 31 76 Z"
                  fill={`url(#${uid}-hat)`}
                />
                <path
                  d="M 98 8 C 128 -2 152 14 154 34 C 156 52 146 67 136 66 C 127 65 125 53 132 46 C 141 37 135 22 114 16 C 106 13 101 11 98 8 Z"
                  fill="#AC4255"
                />
                {/* 折片下缘的一道极淡阴影，让帽尖像垂下来的布，而不是贴上去的独立部件 */}
                <path
                  d="M 132 46 C 125 53 127 65 136 66"
                  stroke="rgba(60,18,28,0.28)"
                  strokeWidth="2.4"
                  fill="none"
                  strokeLinecap="round"
                />
              </>
            )}
          </g>
        </g>
      </g>
    </svg>
  );
};
