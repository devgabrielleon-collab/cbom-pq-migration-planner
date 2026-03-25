from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .knowledge import canonicalize_algorithm
from .models import CryptoAsset


def load_json(path: str | Path) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def parse_cyclonedx_bom(path: str | Path, system_name: str, owner: str) -> List[CryptoAsset]:
    data = load_json(path)
    components = data.get('components', [])
    assets: List[CryptoAsset] = []

    for index, component in enumerate(components, start=1):
        if component.get('type') != 'cryptographic-asset':
            continue
        cp = component.get('cryptoProperties', {}) or {}
        asset_type = cp.get('assetType', 'unknown')
        base = {
            'asset_id': component.get('bom-ref', f'cbom-{index}'),
            'source': 'cyclonedx',
            'source_ref': str(path),
            'system_name': system_name,
            'owner': owner,
            'asset_name': component.get('name', f'asset-{index}'),
            'asset_type': asset_type,
            'component_name': component.get('name', ''),
            'evidence': [f"CycloneDX component {component.get('name', f'asset-{index}')}"] ,
            'raw': component,
        }

        if asset_type == 'algorithm':
            ap = cp.get('algorithmProperties', {}) or {}
            assets.append(CryptoAsset(
                **base,
                algorithm_family=canonicalize_algorithm(ap.get('algorithmFamily', component.get('name', ''))),
                primitive=ap.get('primitive', ''),
                state=ap.get('executionEnvironment', 'unknown'),
            ))
        elif asset_type == 'protocol':
            pp = cp.get('protocolProperties', {}) or {}
            assets.append(CryptoAsset(
                **base,
                protocol_type=pp.get('type', component.get('name', '')),
                version=pp.get('version', ''),
                algorithm_family=canonicalize_algorithm(' '.join(pp.get('algorithms', []) if isinstance(pp.get('algorithms'), list) else [pp.get('algorithms', '')]).strip()),
                primitive='protocol',
            ))
        elif asset_type == 'certificate':
            cp2 = cp.get('certificateProperties', {}) or {}
            assets.append(CryptoAsset(
                **base,
                algorithm_family=canonicalize_algorithm(cp2.get('signatureAlgorithmRef', '') or cp2.get('signatureAlgorithm', '')),
                primitive='signature',
                issuer=cp2.get('issuer', ''),
                subject=cp2.get('subject', ''),
                state=cp2.get('state', 'active'),
            ))
        elif asset_type == 'related-crypto-material':
            rp = cp.get('relatedCryptoMaterialProperties', {}) or {}
            assets.append(CryptoAsset(
                **base,
                algorithm_family=canonicalize_algorithm(component.get('name', '')),
                key_type=rp.get('type', ''),
                key_size=int(rp.get('size', 0) or 0),
                state=rp.get('state', 'unknown'),
                primitive='key-material',
            ))
        else:
            assets.append(CryptoAsset(**base))

    return assets


def parse_code_scan_report(path: str | Path, system_name: str, owner: str) -> List[CryptoAsset]:
    data = load_json(path)
    findings = data.get('findings') or data.get('results') or []
    assets: List[CryptoAsset] = []
    for index, finding in enumerate(findings, start=1):
        algo = finding.get('algorithm') or finding.get('matched_text') or finding.get('title', '')
        category = finding.get('category', '')
        primitive = 'signature' if 'sign' in category.lower() else 'key-establishment' if 'key' in category.lower() or 'exchange' in category.lower() else category
        evidence = []
        if finding.get('file'):
            line = finding.get('line')
            evidence.append(f"{finding['file']}:{line}" if line else finding['file'])
        if finding.get('message'):
            evidence.append(finding['message'])
        assets.append(CryptoAsset(
            asset_id=f"code-{index}",
            source='code-scan',
            source_ref=str(path),
            system_name=system_name,
            owner=owner,
            asset_name=finding.get('title', f'code-finding-{index}'),
            asset_type='algorithm',
            component_name=finding.get('component', ''),
            algorithm_family=canonicalize_algorithm(algo),
            primitive=primitive,
            criticality=(finding.get('severity') or 'medium').lower(),
            evidence=evidence,
            raw=finding,
        ))
    return assets


def parse_surface_scan_report(path: str | Path, system_name: str, owner: str) -> List[CryptoAsset]:
    data = load_json(path)
    assets_in = data.get('assets', [])
    assets: List[CryptoAsset] = []
    counter = 1
    for record in assets_in:
        target = record.get('target', f'asset-{counter}')
        exposure = record.get('exposure', 'public')
        criticality = record.get('criticality', 'medium')
        sensitivity = record.get('data_sensitivity', 'medium')
        tls = record.get('tls', {}) or {}
        service_type = record.get('service_type', '')
        if service_type:
            assets.append(CryptoAsset(
                asset_id=f"surface-{counter}",
                source='surface-scan',
                source_ref=str(path),
                system_name=system_name,
                owner=owner,
                asset_name=target,
                asset_type='protocol',
                component_name=target,
                protocol_type=service_type,
                version=tls.get('version', ''),
                algorithm_family=canonicalize_algorithm(tls.get('cipher', '')),
                primitive='protocol',
                exposure=exposure,
                criticality=criticality,
                data_sensitivity=sensitivity,
                long_lived_data=bool(record.get('long_lived_data', False)),
                evidence=[f"Service {target}", _stringify(tls.get('cipher', ''))],
                raw=record,
            ))
            counter += 1
        cert = tls.get('certificate', {}) or {}
        if cert:
            assets.append(CryptoAsset(
                asset_id=f"surface-{counter}",
                source='surface-scan',
                source_ref=str(path),
                system_name=system_name,
                owner=owner,
                asset_name=f"{target} certificate",
                asset_type='certificate',
                component_name=target,
                algorithm_family=canonicalize_algorithm(cert.get('public_key_algorithm') or cert.get('signature_algorithm', '')),
                primitive='signature' if cert.get('signature_algorithm') else 'key-establishment',
                key_size=int(cert.get('public_key_size', 0) or 0),
                issuer=cert.get('issuer', ''),
                subject=cert.get('subject', ''),
                exposure=exposure,
                criticality=criticality,
                data_sensitivity=sensitivity,
                long_lived_data=bool(record.get('long_lived_data', False)),
                evidence=[f"Certificate for {target}", _stringify(cert)],
                raw=record,
            ))
            counter += 1
    return assets
