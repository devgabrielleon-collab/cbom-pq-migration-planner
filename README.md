# cbom-pq-migration-planner

A portfolio-ready, enterprise-style project that ingests **CycloneDX SBOM/CBOM** plus external scan reports and produces:

- a **normalized cryptographic inventory**
- a **risk-scored asset list**
- a **post-quantum migration roadmap**
- an **executive summary**
- a **dashboard-style HTML report**

## Why this project matters

NIST and the NCCoE recommend that organizations begin with **cryptographic discovery and inventory** so they can understand where quantum-vulnerable public-key cryptography is used and prioritize migration roadmaps. citeturn737378view0turn737378view2

CycloneDX CBOM is designed to represent cryptographic assets such as **algorithms, keys, certificates, and their relationships to software components**, which makes it a natural input format for this workflow. citeturn737378view1turn843457search2

The roadmap defaults in this project align with the NCSC's milestone guidance:
- by **2028**: discovery, assessment, and an initial migration plan
- by **2031**: highest-priority migration activities
- by **2035**: complete migration to PQC for all systems, services, and products. citeturn739029search0turn739029search4

## What the tool does

`cbomplan` reads:
- a **CycloneDX BOM** (SBOM or CBOM)
- an optional **code-discovery report** (for example from `pq-ready-code-scanner`)
- an optional **surface audit report** (for example from `pq-surface-audit`)

It then:
1. extracts cryptographic assets
2. normalizes algorithms and protocols
3. classifies quantum exposure
4. scores asset risk using environment, exposure, data sensitivity, and crypto agility
5. assigns assets to migration waves
6. generates JSON, Markdown, and HTML outputs

## Outputs

Running the tool produces:
- `inventory.json`
- `migration_plan.json`
- `executive_summary.md`
- `dashboard.html`

## Install

```bash
pip install -e .[dev]
```

## Quick start

```bash
cbomplan build   --sbom ./samples/cyclonedx_cbom.json   --code-scan ./samples/pq_ready_report.json   --surface-scan ./samples/pq_surface_report.json   --system-name "NovaBank Identity Gateway"   --owner "Security Architecture"   --output ./out
```

## Run tests

```bash
pytest -q
```

## Project structure

```text
cbom-pq-migration-planner/
├─ src/cbom_pq_migration_planner/
│  ├─ cli.py
│  ├─ models.py
│  ├─ knowledge.py
│  ├─ parsers.py
│  ├─ scoring.py
│  ├─ planner.py
│  └─ report.py
├─ samples/
├─ tests/
├─ out/
└─ .github/workflows/
```

## Supported inputs

### CycloneDX BOM
The parser supports practical subsets of CycloneDX 1.6+ and 1.7 cryptographic objects such as:
- `cryptographic-asset` components
- `cryptoProperties.assetType = algorithm`
- `certificate`
- `protocol`
- `related-crypto-material`

### Code scan report
Expected shape:

```json
{
  "findings": [
    {
      "title": "RSA public key usage",
      "algorithm": "RSA-2048",
      "category": "signature",
      "severity": "high",
      "file": "src/auth.py",
      "line": 44
    }
  ]
}
```

### Surface scan report
Expected shape:

```json
{
  "assets": [
    {
      "target": "api.example.com:443",
      "service_type": "https",
      "exposure": "public",
      "criticality": "high",
      "data_sensitivity": "high",
      "tls": {
        "version": "TLSv1.2",
        "cipher": "ECDHE-RSA-AES256-GCM-SHA384",
        "certificate": {
          "public_key_algorithm": "RSA",
          "public_key_size": 2048,
          "signature_algorithm": "sha256WithRSAEncryption",
          "issuer": "Example CA"
        }
      }
    }
  ]
}
```

## Notes

- This is a **defensive planning tool**, not an exploit framework.
- It helps teams create visibility and a migration backlog.
- NIST's principal PQC standards now include **FIPS 203 (ML-KEM)**, **FIPS 204 (ML-DSA)**, and **FIPS 205 (SLH-DSA)**. citeturn737378view3turn311489search6turn311489search9turn311489search18

## Disclaimer

This project is educational and portfolio-oriented. It should support, not replace, a full enterprise cryptographic inventory program.
