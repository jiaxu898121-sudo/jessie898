import argparse,json,re,sys
from pathlib import Path

def load(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def validate(project,evidence):
 errors=[];warnings=[];fps=project.get('fps',30);ids=set();sources={s['id']:s for s in evidence.get('sources',[])};claims={c['id']:c for c in evidence.get('claims',[])}
 if fps<=0:errors.append('fps must be positive');return errors,warnings
 for c in claims.values():
  if c.get('type') not in ['illustration','question','invitation'] and not c.get('source_ids'):errors.append('claim without source: '+c['id'])
  for sid in c.get('source_ids',[]):
   if sid not in sources:errors.append('unknown source: '+sid)
  if not c.get('support') or 'limits' not in c:errors.append('claim missing support/limits: '+c['id'])
 for s in sources.values():
  if s.get('accessed') not in ['full','abstract','excerpt']:errors.append('unread source: '+s['id'])
  if not s.get('url') or not s.get('locator'):errors.append('source needs URL and locator: '+s['id'])
 total=0
 for sc in project.get('scenes',[]):
  sid=sc.get('id','');dur=sc.get('duration',0)
  if not re.fullmatch('[A-Za-z][A-Za-z0-9-]*',sid) or sid in ids:errors.append('invalid/duplicate scene id: '+sid)
  ids.add(sid);total+=dur
  if dur<=0 or abs(dur*fps-round(dur*fps))>1e-6:errors.append('invalid scene duration: '+sid)
  if not sc.get('beats'):errors.append('scene has no beats: '+sid)
  for field in ['beats','panels']:
   end=0
   for item in sc.get(field,[]):
    a,b=item.get('at',0),item.get('end',dur)
    if not 0<=a<b<=dur or a<end-1e-7:errors.append('overlap/out-of-range '+sid+'/'+field)
    for t in [a,b]:
     if abs(t*fps-round(t*fps))>1e-6:errors.append('time not on frame: '+sid)
    end=b
    if not item.get('zh') or not item.get('en'):errors.append('missing bilingual text: '+sid)
    kind=item.get('type','')
    if kind not in ['illustration','question','invitation'] and not item.get('claim_ids'):errors.append('unmapped factual text: '+sid)
    for cid in item.get('claim_ids',[]):
     if cid not in claims:errors.append('unknown claim: '+cid)
    if len(item.get('zh','').replace('\n',''))/(b-a)>5:warnings.append('fast Chinese reading: '+sid)
    if len(item.get('en','').split())/(b-a)>3.5:warnings.append('fast English reading: '+sid)
  for cid in sc.get('note_claim_ids',[]):
   if cid not in claims:errors.append('unknown note claim: '+cid)
 if not project.get('scenes'):errors.append('no scenes')
 for cue in project.get('cues',[]):
  t=cue.get('time',-1)
  if not 0<=t<total or abs(t*fps-round(t*fps))>1e-6:errors.append('cue outside timeline or off frame')
  if not 100<=cue.get('frequency_hz',659)<=3000 or not 0<=cue.get('amplitude',.025)<=.1:errors.append('cue outside permitted gentle tone parameters')
 return errors,warnings
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--project',required=True);ap.add_argument('--evidence',required=True);ap.add_argument('--output');a=ap.parse_args()
 e,w=validate(load(a.project),load(a.evidence));r={'errors':e,'warnings':w,'structural_pass':not e,'scientific_truth_review':'not_run','layout_review':'not_run','listening_review':'not_run'}
 if a.output:Path(a.output).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(r,ensure_ascii=False));sys.exit(bool(e))
