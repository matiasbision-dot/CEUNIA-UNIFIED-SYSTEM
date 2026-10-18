"""CEUNIA-E PACR v0.3: drift-aware online learning, Potercia and Metapotercia.
Synthetic benchmark only; no real-world predictive claim.
"""
from __future__ import annotations
import hashlib,json,math,random,statistics,time
VERSION='CEUNIA-E-PACR-0.3'
def canon_hash(obj):
 return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def logloss(p,y):
 p=min(1-1e-12,max(1e-12,p)); return -(y*math.log(p)+(1-y)*math.log(1-p))
class Expert:
 def __init__(self,lr): self.lr,self.w,self.b,self.lr_scale=lr,0.,0.,1.
 def predict(self,x): return 1/(1+math.exp(-max(-30,min(30,self.w*x+self.b))))
 def update(self,x,y):
  err=self.predict(x)-y; self.w-=self.lr*self.lr_scale*err*x; self.b-=self.lr*self.lr_scale*err
class BaseModel:
 def __init__(self): self.events=[]; self.losses=[]; self.base_losses=[]; self.prev_y=None; self.version=0
 def event(self,kind,payload):
  e={'seq':len(self.events)+1,'type':kind,'version':self.version,'payload':payload,'prev_hash':self.events[-1]['hash'] if self.events else 'GENESIS'}; e['hash']=canon_hash(e); self.events.append(e)
 def verify_chain(self):
  prev='GENESIS'
  for e in self.events:
   obj=dict(e); h=obj.pop('hash')
   if obj['prev_hash']!=prev or canon_hash(obj)!=h:return False
   prev=h
  return True
 def base_prob(self): return .5 if self.prev_y is None else (.75 if self.prev_y else .25)
 def metrics(self,p,y):
  loss=logloss(p,y); bl=logloss(self.base_prob(),y); self.losses.append(loss); self.base_losses.append(bl)
  w=50; lo=max(0,len(self.losses)-w)
  pot=sum(self.base_losses[lo:])/len(self.base_losses[lo:])-sum(self.losses[lo:])/len(self.losses[lo:])
  plo=max(0,lo-w); phi=lo
  prevpot=(sum(self.base_losses[plo:phi])-sum(self.losses[plo:phi]))/(phi-plo) if phi>plo else 0.
  self.prev_y=y
  return loss,bl,pot,pot-prevpot
class OnlineLogistic(BaseModel):
 def __init__(self,lr=.05): super().__init__(); self.e=Expert(lr)
 def step(self,x,y,t):
  p=self.e.predict(x); loss,bl,pot,mp=self.metrics(p,y)
  self.event('prediction_then_reveal',{'t':t,'p':round(p,8),'label':y,'prediction_preceded_label_update':True})
  self.e.update(x,y); self.version+=1; self.event('learning_update',{'t':t,'loss':round(loss,8)})
  return {'loss':loss,'baseline_loss':bl,'potercia':pot,'metapotercia':mp}
class AdaptiveEnsemble(BaseModel):
 def __init__(self,drift_aware=False):
  super().__init__(); self.experts=[Expert(.015),Expert(.05),Expert(.14)]; self.logw=[0.,0.,0.]
  self.drift_aware=drift_aware; self.drift_events=0; self.boost_remaining=0; self.loss_window=50; self.recent=[]; self.consecutive=0; self.cooldown=0
 def predict(self,x):
  qs=[e.predict(x) for e in self.experts]; ws=[math.exp(max(-20,min(20,a))) for a in self.logw]
  return min(1-1e-9,max(1e-9,sum(q*w for q,w in zip(qs,ws))/sum(ws))),qs
 def step(self,x,y,t):
  p,qs=self.predict(x); loss,bl,pot,mp=self.metrics(p,y)
  self.event('prediction_committed',{'t':t,'p':round(p,8),'label_revealed_after_prediction':True})
  self.recent.append(loss); trigger=False
  if self.cooldown>0:self.cooldown-=1
  if self.drift_aware and self.cooldown==0 and len(self.recent)>=2*self.loss_window:
   old=self.recent[-2*self.loss_window:-self.loss_window]; new=self.recent[-self.loss_window:]
   delta=statistics.mean(new)-statistics.mean(old)
   self.consecutive=self.consecutive+1 if delta>.035 else 0
   if self.consecutive>=2:
    trigger=True; self.drift_events+=1; self.consecutive=0; self.logw=[0.,0.,0.]; self.boost_remaining=80; self.cooldown=150
    self.event('drift_detected_and_recovery_started',{'t':t,'loss_delta':round(delta,8),'boost_steps':80,'cooldown_steps':150})
  scale=1.8 if self.boost_remaining>0 else 1.
  for e in self.experts:e.lr_scale=scale;e.update(x,y);e.lr_scale=1.
  for i,q in enumerate(qs):self.logw[i]=max(-20,min(20,self.logw[i]-.12*logloss(q,y)))
  if self.boost_remaining>0:self.boost_remaining-=1
  self.version+=1; self.event('learning_update',{'t':t,'loss':round(loss,8),'drift_trigger':trigger,'boost_remaining':self.boost_remaining})
  return {'loss':loss,'baseline_loss':bl,'potercia':pot,'metapotercia':mp}
