import argparse,json,shutil
from pathlib import Path
from validate_project import load,validate
ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--project',required=True);ap.add_argument('--evidence',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
brief=load(a.input);p=load(a.project);ev=load(a.evidence);errors,warnings=validate(p,ev)
if (p.get('width'),p.get('height'))!=(1920,1080):raise SystemExit('Bundled template targets 1920x1080; adapt layout before using another resolution')
if errors:raise SystemExit('\n'.join(errors))
out=Path(a.output).resolve()
if out.exists():raise SystemExit('Output must not exist; choose a new version directory')
template=Path(__file__).resolve().parents[1]/'assets/template';shutil.copytree(template,out)
(out/'docs').mkdir(exist_ok=True);(out/'out').mkdir(exist_ok=True)
for name,data in [('input.json',brief),('evidence.json',ev),('src/project.json',p)]:
 (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
start=0;nodes=[];comps=[];fps=p['fps']
for i,s in enumerate(p['scenes']):
 n=round(s['duration']*fps);nodes.append(f'<Scene name={{{json.dumps(s["title"],ensure_ascii=False)}}} index={{{i}}} from={{{start}}} durationInFrames={{{n}}}/>')
 comps.append(f'<Composition id="{s["id"]}" component={{StandaloneScene}} width={{{p["width"]}}} height={{{p["height"]}}} fps={{{fps}}} durationInFrames={{{n}}} defaultProps={{{{index:{i}}}}}/>');start+=n
code="""import React from 'react';
import {AbsoluteFill,Audio,Composition,Track,staticFile} from 'remotion';
import project from './project.json';
import {Scene,StandaloneScene,World} from './Scene';
const Film=()=> <AbsoluteFill><World/><Track name="Scenes">__NODES__</Track>{project.audio_asset?<Audio src={staticFile(project.audio_asset)}/>:null}</AbsoluteFill>;
export const RemotionRoot=()=> <><Composition id="TermVideo" component={Film} width={__WIDTH__} height={__HEIGHT__} fps={__FPS__} durationInFrames={__FRAMES__}/>__COMPS__</>;
"""
for k,v in {'__NODES__':''.join(nodes),'__COMPS__':''.join(comps),'__WIDTH__':str(p['width']),'__HEIGHT__':str(p['height']),'__FPS__':str(fps),'__FRAMES__':str(start)}.items():code=code.replace(k,v)
(out/'src/Root.tsx').write_text(code,encoding='utf-8')
def stamp(s):
 m=round(s*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
rows=[];base=0;script=[]
for s in p['scenes']:
 script.append('## '+s['title'])
 for b in s['beats']:
  rows.append((base+b['at'],base+b['end'],b['zh'],b['en']));script.extend([b['zh'],b['en']])
 for b in s.get('panels',[]):script.extend([b.get('label',''),b['zh'],b['en']])
 base+=s['duration']
# Build subtitle intervals from both headline and timed panel boundaries.
rows=[];base=0
for scene in p['scenes']:
 items=scene['beats']+scene.get('panels',[])
 points=sorted(set([0,scene['duration']]+[v[k] for v in items for k in ['at','end']]))
 for x,y in zip(points,points[1:]):
  active=[v for v in items if v['at']<=x and v['end']>=y]
  if active:rows.append((base+x,base+y,'\n'.join(v['zh'] for v in active),'\n'.join(v['en'] for v in active)))
 base+=scene['duration']
(out/'docs/subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(x)} --> {stamp(y)}\n{z}\n{e}' for i,(x,y,z,e) in enumerate(rows)),encoding='utf-8')
(out/'docs/script.md').write_text('\n\n'.join(script),encoding='utf-8')
(out/'docs/validation.json').write_text(json.dumps({'errors':errors,'warnings':warnings,'scientific_truth_review':'not_run','layout_review':'not_run','listening_review':'not_run'},ensure_ascii=False,indent=2),encoding='utf-8')
print(str(out))
