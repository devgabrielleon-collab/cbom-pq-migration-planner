from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from .models import CryptoAsset


WAVE_1 = 'Wave 1 — by 2028'
WAVE_2 = 'Wave 2 — by 2031'
WAVE_3 = 'Wave 3 — by 2035'
MONITOR = 'Monitor / already aligned'


def assign_migration_wave(asset: CryptoAsset) -> CryptoAsset:
    if asset.pq_status == 'pqc-ready':
        asset.migration_wave = MONITOR
        asset.target_milestone = 'Validate interoperability and monitor policy updates'
        return asset
    if asset.risk_score >= 70:
        asset.migration_wave = WAVE_1
        asset.target_milestone = 'Discovery complete and high-priority backlog planned by 2028'
    elif asset.risk_score >= 40:
        asset.migration_wave = WAVE_2
        asset.target_milestone = 'Execute priority migrations and refine roadmap by 2031'
    else:
        asset.migration_wave = WAVE_3
        asset.target_milestone = 'Complete remaining migrations by 2035'
    return asset


def build_milestones(assets: List[CryptoAsset]) -> Dict[str, List[dict]]:
    grouped: Dict[str, List[dict]] = defaultdict(list)
    for asset in assets:
        grouped[asset.migration_wave].append({
            'asset_id': asset.asset_id,
            'asset_name': asset.asset_name,
            'algorithm_family': asset.algorithm_family,
            'risk_level': asset.risk_level,
            'risk_score': asset.risk_score,
            'recommended_replacement': asset.recommended_replacement,
            'owner': asset.owner,
            'system_name': asset.system_name,
        })

    for items in grouped.values():
        items.sort(key=lambda row: row['risk_score'], reverse=True)
    return dict(grouped)


def build_executive_summary(assets: List[CryptoAsset]) -> str:
    high = [a for a in assets if a.migration_wave == WAVE_1]
    medium = [a for a in assets if a.migration_wave == WAVE_2]
    low = [a for a in assets if a.migration_wave == WAVE_3]
    aligned = [a for a in assets if a.migration_wave == MONITOR]

    lines = [
        '# Executive Summary',
        '',
        f'- Total cryptographic assets normalized: **{len(assets)}**',
        f'- Wave 1 assets (to 2028): **{len(high)}**',
        f'- Wave 2 assets (to 2031): **{len(medium)}**',
        f'- Wave 3 assets (to 2035): **{len(low)}**',
        f'- Monitor/aligned assets: **{len(aligned)}**',
        '',
        '## Recommended program shape',
        '',
        '1. Finish discovery and owner mapping for all Wave 1 assets.',
        '2. Start design decisions for ML-KEM, ML-DSA, SLH-DSA, or hybrid adoption paths where appropriate.',
        '3. Track vendor readiness and interoperability constraints for externally managed systems.',
        '4. Use the inventory as a living artifact inside broader cyber risk and architecture governance.',
        '',
        '## Highest-priority items',
        '',
    ]
    for asset in sorted(high, key=lambda a: a.risk_score, reverse=True)[:10]:
        lines.append(f"- **{asset.asset_name}** — {asset.algorithm_family or asset.protocol_type} — score {asset.risk_score} — {asset.recommended_replacement}")
    if not high:
        lines.append('- No Wave 1 assets were detected in the current sample set.')
    lines.append('')
    return '\n'.join(lines)
