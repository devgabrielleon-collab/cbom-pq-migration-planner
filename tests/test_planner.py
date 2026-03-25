from cbom_pq_migration_planner.models import CryptoAsset
from cbom_pq_migration_planner.planner import assign_migration_wave
from cbom_pq_migration_planner.scoring import score_asset


def test_wave_assignment_for_high_risk_asset():
    asset = CryptoAsset(
        asset_id='1',
        source='test',
        source_ref='-',
        system_name='S',
        owner='O',
        asset_name='Public RSA TLS',
        asset_type='certificate',
        algorithm_family='RSA',
        primitive='signature',
        exposure='public',
        criticality='high',
        data_sensitivity='high',
        long_lived_data=True,
    )
    asset = assign_migration_wave(score_asset(asset))
    assert asset.migration_wave.startswith('Wave 1')