def make_stream(n,seed,switch=True):
 r=random.Random(seed); data=[]; switch_at=n//2 if switch else n+1
 for t in range(n):
  x=r.uniform(-1,1); sign=1 if t<switch_at else -1; prob=1/(1+math.exp(-5*sign*x)); data.append((x,int(r.random()<prob)))
 return data
def run_one(seed,n=3000):
 data=make_stream(n,seed,True); models={'single_online_logistic':OnlineLogistic(.05),'adaptive_ensemble':AdaptiveEnsemble(False),'drift_aware_ensemble':AdaptiveEnsemble(True)}; outputs={}
 for name,m in models.items():
  rows=[m.step(x,y,t) for t,(x,y) in enumerate(data)]; h=n//2
  outputs[name]={'mean_log_loss':statistics.mean(r['loss'] for r in rows),'first_half_log_loss':statistics.mean(r['loss'] for r in rows[:h]),'second_half_log_loss':statistics.mean(r['loss'] for r in rows[h:]),'post_switch_100_log_loss':statistics.mean(r['loss'] for r in rows[h:h+100]),'potercia_final':rows[-1]['potercia'],'metapotercia_final':rows[-1]['metapotercia'],'updates':sum(e['type']=='learning_update' for e in m.events),'events':len(m.events),'hash_chain_valid':m.verify_chain(),'drift_events':getattr(m,'drift_events',0)}
 return {'seed':seed,'n':n,'models':outputs}
def main():
 t0=time.perf_counter(); results=[run_one(s) for s in range(20261018,20261038)]; names=list(results[0]['models']); summary={}
 for name in names:
  for metric in ('mean_log_loss','first_half_log_loss','second_half_log_loss','post_switch_100_log_loss'):
   vals=[r['models'][name][metric] for r in results]; summary.setdefault(name,{})[metric+'_mean']=statistics.mean(vals); summary[name][metric+'_sd']=statistics.stdev(vals)
 for candidate in ('adaptive_ensemble','drift_aware_ensemble'):
  diffs=[r['models']['single_online_logistic']['mean_log_loss']-r['models'][candidate]['mean_log_loss'] for r in results]
  summary[candidate]['paired_gain_vs_single_mean']=statistics.mean(diffs); summary[candidate]['seeds_better_than_single']=sum(d>0 for d in diffs)
 counts=[r['models']['drift_aware_ensemble']['drift_events'] for r in results]
 report={'version':VERSION,'dataset':'synthetic_nonstationary_stream','seed_start':20261018,'seeds':len(results),'observations_per_seed':3000,'total_observations':len(results)*3000,'concept_reversal_at_halfway':True,'models':summary,'drift_detection_events_mean':statistics.mean(counts),'all_hash_chains_valid':all(r['models'][m]['hash_chain_valid'] for r in results for m in names),'runtime_seconds':time.perf_counter()-t0,'raw_seed_results':results,'metrics_status':'Potercia and Metapotercia are provisional operational proxies','real_world_predictive_claim':False,'limitations':['Synthetic data only.','Fixed concept reversal is a known benchmark, not a live-data test.','Drift threshold is preselected, not tuned on holdout.','Ablations and confidence intervals are still needed.','Hash chain does not authenticate source data.']}
 report['report_hash']=canon_hash(report); print(json.dumps(report,indent=2))
if __name__=='__main__':main()
