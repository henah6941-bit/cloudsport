import pytest
from types import SimpleNamespace
from app.predictions import RulePredictionEngine

def test_rule_engine_returns_phase_one_markets():
    result = RulePredictionEngine().predict(SimpleNamespace(home_form=.8, away_form=.4, home_goals_avg=1.8, away_goals_avg=1.0))
    assert {item.market for item in result} == {"match_winner", "over_under_goals"}
    assert result[0].selection == "Home"

def test_rule_engine_has_safe_defaults():
    result = RulePredictionEngine().predict(SimpleNamespace(home_form=None, away_form=None, home_goals_avg=None, away_goals_avg=None))
    assert len(result) == 2
    assert all(.5 <= item.confidence <= .85 for item in result)
