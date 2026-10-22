# 工具、流程与命令

## 工具分工

| 任务 | 优先工具 | 能力边界 |
| --- | --- | --- |
| 查证 | 可用网络检索、PubMed/期刊/研究团队原文；可选科研连接器 | 摘要不等于全文；连接器不是必须 |
| 分镜与画面 | Node.js、React、Remotion；已有remotion-best-practices | 不需要GitHub代调其他模型 |
| 音频解码/混合 | FFmpeg + Python/NumPy | 不依赖Cubase；不自动下载音乐 |
| 替代导出 | JPEG帧序列 + encode_frames.py（PyAV/Pillow/NumPy） | 默认编码失败才切换，不反复无差别重试 |
| 成片核验 | audit_video.py（PyAV/Pillow/NumPy）、实际看图与试听 | 技术指标不是听感与科学准确性 |
| 新插画/音乐 | 已安装图像/音乐工具，确有需要才用 | 新付费调用先按用户授权处理 |

先定位已有Node/Python/FFmpeg，不把某台机器的绝对路径写成通用要求。Python需要numpy、Pillow、av；初始化和验证脚本仅用标准库。缺依赖时说明；不要自动引入庞大软件。

## 标准流程

1. 整理input.json，浏览原文并写evidence.json，完成project.json；运行validate_project.py。
2. `python scripts/scaffold.py --input input.json --project project.json --evidence evidence.json --output NEW_PROJECT_DIR`
   输出目录必须不存在，避免覆盖。脚本只复制模板，不安装依赖、不联网、不研究选题。
3. 在工程目录安装/复用已批准的Remotion依赖；打开Studio后再实现/调整镜头。命令以当前平台工具路径为准：`npx remotion studio src/index.ts --no-open --port=3119`。实际打开该URL确认composition显示。
4. 配乐先转为48kHz双声道PCM16 WAV。例如：`ffmpeg -i selected.mp3 -ar 48000 -ac 2 -c:a pcm_s16le selected.wav`。
5. `python scripts/prepare_audio.py --project NEW_PROJECT_DIR/src/project.json --music selected.wav --output NEW_PROJECT_DIR/public/audio/mix.wav`
   无音乐明确使用`--silence`；脚本输出report，工程audio_asset设为audio/mix.wav。
6. 选最复杂的两帧/十秒预览，按用户要求决定是否等待反馈。用户要MP4则导出：在工程目录`npx remotion render src/index.ts TermVideo out/final-v1.mp4 --overwrite`。
7. 若编码进程失败，换独立端口、降低并发；仍失败则渲染JPEG序列：`npx remotion render src/index.ts TermVideo build/frames --sequence --image-format=jpeg --jpeg-quality=90 --muted --concurrency=2 --port=3125`。
   `python scripts/encode_frames.py --frames NEW_PROJECT_DIR/build/frames --audio NEW_PROJECT_DIR/public/audio/mix.wav --output NEW_PROJECT_DIR/out/final-v1.mp4 --fps 30`
8. `python scripts/audit_video.py NEW_PROJECT_DIR/out/final-v1.mp4 --output NEW_PROJECT_DIR/docs/qa.json`
   查看contact图与过渡片段，按quality.md补人工检查。代理不能将自动report中的not_run改成pass而不执行对应检查。

## 配乐替换和循环

足够长的音乐只裁切所需部分并片尾淡出；不要重复已淡出的尾巴。短音乐脚本会拒绝任意填满。

确实需要循环时，在分析和试听后提供loop.json：
```json
{"center_sec":49.3,"source_offset_sec":40.8,"crossfade_sec":3.0,"musical_match_review":"checked separately"}
```
这里数值仅为字段示例，不是所有音乐可用的默认值。脚本按center±crossfade/2把源音乐与向后偏移source_offset的片段叠接，使用均方根增益匹配及相关补偿的等功率过渡；检查源区间、目标尾部是否越界。短音乐只支持一次明确回跳，不自动无限循环。调用时附`--loop loop.json`。musical_match_review是供人阅读的说明，不是自动验真的证据。

重配音轨后重新核验cue与字幕落帧；音轨变更时不要无故重排科学文案。只改音乐可用FFmpeg视频流copy换音轨，输出新文件；改文字/卡片则仅重渲染受影响段，最后检查合片时长和接缝。
