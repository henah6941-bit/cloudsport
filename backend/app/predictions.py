from dataclasses import dataclass
from .models import Fixture

@dataclass(frozen=True)
class PredictionResult:
    market: str
    selection: str
    confidence: float
    explanation: str


class PredictionProvider:
    name = "base"
    version = "base-v1"

    def predict(self, fixture: Fixture) -> list[PredictionResult]:
        raise NotImplementedError


class RulePredictionEngine(PredictionProvider):
    name = "rules"
    version = "rules-v1"

    def predict(self, fixture: Fixture) -> list[PredictionResult]:
        hf = fixture.home_form if fixture.home_form is not None else 0.5
        af = fixture.away_form if fixture.away_form is not None else 0.5
        hg = fixture.home_goals_avg if fixture.home_goals_avg is not None else 1.35
        ag = fixture.away_goals_avg if fixture.away_goals_avg is not None else 1.05
        home_score, away_score = hf + 0.08, af
        if abs(home_score - away_score) < 0.08:
            winner, margin = "Draw", abs(home_score - away_score)
        elif home_score > away_score:
            winner, margin = "Home", home_score - away_score
        else:
            winner, margin = "Away", away_score - home_score
        total = hg + ag
        return [
            PredictionResult("match_winner", winner, round(min(0.85, max(0.50, 0.50 + margin * 0.65)), 3), f"Form and home advantage produce {winner.lower()} as the highest-scoring outcome."),
            PredictionResult("over_under_goals", "Over 2.5" if total >= 2.5 else "Under 2.5", round(min(0.82, max(0.50, 0.50 + abs(total - 2.5) * 0.12)), 3), f"Estimated combined goals are {total:.2f}, compared with the 2.5-goal threshold."),
        ]


class AnthropicPredictionProvider(PredictionProvider):
    """Reserved adapter boundary; intentionally unavailable until Phase 2 billing/configuration."""
    name = "anthropic"
    version = "anthropic-disabled"

    def predict(self, fixture: Fixture) -> list[PredictionResult]:
        raise RuntimeError("Anthropic provider is disabled in Phase 1")
