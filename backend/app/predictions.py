from dataclasses import dataclass
from .models import Fixture

@dataclass
class PredictionResult:
    market: str
    selection: str
    confidence: float
    explanation: str

class RulePredictionEngine:
    version = "rules-v1"

    def predict(self, fixture: Fixture) -> list[PredictionResult]:
        hf = fixture.home_form if fixture.home_form is not None else 0.5
        af = fixture.away_form if fixture.away_form is not None else 0.5
        hg = fixture.home_goals_avg if fixture.home_goals_avg is not None else 1.35
        ag = fixture.away_goals_avg if fixture.away_goals_avg is not None else 1.05
        home_score = hf + 0.08
        away_score = af
        if abs(home_score - away_score) < 0.08:
            winner, margin = "Draw", abs(home_score - away_score)
        elif home_score > away_score:
            winner, margin = "Home", home_score - away_score
        else:
            winner, margin = "Away", away_score - home_score
        winner_confidence = min(0.85, max(0.50, 0.50 + margin * 0.65))
        total = hg + ag
        threshold = 2.5
        ou = "Over 2.5" if total >= threshold else "Under 2.5"
        ou_confidence = min(0.82, max(0.50, 0.50 + abs(total - threshold) * 0.12))
        return [
            PredictionResult("match_winner", winner, round(winner_confidence, 3), f"Form and home advantage produce {winner.lower()} as the highest-scoring outcome."),
            PredictionResult("over_under_goals", ou, round(ou_confidence, 3), f"Estimated combined goals are {total:.2f}, compared with the 2.5-goal threshold."),
        ]
