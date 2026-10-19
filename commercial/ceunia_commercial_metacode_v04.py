"""CEUNIA Commercial Evolution Metacode v0.4
Decision-support experiment for prioritizing monetization hypotheses.
All rubric scores and price bands are assumptions, NOT market research or actual revenue.
Standard library only.
"""
from __future__ import annotations
import json, random, statistics, hashlib
from pathlib import Path

VERSION = "CEUNIA-COMMERCIAL-EVOLUTION-0.4"
SEED = 20261018
N_SIM = 50000

HYPOTHESES = {
    "AI evaluation + audit observatory": {
        "scores": {"buyer_pain": 4.5, "mvp_speed": 4.5, "measurable_roi": 4.5,
                   "differentiation": 3.5, "repeatability": 4.5, "sales_access": 3.5,
                   "delivery_ease": 4.0, "evidence_fit": 4.5},
        "offer": "Fixed-scope pilot: evaluate an AI workflow, trace decisions, detect regressions, and deliver an audit report.",
        "pricing_hypothesis_usd": [3000, 10000],
        "note": "Most aligned with observable traceability, evaluation and drift monitoring; differentiation must be demonstrated."
    },
    "Inter-IA orchestration layer": {
        "scores": {"buyer_pain": 4.0, "mvp_speed": 3.0, "measurable_roi": 4.0,
                   "differentiation": 4.5, "repeatability": 4.0, "sales_access": 3.0,
                   "delivery_ease": 2.5, "evidence_fit": 3.0},
        "offer": "Pilot coordinating two or more model providers with routing, fallback, cost/quality logging and evaluation.",
        "pricing_hypothesis_usd": [5000, 20000],
        "note": "Potentially differentiated, but integrations and vendor dependencies increase delivery risk."
    },
    "Adaptive learning / drift recovery module": {
        "scores": {"buyer_pain": 3.5, "mvp_speed": 3.0, "measurable_roi": 4.0,
                   "differentiation": 4.0, "repeatability": 3.5, "sales_access": 2.5,
                   "delivery_ease": 2.5, "evidence_fit": 2.5},
        "offer": "Offline benchmark and shadow-mode pilot measuring recovery after drift against strong baselines.",
        "pricing_hypothesis_usd": [4000, 15000],
        "note": "Strong technical thesis, but needs real-data evidence before making performance claims."
    }
}
WEIGHTS = {"buyer_pain": .18, "mvp_speed": .16, "measurable_roi": .17,
           "differentiation": .12, "repeatability": .12, "sales_access": .10,
           "delivery_ease": .07, "evidence_fit": .08}

def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def weighted_score(scores, weights=WEIGHTS):
    return sum(scores[k] * weights[k] for k in weights)

def run(seed=SEED, n_sim=N_SIM):
    rng = random.Random(seed)
    base = {name: weighted_score(v["scores"]) for name, v in HYPOTHESES.items()}
    wins = {name: 0 for name in HYPOTHESES}
    ranks = {name: [] for name in HYPOTHESES}
    for _ in range(n_sim):
        trial = {}
        for name, item in HYPOTHESES.items():
            noisy = {k: max(1.0, min(5.0, val + rng.uniform(-0.6, 0.6)))
                     for k, val in item["scores"].items()}
            trial[name] = weighted_score(noisy)
        winner = max(trial, key=trial.get)
        wins[winner] += 1
        order = sorted(trial, key=trial.get, reverse=True)
        for rank, name in enumerate(order, 1):
            ranks[name].append(rank)
    rows = []
    for name, item in HYPOTHESES.items():
        rows.append({"hypothesis": name, "weighted_score_1_to_5": round(base[name], 3),
                     "win_rate_under_score_perturbation": round(wins[name]/n_sim, 4),
                     "mean_rank_under_perturbation": round(statistics.mean(ranks[name]), 3),
                     "offer": item["offer"], "pricing_hypothesis_usd_not_validated": item["pricing_hypothesis_usd"],
                     "interpretation": item["note"]})
    rows.sort(key=lambda x: x["weighted_score_1_to_5"], reverse=True)
    report = {
        "version": VERSION, "method": "Weighted decision rubric + Monte Carlo perturbation sensitivity analysis",
        "seed": seed, "simulations": n_sim, "rubric_weights": WEIGHTS, "candidate_results": rows,
        "recommended_first_experiment": rows[0]["hypothesis"],
        "decision": "Prioritize the AI evaluation + audit observatory as the first paid pilot hypothesis; validate with buyer interviews and paid-pilot conversion before claiming commercial traction.",
        "next_30_day_test": [
            "Interview 10 target buyers who own production AI workflows.",
            "Offer a narrowly scoped paid diagnostic to at least 3 qualified prospects.",
            "Measure outreach-to-meeting, meeting-to-pilot, delivery hours, gross margin, and whether the buyer renews or expands.",
            "Reject or revise the offer if buyers will not pay; do not treat interest or this model score as revenue evidence."
        ],
        "limitations": [
            "Scores, weights, and pricing ranges are unvalidated assumptions authored for prioritization, not observed market data.",
            "Monte Carlo tests sensitivity to subjective scores; it does not estimate real market probabilities.",
            "No revenue, customer demand, defensibility, patentability, or uniqueness is proven.",
            "The model favors a testable entry product, not a valuation of CEUNIA as a whole."
        ]
    }
    report["report_sha256"] = sha(report)
    return report

if __name__ == "__main__":
    result = run()
    out = Path(__file__).with_name("ceunia_commercial_metacode_v04_report.json")
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nREPORT_PATH={out}")
