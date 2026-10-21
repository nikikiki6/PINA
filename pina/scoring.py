from dataclasses import dataclass
from typing import Dict

@dataclass
class ScoringWeights:
    step_weight: float = 0.15
    length_weight: float = 0.15
    nav_error_weight: float = 0.2
    oracle_error_weight: float = 0.2
    spl_weight: float = 0.1
    sr_weight: float = 0.1
    oracle_sr_weight: float = 0.1

    def __post_init__(self):
        total = self.step_weight + self.length_weight + self.nav_error_weight + self.oracle_error_weight + self.spl_weight + self.sr_weight + self.oracle_sr_weight
        if abs(total - 1.0) > 0.01:
            pass

@dataclass
class ScoringBaselines:
    step_baseline: float = 5.0
    length_baseline: float = 5.0
    error_baseline: float = 10.0
    success_baseline: float = 50.0
    quality_baseline: float = 50.0
DEFAULT_WEIGHTS = ScoringWeights()
DEFAULT_BASELINES = ScoringBaselines()
AGGRESSIVE_ATTACK_WEIGHTS = ScoringWeights(step_weight=0.1, length_weight=0.1, nav_error_weight=0.3, oracle_error_weight=0.3, spl_weight=0.05, sr_weight=0.075, oracle_sr_weight=0.075)
CONSERVATIVE_ATTACK_WEIGHTS = ScoringWeights(step_weight=0.2, length_weight=0.2, nav_error_weight=0.15, oracle_error_weight=0.15, spl_weight=0.15, sr_weight=0.075, oracle_sr_weight=0.075)
SCORING_CONFIGS = {'default': (DEFAULT_WEIGHTS, DEFAULT_BASELINES), 'aggressive': (AGGRESSIVE_ATTACK_WEIGHTS, DEFAULT_BASELINES), 'conservative': (CONSERVATIVE_ATTACK_WEIGHTS, DEFAULT_BASELINES)}

def get_scoring_config(config_name: str='default'):
    if config_name not in SCORING_CONFIGS:
        config_name = 'default'
    return SCORING_CONFIGS[config_name]
