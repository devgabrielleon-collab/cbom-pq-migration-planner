from cbom_pq_migration_planner.parsers import parse_cyclonedx_bom, parse_code_scan_report, parse_surface_scan_report


def test_parse_cyclonedx_bom():
    assets = parse_cyclonedx_bom('samples/cyclonedx_cbom.json', 'System', 'Owner')
    assert len(assets) >= 4
    assert any(asset.asset_type == 'protocol' for asset in assets)


def test_parse_code_scan_report():
    assets = parse_code_scan_report('samples/pq_ready_report.json', 'System', 'Owner')
    assert len(assets) == 2
    assert assets[0].source == 'code-scan'


def test_parse_surface_scan_report():
    assets = parse_surface_scan_report('samples/pq_surface_report.json', 'System', 'Owner')
    assert len(assets) >= 2
    assert any(asset.exposure == 'public' for asset in assets)
