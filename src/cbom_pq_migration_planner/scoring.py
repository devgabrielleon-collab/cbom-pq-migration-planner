from __future__ import annotations

from collections import Counter
from typing import Iterable, Tuple

from .knowledge import classify_posture
from .models import BuildSummary, CryptoAsset


EXPOSURE_POINTS = {
    'public': 25,
    'partner': 18,
    'internal': 10,
    'private': 10,
    'embedded': 15,
    'unknown': 8,
}
CRITICALITY_POINTS = {'critical': 25, 'high': 20, 'medium': 12, 'low': 5}
SENSITIVITY_POINTS = {'high': 15, 'medium': 8, 'low': 2}
AGILITY_POINTS = {'low': 10, 'medium': 5, 'high': 0}
POSTURE_POINTS = {
    'quantum-vulnerable': 35,
    'legacy-but-not-pqc-primary': 20,
    'monitor': 8,
    'pqc-ready': 0,
    'unknown': 12,
}


def score_asset(asset: CryptoAsset) -> CryptoAsset:
    status, replacement, rationale = classify_posture(asset.algorithm_family or asset.protocol_type, asset.primitive)
    asset.pq_status = status
    asset.recommended_replacement = replacement
    asset.rationale = rationale

    score = 0
    score += POSTURE_POINTS.get(status, 10)
    score += EXPOSURE_POINTS.get((asset.exposure or 'unknown').lower(), 8)
    score += CRITICALITY_POINTS.get((asset.criticality or 'medium').lower(), 12)
    score += SENSITIVITY_POINTS.get((asset.data_sensitivity or 'medium').lower(), 8)
    score += AGILITY_POINTS.get((asset.crypto_agility or 'medium').lower(), 5)
    if asset.long_lived_data:
        score += 10
    if (asset.state or '').lower() in {'compromised', 'expired', 'revoked'}:
        score += 15
    if asset.key_size and asset.key_size < 2048 and 'RSA' in (asset.algorithm_family or ''):
        score += 5

    asset.risk_score = max(0, min(score, 100))
    if asset.risk_score >= 70:
        asset.risk_level = 'high'
    elif asset.risk_score >= 40:
        asset.risk_level = 'medium'
    else:
        asset.risk_level = 'low'
    return asset


def build_summary(assets: Iterable[CryptoAsset]) -> BuildSummary:
    assets_list = list(assets)
    return BuildSummary(
        total_assets=len(assets_list),
        by_risk_level=dict(Counter(asset.risk_level for asset in assets_list)),
        by_pq_status=dict(Counter(asset.pq_status for asset in assets_list)),
        by_migration_wave=dict(Counter(asset.migration_wave for asset in assets_list)),
    )
