"""CEUNIA-E / CEUNIA-OBS metacode v0.1.
Deterministic, dependency-free proof-of-mechanism on synthetic data only.
Not a production agent, not evidence of real-world predictive advantage.
"""
from __future__ import annotations
import hashlib, json, math, random, time
from dataclasses import dataclass
from typing import Any

VERSION = "CEUNIA-E-PACR-0.1"

def canonical_hash(obj: Any) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

@dataclass
class OnlineExpert:
    name: str
    lr: float
    w: float = 0.0
    b: float = 0.0
    def predict(self, x: float) -> float:
        z = max(-30.0, min(30.0, self.w*x + self.b))
        return 1.0/(1.0+math.exp(-z))
    def update(self, x: float, y: int) -> None:
        p = self.predict(x)
        err = p-y
        self.w -= self.lr*err*x
        self.b -= self.lr*err

class CEUNIAE:
    """Online contextual ensemble + observed adaptation, provenance, and bounded agency."""
    def __init__(self, seed: int = 20261018):
        self.rng = random.Random(seed)
        self.experts = [OnlineExpert("slow", .015), OnlineExpert("medium", .05), OnlineExpert("fast", .14)]
        self.log_weights = [0.0]*len(self.experts)
        self.events: list[dict[str, Any]] = []
        self.loss_history: list[float] = []
        self.baseline_loss: list[float] = []
        self.prior_context: list[float] = []
        self.last_prediction: float | None = None
        self.last_context: float | None = None
        self.last_decision = "INIT"
        self.model_version = 0

    @staticmethod
    def loss(p: float, y: int) -> float:
        p = min(1-1e-12, max(1e-12, p))
        return -(y*math.log(p)+(1-y)*math.log(1-p))

    def _event(self, kind: str, payload: dict[str, Any]) -> None:
        prev = self.events[-1]["hash"] if self.events else "GENESIS"
        core = {"seq": len(self.events)+1, "time_ns": time.time_ns(), "type": kind,
                "model_version": self.model_version, "payload": payload, "prev_hash": prev}
        core["hash"] = canonical_hash(core)
        self.events.append(core)

    def predict_then_observe(self, x: float, y: int, step: int) -> dict[str, Any]:
        # Prediction is committed before the current label is used.
        ps = [e.predict(x) for e in self.experts]
        ws = [math.exp(max(-30, min(30, lw))) for lw in self.log_weights]
        z = sum(ws) or 1.0
        p = sum(a*b for a,b in zip(ps, ws))/z
        p = min(1-1e-9, max(1e-9, p))
        base = .5 if step == 0 else (0.75 if self.last_prediction is not None and self.last_prediction >= .5 else .25)
        prequential_loss = self.loss(p, y)
        drift = abs(x-(self.prior_context[-1] if self.prior_context else x))
        confidence = abs(p-.5)*2
        # Point Albedrío is a bounded policy gate. Here, updates are authorized only
        # after a prediction has been emitted and its target revealed.
        allow_update = (step >= 1 and math.isfinite(prequential_loss))
        decision = "UPDATE_AUTHORIZED" if allow_update else "HOLD_AND_OBSERVE"
        b_loss = self.loss(base, y)
        self.loss_history.append(prequential_loss); self.baseline_loss.append(b_loss)
        old_version = self.model_version
        self._event("prediction", {"step":step,"x":round(x,8),"p":round(p,8),"baseline_p":base,
                                    "label_revealed_after_prediction":True,"model_probs":[round(q,8) for q in ps]})
        if allow_update:
            for e in self.experts: e.update(x,y)
            for i,q in enumerate(ps):
                self.log_weights[i] = max(-20, min(20, self.log_weights[i] - .15*self.loss(q,y)))
            self.model_version += 1
            self._event("learning_update", {"step":step,"label":y,"loss":round(prequential_loss,8),
                                             "decision":decision,"from_version":old_version,"to_version":self.model_version})
        else:
            self._event("bounded_abstention", {"step":step,"decision":decision,"drift":round(drift,8),
                                                "loss":round(prequential_loss,8)})
        self.prior_context.append(x)
        self.last_prediction = p; self.last_context=x; self.last_decision=decision
        # CEUNIA metrics are explicit proxies, not certified measures.
        recent = self.loss_history[-25:]
        recent_base = self.baseline_loss[-25:]
        potency = (sum(recent_base)/len(recent_base) - sum(recent)/len(recent)) if recent else 0.0
        prev = slice(max(0,len(self.loss_history)-50), max(0,len(self.loss_history)-25))
        prev_gain = (sum(self.baseline_loss[prev])/max(1,len(self.baseline_loss[prev])) - sum(self.loss_history[prev])/max(1,len(self.loss_history[prev]))) if len(self.loss_history)>25 else 0.0
        metapotency = potency-prev_gain
        serendipity = max(0.0, b_loss-prequential_loss) if max(abs(q-.5) for q in ps)<.2 else 0.0
        metaserendipity = serendipity if drift > .25 and prequential_loss < b_loss else 0.0
        return {"step":step,"prediction":p,"label":y,"loss":prequential_loss,"baseline_loss":b_loss,
                "potency_proxy":potency,"metapotency_proxy":metapotency,"serendipity_proxy":serendipity,
                "metaserendipity_proxy":metaserendipity,"point_albedrio":decision,"confidence":confidence,
                "drift":drift,"model_version":self.model_version}

    def verify_chain(self) -> bool:
        prev = "GENESIS"
        for event in self.events:
            candidate = dict(event); actual = candidate.pop("hash")
            if candidate.get("prev_hash") != prev or canonical_hash(candidate) != actual:
                return False
            prev = actual
        return True

