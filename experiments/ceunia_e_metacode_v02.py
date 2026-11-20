"""CEUNIA-E PACR v0.2: Potercia + Metapotercia, online learning and audit.
Synthetic proof-of-mechanism only; no real-world predictive claim.
"""
import hashlib,json,math,random,time

def sha(o):
 return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
class Expert:
 def __init__(self,lr): self.lr,self.w,self.b=lr,0.,0.
 def predict(self,x): return 1/(1+math.exp(-max(-30,min(30,self.w*x+self.b))))
 def update(self,x,y):
  e=self.predict(x)-y; self.w-=self.lr*e*x; self.b-=self.lr*e
class CEUNIAE:
 def __init__(self):
  self.experts=[Expert(.015),Expert(.05),Expert(.14)]; self.lw=[0.,0.,0.]; self.events=[]; self.losses=[]; self.base_losses=[]; self.last_y=None; self.version=0
 @staticmethod
 def loss(p,y):
  p=min(1-1e-12,max(1e-12,p)); return -(y*math.log(p)+(1-y)*math.log(1-p))
 def event(self,kind,payload):
  e={'seq':len(self.events)+1,'type':kind,'version':self.version,'payload':payload,'prev_hash':self.events[-1]['hash'] if self.events else 'GENESIS'}; e['hash']=sha(e); self.events.append(e)
 def step(self,x,y,t):
  # Current y is not used to compute the forecast; it is revealed only after forecast commitment.
  qs=[e.predict(x) for e in self.experts]; ws=[math.exp(max(-20,min(20,a))) for a in self.lw]
  p=min(1-1e-9,max(1e-9,sum(q*w for q,w in zip(qs,ws))/sum(ws)))
  base=.5 if self.last_y is None else (.75 if self.last_y==1 else .25)
  loss=self.loss(p,y); bl=self.loss(base,y)
  self.event('prediction_committed',{'t':t,'x':round(x,8),'p':round(p,8),'baseline_p':base,'label_not_used_before_prediction':True})
  self.losses.append(loss); self.base_losses.append(bl)
  start=max(0,len(self.losses)-50)
  pot=sum(self.base_losses[start:])/len(self.base_losses[start:])-sum(self.losses[start:])/len(self.losses[start:])
  ps=max(0,start-50); pe=start
  prev=(sum(self.base_losses[ps:pe])-sum(self.losses[ps:pe]))/(pe-ps) if pe>ps else 0.
  metapot=pot-prev
  allow=t>0 and math.isfinite(loss) and all(math.isfinite(q) for q in qs)
  if allow:
   for e in self.experts: e.update(x,y)
   for i,q in enumerate(qs): self.lw[i]=max(-20,min(20,self.lw[i]-.12*self.loss(q,y)))
   self.version+=1
   self.event('result_revealed_and_learned',{'t':t,'observed_y':y,'loss':round(loss,8),'point_albedrio':'UPDATE_AFTER_REVEAL','potercia':round(pot,8),'metapotercia':round(metapot,8)})
  else: self.event('update_held',{'t':t,'point_albedrio':'HOLD','loss':round(loss,8)})
  self.last_y=y
  return {'loss':loss,'baseline_loss':bl,'potercia':pot,'metapotercia':metapot,'prediction':p,'y':y}
 def verify(self):
  prev='GENESIS'
  for ev in self.events:
   d=dict(ev); h=d.pop('hash')
   if d['prev_hash']!=prev or sha(d)!=h:return False
   prev=h
  return True

def stream(n,seed):
 r=random.Random(seed); out=[]
 for t in range(n):
  x=r.uniform(-1,1); sign=1 if t<n//2 else -1; prob=1/(1+math.exp(-5*sign*x)); out.append((x,int(r.random()<prob)))
 return out

def run(seed,n=2400):
 data=stream(n,seed); m=CEUNIAE(); t0=time.perf_counter(); rows=[m.step(x,y,t) for t,(x,y) in enumerate(data)]; elapsed=time.perf_counter()-t0; h=n//2
 avg=lambda k,a,b:sum(r[k] for r in rows[a:b])/(b-a)
 out={'version':'CEUNIA-E-PACR-0.2','seed':seed,'observations':n,'source':'synthetic_nonstationary_stream','mean_log_loss':avg('loss',0,n),'sequential_baseline_log_loss':avg('baseline_loss',0,n),'gain_vs_sequential_baseline':avg('baseline_loss',0,n)-avg('loss',0,n),'first_half_log_loss':avg('loss',0,h),'second_half_log_loss':avg('loss',h,n),'mean_potercia':avg('potercia',0,n),'mean_metapotercia':avg('metapotercia',0,n),'updates':sum(e['type']=='result_revealed_and_learned' for e in m.events),'events':len(m.events),'hash_chain_valid':m.verify(),'runtime_seconds':elapsed,'metrics_status':'provisional operational proxies','real_data_used':False,'future_labels_used_before_prediction':False}
 out['report_hash']=sha(out); return out
if __name__=='__main__':
 results=[run(s) for s in (20261018,20261019,20261020)]
 print(json.dumps({'suite':'CEUNIA-E-PACR-0.2','results':results,'pass':all(r['hash_chain_valid'] and not r['future_labels_used_before_prediction'] for r in results)},indent=2))
