"""CEUNIA Ω online learning and anticipatory model selection on NASA POWER monthly data.

Historical months are replayed as simulated future: at month t all forecasts and
the model choice use only months < t. The target is revealed afterward, errors are
scored, and the seasonal residual learner is updated for month t+1.
"""
from __future__ import annotations
import hashlib, json, math, os, urllib.parse, urllib.request
from typing import Any

LATITUDE=-38.0
LONGITUDE=-57.55
START_DATE="2010"
END_DATE="2025"
PARAMETER="T2M"
USER_AGENT="CEUNIA-Research-Prototype/1.1"

def fetch_nasa_power_monthly() -> tuple[list[str], list[float], str]:
    params={"parameters":PARAMETER,"community":"RE","longitude":str(LONGITUDE),
            "latitude":str(LATITUDE),"start":START_DATE,"end":END_DATE,"format":"JSON"}
    url="https://power.larc.nasa.gov/api/temporal/monthly/point?"+urllib.parse.urlencode(params)
    req=urllib.request.Request(url,headers={"User-Agent":USER_AGENT})
    with urllib.request.urlopen(req,timeout=60) as response: raw=response.read()
    digest=hashlib.sha256(raw).hexdigest()
    data=json.loads(raw).get("properties",{}).get("parameter",{}).get(PARAMETER)
    if not isinstance(data,dict) or not data: raise RuntimeError("NASA POWER response lacks monthly T2M")
    pairs=[]
    for key,value in sorted(data.items()):
        if not isinstance(key,str) or len(key)!=6 or not key.isdigit(): continue
        month=int(key[4:6])
        if not 1<=month<=12: continue
        val=float(value)
        if not math.isfinite(val) or val<=-900: continue
        pairs.append((f"{key[:4]}-{key[4:6]}",val))
    if len(pairs)<100: raise RuntimeError(f"Too few valid monthly observations: {len(pairs)}")
    # Fail closed if the provider returns duplicate or non-contiguous monthly keys.
    keys=[int(m[:4])*12+int(m[5:])-1 for m,_ in pairs]
    if len(set(keys))!=len(keys) or any(b-a!=1 for a,b in zip(keys,keys[1:])):
        raise RuntimeError("NASA POWER monthly series contains duplicate or missing months")
    return [m for m,_ in pairs],[v for _,v in pairs],digest

def mae(actual:list[float],predicted:list[float])->float:
    if not actual or len(actual)!=len(predicted): raise ValueError("Series must have equal non-zero lengths")
    return sum(abs(a-p) for a,p in zip(actual,predicted))/len(actual)

def run_walk_forward(months:list[str],values:list[float],initial_train:int=60,
                     validation_window:int=24,alpha:float=.15,min_improvement:float=.02)->dict[str,Any]:
    if len(months)!=len(values) or initial_train<24 or initial_train>=len(values):
        raise ValueError("Invalid chronological series or initial_train")
    if validation_window<12 or not 0<alpha<=1 or not 0<=min_improvement<1:
        raise ValueError("Invalid validation_window, alpha, or min_improvement")
    # Score histories contain only targets revealed before the current prediction.
    preds={"persistence":[],"seasonal":[],"online_corrected":[],"gated":[]}
    actuals=[]; dates=[]; residual_bias=0.0; selection_counts={k:0 for k in ("persistence","seasonal","online_corrected")}
    for t in range(initial_train,len(values)):
        pred_persistence=values[t-1]
        pred_seasonal=values[t-12] if t>=12 else pred_persistence
        pred_corrected=pred_seasonal+residual_bias
        selected="persistence"
        if len(actuals)>=validation_window:
            hist_actual=actuals[-validation_window:]
            scores={
                "persistence":mae(hist_actual,preds["persistence"][-validation_window:]),
                "seasonal":mae(hist_actual,preds["seasonal"][-validation_window:]),
                "online_corrected":mae(hist_actual,preds["online_corrected"][-validation_window:]),
            }
            best=min(scores,key=scores.get)
            if best!="persistence" and scores[best] < scores["persistence"]*(1-min_improvement):
                selected=best
        current={"persistence":pred_persistence,"seasonal":pred_seasonal,"online_corrected":pred_corrected}
        # Lock all candidate forecasts and the chosen forecast before revealing y_t.
        for key in current: preds[key].append(current[key])
        preds["gated"].append(current[selected]); selection_counts[selected]+=1
        y=values[t]
        actuals.append(y); dates.append(months[t])
        # Online update only after target reveal; affects predictions from t+1 onward.
        residual_bias=(1-alpha)*residual_bias+alpha*(y-pred_seasonal)
    scores={key:mae(actuals,preds[key]) for key in preds}
    baseline=scores["persistence"]
    return {
      "initial_train_months":initial_train,"test_months":len(actuals),"test_start":dates[0],"test_end":dates[-1],
      "mae_by_model":scores,
      "improvement_vs_persistence_pct":{key:100*(baseline-value)/baseline for key,value in scores.items()},
      "selection_counts":selection_counts,
      "online_learning":{"enabled":True,"rule":"EMA of seasonal forecast residuals; update after target reveal only","alpha":alpha},
      "selector":{"validation_window":validation_window,"minimum_relative_gain":min_improvement,
                  "rule":"choose best trailing MAE only when it beats persistence by minimum relative gain"},
      "protocol":"forecast -> lock prediction and choice -> reveal current target -> score -> update residual",
      "data_kind":"REAL NASA POWER historical monthly observations replayed chronologically",
      "caveat":"Historical replay is not a guarantee of future accuracy; all models and parameters should be evaluated on a final untouched holdout.",
    }

def main()->dict[str,Any]:
    months,values,source_hash=fetch_nasa_power_monthly()
    report={"schema":"CEUNIA-ONLINE-METACODE-1.1","dataset":"NASA POWER monthly point data",
      "parameter":PARAMETER,"units":"degC","latitude":LATITUDE,"longitude":LONGITUDE,
      "source_period_requested":f"{START_DATE}-{END_DATE}","observations":len(values),
      "first_month":months[0],"last_month":months[-1],"raw_response_sha256":source_hash,
      "method":run_walk_forward(months,values)}
    report["report_sha256"]=hashlib.sha256(json.dumps(report,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    output=os.environ.get("CEUNIA_REPORT_PATH","ceunia_nasa_power_report.json")
    with open(output,"w",encoding="utf-8") as f: json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2)); return report

if __name__=="__main__": main()
