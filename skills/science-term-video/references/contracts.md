# 输入输出契约

自然语言也可作为输入，代理负责归一化，不要求用户填写全部JSON。

## input.json（需求层）

必填topic、output_dir；其余按上下文默认。terms是本轮要解释的词，不固定四个。deliverable取script/frames/preview/mp4；preview_seconds仅在预览模式使用。format默认1920×1080/30，时长为目标而非压缩内容的硬上限。locked_items声明不可擅改内容。

music.path可为null（明确无BGM）；若用户要求配乐却未提供素材，使用已有明确选定素材，或询问选择，不能把缺音乐伪装成完成。包内不附商业/参考旋律。更换音乐只修改music与cue，视觉保持锁定。

## project.json（可渲染时间线）

- title、fps、width、height、audio_asset（相对public路径或null）。
- scenes数组：id（合法Composition ID）、title、duration秒、beats、panels、note。
- beats：at、end为段内秒，zh、en、type、claim_ids；一段内主字幕不重叠。
- panels：at、end、label、zh、en、type、claim_ids；对话/定义案例/研究发现/总结均可放卡片；同一时间只显示一张。
- note为简短辅助来源字符串；note_claim_ids绑定其中事实。
- cues数组：time（全片绝对秒）、frequency_hz、amplitude；本模板仅生成提示音，不自动推断BPM/强拍。

全片时长=sum(scene.duration)；实际帧数=各段duration×fps的整数和。at/end也必须能精确落帧。中文、英文和卡片文本允许用\n手动换行，但最长排版必须实际预览。

## evidence.json（证据层）

sources数组：id、title、year、url、type、accessed、locator。
claims数组：id、statement、type、source_ids、support、limits。
事实/定义/建议必须指向有效claim；原创示例、提问和邀请可为空，但type需分别为illustration/question/invitation，不能借此把事实伪装成提问。

## 输出目录

```
project/
  input.json
  evidence.json
  src/project.json
  src/Root.tsx
  src/Scene.tsx
  src/components/...
  public/audio/mix.wav
  docs/script.md
  docs/subtitles.srt
  docs/evidence.md
  docs/audio-report.json
  docs/validation.json
  docs/qa.json
  out/final-v1.mp4
  out/contact-sheet.jpg
```

脚本生成的是技术报告，代理另写evidence.md，将sources/claims对应到画面句子；文案与SRT可由scaffold.py生成。qa的truth_review、layout_review、listening_review须分别填写not_run/pass/issues，不能自动设为pass。
