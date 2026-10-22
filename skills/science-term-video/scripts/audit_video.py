import argparse,json,sys,math
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('video');ap.add_argument('--output',required=True);ap.add_argument('--module-dir');a=ap.parse_args()
if a.module_dir:sys.path.insert(0,a.module_dir)
try:import av,numpy as np;from PIL import Image,ImageDraw
except ImportError:raise SystemExit('Requires PyAV, NumPy and Pillow; install approved packages or use available runtime')
c=av.open(a.video);s=c.streams.video[0];fps=float(s.average_rate);meta={'width':s.width,'height':s.height,'fps':fps};duration=float(s.duration*s.time_base) if s.duration else 0;targets=set(round(t*fps) for t in np.linspace(.5,max(.5,duration-.5),min(16,max(1,int(duration)))));samples=[];count=0;prev=None;gaps=[]
for f in c.decode(s):
 t=float(f.pts*f.time_base)
 if prev is not None and abs(t-prev-1/fps)>1e-5:gaps.append({'frame':count,'delta':t-prev})
 if count in targets:samples.append((t,f.to_image().resize((480,270))))
 prev=t;count+=1
c.close();out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(1920,max(300,math.ceil(len(samples)/4)*300)),'#D9DFE2');d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(samples):x=i%4*480;y=i//4*300;sheet.paste(im,(x,y+25));d.text((x+8,y+6),f'{t:.3f}s',fill='black')
sheet.save(out.with_suffix('.contact.jpg'));c=av.open(a.video);audio={}
if c.streams.audio:
 r=av.AudioResampler(format='fltp',layout='stereo',rate=48000);parts=[];agaps=[];end=None
 for f in c.decode(audio=0):
  t=float(f.pts*f.time_base)
  if end is not None and abs(t-end)>2/48000:agaps.append(t-end)
  end=t+f.samples/f.sample_rate
  for z in r.resample(f):parts.append(z.to_ndarray().T)
 x=np.concatenate(parts);audio={'seconds':len(x)/48000,'sample_peak_dbfs':float(20*np.log10(abs(x).max()+1e-12)),'pts_gaps':agaps,'tail_100ms_rms_dbfs':float(20*np.log10(np.sqrt(np.mean(x[-4800:]**2))+1e-12))}
meta.update(frames=count,seconds=count/fps,frame_gaps=gaps,audio=audio,scientific_truth_review='not_run',layout_review='not_run',listening_review='not_run',note='Contact sheet and metrics require inspection; RMS/sample peak do not establish musical continuity or scientific accuracy.')
out.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(meta,ensure_ascii=False))