def make_stream(n: int = 2400, seed: int = 20261018) -> list[tuple[float,int]]:
    """Synthetic contextual stream with a concept change; never represents real data."""
    rng = random.Random(seed); rows=[]
    for t in range(n):
        x = rng.uniform(-1,1)
        sign = 1 if t < n//2 else -1
        prob = 1/(1+math.exp(-5*sign*x))
        y = 1 if rng.random() < prob else 0
        rows.append((x,y))
    return rows

def run(seed: int = 20261018, n: int = 2400) -> dict[str, Any]:
    stream = make_stream(n, seed)
    model = CEUNIAE(seed)
    t0=time.perf_counter(); rows=[]
    for step,(x,y) in enumerate(stream): rows.append(model.predict_then_observe(x,y,step))
    elapsed=time.perf_counter()-t0
    mean_loss=sum(r["loss"] for r in rows)/n
    fixed_loss=sum(model.loss(.5,y) for _,y in stream)/n
    acc=sum((r["prediction"]>=.5)==bool(r["label"]) for r in rows)/n
    half=n//2
    first=sum(r["loss"] for r in rows[:half])/half
    second=sum(r["loss"] for r in rows[half:])/(n-half)
    result={"version":VERSION,"data":"synthetic_nonstationary_stream","seed":seed,"n":n,
            "mean_prequential_log_loss":mean_loss,"fixed_0_5_log_loss":fixed_loss,
            "gain_vs_fixed_0_5":fixed_loss-mean_loss,"accuracy":acc,
            "first_half_log_loss":first,"second_half_log_loss":second,
            "updates":sum(e["type"]=="learning_update" for e in model.events),
            "abstentions":sum(e["type"]=="bounded_abstention" for e in model.events),
            "events":len(model.events),"hash_chain_valid":model.verify_chain(),
            "runtime_seconds":elapsed,"metrics_are_proxies_not_certified":True,
            "real_world_predictive_claim":False}
    result["result_hash"]=canonical_hash(result)
    return result

if __name__ == "__main__":
    outputs=[run(seed=s) for s in (20261018,20261019,20261020)]
    print(json.dumps({"suite":VERSION,"results":outputs,
                      "pass":all(r["hash_chain_valid"] and r["n"]==2400 for r in outputs)},indent=2))
