"""CEUNIA Ω: causal, evidence-gated anticipatory correction prototype."""
from __future__ import annotations
import hashlib, json, math, random
from typing import Any

def make_synthetic_history(n: int = 1200, seed: int = 20261018) -> list[float]:
    if n < 3: raise ValueError("n debe ser >= 3")
    rng=random.Random(seed); out=[]
    for t in range(n):
        slope=0.025 if t < 2*n//3 else -0.018
        out.append(10+slope*t+1.8*math.sin(2*math.pi*t/48)+0.7*math.sin(2*math.pi*t/13)+rng.gauss(0,.45))
    return out

def _mae(a, p):
    if not a or len(a)!=len(p): raise ValueError("Series iguales y no vacías requeridas")
    return sum(abs(x-y) for x,y in zip(a,p))/len(a)

def _trend(past, window):
    r=past[-window:]; xs=list(range(len(r))); xm=sum(xs)/len(xs); ym=sum(r)/len(r)
    den=sum((x-xm)**2 for x in xs)
    slope=sum((x-xm)*(y-ym) for x,y in zip(xs,r))/den if den else 0.0
    return r[-1]+slope

def walk_forward(values: list[float], start: int=100, window: int=64, validation: int=48,
                 alpha: float=.03, improvement_margin: float=.03) -> dict[str, Any]:
    """Predict and lock first; reveal target and update residual state afterward.
    Switch from persistence only if a candidate beats past-only validation MAE by margin.
    """
    if not (2 <= window <= start < len(values)): raise ValueError("Requiere 2 <= window <= start < len(values)")
    if validation < 8: raise ValueError("validation debe ser >= 8")
    if not (0 < alpha <= 1): raise ValueError("alpha debe estar en (0, 1]")
    if not (0 <= improvement_margin < 1): raise ValueError("improvement_margin debe estar en [0, 1)")
    n=len(values); base=[None]*n; raw=[None]*n; corr=[None]*n; bias=0.0
    for t in range(start,n):
        past=values[:t]; base[t]=past[-1]; raw[t]=_trend(past,window); corr[t]=raw[t]+bias
        # Current target is revealed only after all current predictions are stored.
        bias=(1-alpha)*bias+alpha*(values[t]-raw[t])
    actual=values[start:]; gated=[]; chosen=[]
    for t in range(start,n):
        selected=0
        if t >= start+validation:
            ix=list(range(t-validation,t)); va=[values[j] for j in ix]
            scores=[_mae(va,[base[j] for j in ix]),_mae(va,[raw[j] for j in ix]),_mae(va,[corr[j] for j in ix])]
            candidate=min((1,2),key=lambda i:scores[i])
            if scores[candidate] < scores[0]*(1-improvement_margin): selected=candidate
        gated.append((base[t],raw[t],corr[t])[selected]); chosen.append(selected)
    bm=_mae(actual,base[start:]); rm=_mae(actual,raw[start:]); cm=_mae(actual,corr[start:]); gm=_mae(actual,gated)
    report={"schema":"CEUNIA-ANTICIPATORY-CORRECTION-1.1","data_kind":"SYNTHETIC_NOT_REAL_WORLD",
      "n_total":n,"n_test":len(actual),"start_index":start,"window":window,"validation_window":validation,
      "alpha":alpha,"improvement_margin":improvement_margin,"baseline_mae":bm,"raw_trend_mae":rm,
      "fixed_adaptive_mae":cm,"evidence_gated_mae":gm,
      "gated_vs_baseline_improvement_pct":100*(bm-gm)/bm,
      "selection_counts":{"baseline":chosen.count(0),"raw_trend":chosen.count(1),"adaptive_correction":chosen.count(2)},
      "protocol":"predict -> lock -> reveal target -> score -> update",
      "limitations":["Synthetic data only; no NASA POWER/live data fetched.","Holdout is diagnostic, not independent real-world validation.","Selection can fail under distribution shift.","Not for financial execution."]}
    report["result_sha256"]=hashlib.sha256(json.dumps(report,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return report

if __name__=="__main__": print(json.dumps(walk_forward(make_synthetic_history()),indent=2))
