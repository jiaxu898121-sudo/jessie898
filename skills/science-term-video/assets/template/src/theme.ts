// 全片共用色板与版式常量。后续段落(S02–S06)沿用同一份，保证角色比例、色值、主阅读区稳定。

export const W = 1920;
export const H = 1080;

// 字体：本机 Windows 自带 Noto Sans SC(可变字重) + 微软雅黑兜底。
// 两者均已本地安装，渲染时不依赖网络字体，避免缺字与首帧闪烁。
export const FONT = "'Noto Sans SC', 'Microsoft YaHei', sans-serif";

export const COLOR = {
  bgDeep: '#141E27',
  bgMid: '#1E2A36',
  bgHigh: '#2A3947',
  warmWhite: '#F6F1E7',
  gold: '#E3B87C',
  goldDim: '#C9A46E',
  // 字幕关键词专用：比 gold 亮一档(#E3B87C 峰值亮度 178，比正文 warmWhite 的 239 暗 25%，
  // 68px 细笔画下会显得发闷、与两侧白字视觉粘连)。此色峰值亮度约 207，
  // 仍明显低于正文，靠色相而非压暗来承担"强调"，图形区继续用 gold 不变。
  goldText: '#F7D5A2',
  hat: '#B8485C',
  hatDark: '#9D3A4D',
  skin: '#F7EFE2',
  clothes: '#33455C',
  clothesLight: '#3D5170',
  clothesDark: '#2A3A4E',
  ink: '#2A3542',
};

// 主阅读区：三拍共用同一锚点，不逐屏漂移。
export const TEXT = {
  x: 170,
  zhTop: 206,
  width: 900,
  zhSize: 68,
  zhLineHeight: 1.42,
  enSize: 38,
  enLineHeight: 1.45,
  enGap: 18,
  // 英文行允许比中文行宽：中文主句一眼必须读完，所以卡在 900；
  // 译文是副层，能一行排完比"和中文一样宽"更重要。
  // 实测最长的一行（S04-b3）渲染宽度 1141px，右端 x=1311。
  // 上限取 1250 还留约 110px 余量；再长就会贴到角色头顶那片空白（角色最左 x≈1405），
  // 虽然字幕带下沿 y≈360、角色头顶 y=480，竖向上根本不重叠，但再往右就开始"看着挤"。
  // 超过 1250 的英文行必须改字，不许折两行、也不许压字号。
  enWidth: 1250,
  accentY: 168,
  accentWidth: 72,
};

// 概念图形区中心
export const GRAPHIC = {cx: 1000, cy: 620};

// 角色：可见高度 400px，脚底落在 880 的地平面上，站在画面右侧，面向左侧图形。
export const CHAR = {cx: 1560, feetY: 880, height: 400};
