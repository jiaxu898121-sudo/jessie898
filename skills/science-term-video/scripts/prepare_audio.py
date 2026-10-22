import argparse,json,wave
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--project',required=True);ap.add_argument('--music');ap.add_argument('--silence',action='store_true');ap.add_argument('--loop');ap.add_argument('--gain-db',type=float,default=-1.7);ap.add_argument('--output',required=True);a=ap.parse_args()
p=json.loads(Path(a.project).read_text(encoding='utf-8-sig'));secs=sum(s['duration'] for s in p['scenes']);sr=48000;n=round(secs*sr);report={'seconds':secs,'sample_rate':sr,'loop':None,'listening_review':'not_run'}
if a.silence and a.music:raise SystemExit('Use --music OR --silence')
if a.silence:out=np.zeros((n,2))
else:
 if not a.music:raise SystemExit('Provide --music or explicitly choose --silence')
 with wave.open(a.music,'rb') as w:
  if (w.getframerate(),w.getnchannels(),w.getsampwidth())!=(sr,2,2):raise SystemExit('Convert music to 48kHz stereo PCM16 WAV with FFmpeg first')
  src=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2).astype(float)/32768
 if len(src)>=n:out=src[:n].copy()
 elif not a.loop:raise SystemExit('Music shorter than target: provide a longer track or a reviewed loop plan; no arbitrary repetition performed')
 else:
  plan=json.loads(Path(a.loop).read_text(encoding='utf-8-sig'));center=plan['center_sec'];jump=plan['source_offset_sec'];fade=plan['crossfade_sec'];l=round((center-fade/2)*sr);r=round((center+fade/2)*sr);il=round((center-jump-fade/2)*sr);ir=il+(r-l)
  if not (0<fade and 0<jump and 0<=l<r<=min(n,len(src)) and 0<=il<ir<=len(src) and ir+n-r<=len(src)):raise SystemExit('Loop interval or target tail exceeds available source; choose a different plan')
  old=src[l:r];incoming=src[il:ir].copy();rms=lambda x:np.sqrt(np.mean(x*x));gain=np.clip(rms(old)/(rms(incoming)+1e-12),10**(-2/20),10**(2/20));incoming*=gain;rho=float(np.corrcoef(old.ravel(),incoming.ravel())[0,1]);rho=rho if np.isfinite(rho) else 0
  theta=np.linspace(0,np.pi/2,r-l)[:,None];g0=np.cos(theta);g1=np.sin(theta);norm=np.sqrt(g0*g0+g1*g1+2*max(0,rho)*g0*g1);out=np.zeros((n,2));out[:l]=src[:l];out[l:r]=(old*g0+incoming*g1)/norm;tail=src[ir:ir+n-r].copy();tg=np.ones(len(tail));m=min(3*sr,len(tail));tg[:m]=np.linspace(gain,1,m);out[r:]=tail*tg[:,None];report['loop']={**plan,'gain_db':float(20*np.log10(gain)),'crossfade_output_seconds':[l/sr,r/sr]}
 out*=10**(a.gain_db/20)
for cue in p.get('cues',[]):
 at=round(cue['time']*sr);hz=cue.get('frequency_hz',659.25);amp=cue.get('amplitude',.025)
 if not 0<=at<n or not 100<=hz<=3000 or not 0<=amp<=.1:raise SystemExit('Invalid cue')
 t=np.arange(round(2.1*sr))/sr;env=(1-np.exp(-t/.009))*np.exp(-t/.52);tone=(np.sin(2*np.pi*hz*t)+.21*np.sin(2*np.pi*hz*2*t)+.06*np.sin(2*np.pi*hz*3*t))*env*amp;hit=np.stack([tone,tone*.92],axis=1);delay=round(.19*sr);hit[delay:]+=hit[:-delay].copy()*.2;m=min(len(hit),n-at);out[at:at+m]+=hit[:m]
m=min(n,3*sr);out[-m:]*=np.linspace(1,0,m)[:,None]**1.35;peak=float(np.max(abs(out)));limiter=1
if peak>.84:limiter=.84/peak;out*=limiter
path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
with wave.open(str(path),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype('<i2').tobytes())
report.update(sample_peak_dbfs=float(20*np.log10(np.max(abs(out))+1e-12)),peak_gain_db=float(20*np.log10(limiter)),cues=p.get('cues',[]),rms_windows=[{'at':t,'dbfs':float(20*np.log10(np.sqrt(np.mean(out[round(t*sr):min(n,round((t+.5)*sr))]**2))+1e-12))} for t in np.arange(0,secs,.5)])
path.with_suffix('.report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(str(path))
