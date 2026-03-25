from cbom_pq_migration_planner.models import CryptoAsset
from cbom_pq_migration_planner.scoring import score_asset


def test_score_asset_quantum_vulnerable():
    asset = CryptoAsset(
        asset_id='1',
        source='test',
        source_ref='-',
        system_name='S',
        owner='O',
        asset_name='RSA signing',
        asset_type='algorithm',
        algorithm_family='RSA',
        primitive='signature',
        exposure='public',
        criticality='high',
        data_sensitivity='high',
    )
    scored = score_asset(asset)
    assert scored.pq_status == 'quantum-vulnerable'
    assert scored.risk_score >= 60
