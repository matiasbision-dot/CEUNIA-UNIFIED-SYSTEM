"""
CEUNIA Core Validator

Version: 1.0
Purpose:
Evaluates outputs based on coherence, structure and minimal quality heuristics.
Later versions will integrate CEUNIA Metrics (Coherence, Potercia, PRE, etc.).
"""

def structural_score(text: str) -> float:
"""
Basic structural coherence proxy.
"""
if not text:
return 0.0

score = 0.0

# length contribution
score += min(len(text) / 200, 0.4)

# sentence structure heuristic
sentences = text.count(".") + text.count("!") + text.count("?")
score += min(sentences / 5, 0.3)

# basic richness heuristic
words = len(text.split())
score += min(words / 100, 0.3)

return round(min(score, 1.0), 2)

def validate(output: str) -> dict:
"""
Main CEUNIA validation function.
Returns coherence score and decision.
"""

score = structural_score(output)

if score >= 0.75:
    decision = "accept"
elif score >= 0.45:
    decision = "review"
else:
    decision = "reject"

return {
    "coherence": score,
    "decision": decision
}
