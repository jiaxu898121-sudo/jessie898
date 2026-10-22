import sys,wave,time,json
from pathlib import Path
# Dependencies are provided by the selected Python runtime.
if '--module-dir' in sys.argv:sys.path.insert(0,sys.argv[sys.argv.index('--module-dir')+1])
import av,numpy as np
from PIL import Image
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--frames',required=True);ap.add_argument('--audio',required=True);ap.add_argument('--output',required=True);ap.add_argument('--fps',type=int,default=30);ap.add_argument('--module-dir');args=ap.parse_args()
frames=Path(args.frames);files=sorted(frames.glob('*.jpeg')) or sorted(frames.glob('*.jpg'))
if not files:raise SystemExit('No JPEG frames')
Path(args.output).parent.mkdir(parents=True,exist_ok=True)
with wave.open(args.audio,'rb') as w:
 sr=w.getframerate();assert w.getnchannels()==2 and w.getsampwidth()==2,'Audio must be stereo PCM16 WAV';audio=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2).astype(np.float32)/32768
assert abs(len(audio)/sr-len(files)/args.fps)<=1/args.fps,'Audio/frame duration mismatch'
out=av.open(args.output,'w',options={'movflags':'+faststart'})
v=out.add_stream('libx264',rate=args.fps)
with Image.open(files[0]) as probe: imageWidth,imageHeight=probe.size
v.width=imageWidth;v.height=imageHeight;v.pix_fmt='yuv420p';v.options={'crf':'20','preset':'fast','threads':'2'}
a=out.add_stream('aac',rate=sr);a.layout='stereo';a.bit_rate=192000
out.metadata['title']='Science term explainer'
from fractions import Fraction
ap=0;start=time.monotonic()
for i,fn in enumerate(files):
 with Image.open(fn) as im: vf=av.VideoFrame.from_image(im.convert('RGB'))
 vf.pts=i;vf.time_base=Fraction(1,args.fps)
 for pkt in v.encode(vf):out.mux(pkt)
 until=min(len(audio),round((i+1)*sr/args.fps))
 while ap+1024<=until:
  af=av.AudioFrame.from_ndarray(audio[ap:ap+1024].T.copy(),format='fltp',layout='stereo');af.sample_rate=sr;af.pts=ap;af.time_base=Fraction(1,sr)
  for pkt in a.encode(af):out.mux(pkt)
  ap+=1024
 if i%600==0:print('encoded',i,'seconds',round(time.monotonic()-start,1),flush=True)
if ap<len(audio):
 af=av.AudioFrame.from_ndarray(audio[ap:].T.copy(),format='fltp',layout='stereo');af.sample_rate=sr;af.pts=ap;af.time_base=Fraction(1,sr)
 for pkt in a.encode(af):out.mux(pkt)
for pkt in v.encode():out.mux(pkt)
for pkt in a.encode():out.mux(pkt)
out.close();print('complete',round(time.monotonic()-start,1),flush=True)

