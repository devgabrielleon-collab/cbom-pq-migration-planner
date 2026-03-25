# CBOM PQ Migration Planner 🔐

[![CI](https://github.com/devgabrielleon-collab/cbom-pq-migration-planner/workflows/CI/badge.svg)](https://github.com/devgabrielleon-collab/cbom-pq-migration-planner/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Overview

**CBOM PQ Migration Planner** is an enterprise-grade tool designed to help organizations transition from quantum-vulnerable cryptography to post-quantum cryptography (PQC). It ingests **CycloneDX Software/Cryptographic Bill of Materials (SBOM/CBOM)** plus external security scan reports and produces actionable migration roadmaps aligned with NIST and NCSC guidance.

### Key Outputs

- **Normalized Cryptographic Inventory**: Unified view of all cryptographic assets across your infrastructure
- **Risk-Scored Asset List**: Prioritized assets based on exposure, environment, and data sensitivity
- **Post-Quantum Migration Roadmap**: Phased migration plan aligned with NCSC milestones (2028, 2031, 2035)
- **Executive Summary**: High-level overview for stakeholders and decision-makers
- **Interactive Dashboard**: HTML-based visualization of migration progress and asset distribution

## 🎯 Why This Project Matters

The quantum computing threat to cryptography is no longer theoretical. Organizations must begin **cryptographic discovery and inventory** to understand where quantum-vulnerable public-key cryptography is deployed and prioritize migration efforts.

### NIST & NCSC Alignment

- **2028**: Discovery, assessment, and initial migration plan
- **2031**: Highest-priority migration activities
- **2035**: Complete migration to PQC for all systems, services, and products

This tool automates the discovery and planning phases, reducing time-to-action and improving accuracy.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/devgabrielleon-collab/cbom-pq-migration-planner.git
cd cbom-pq-migration-planner

# Install dependencies
pip install -e .
```

### Usage

```bash
# Basic usage with a CycloneDX CBOM
cbomplan plan --cbom path/to/cbom.json

# Include code discovery and surface audit reports
cbomplan plan \
  --cbom path/to/cbom.json \
  --code-discovery path/to/code-discovery.json \
  --surface-audit path/to/surface-audit.json

# Generate all outputs
cbomplan plan --cbom path/to/cbom.json --output-dir ./migration-plan
```

### Outputs

After running the tool, you'll find:

- `inventory.json` - Complete cryptographic asset inventory
- `migration_plan.json` - Phased migration strategy
- `executive_summary.md` - Stakeholder-ready summary
- `dashboard.html` - Interactive visualization

## 📊 Features

- **Cryptographic Asset Extraction**: Automatically identifies algorithms, keys, and certificates
- **Algorithm Normalization**: Standardizes cryptographic nomenclature across sources
- **Quantum Exposure Classification**: Categorizes assets by quantum vulnerability level
- **Risk Scoring**: Multi-factor risk assessment (environment, exposure, data sensitivity, crypto agility)
- **Migration Wave Assignment**: Intelligently groups assets into migration phases
- **Multi-Format Output**: JSON, Markdown, and HTML for different stakeholder needs

## 🔧 Development

### Running Tests

```bash
pytest tests/ -v
```

### Project Structure

```
cbom-pq-migration-planner/
├── src/cbom_pq_migration_planner/
│   ├── cli.py                 # Command-line interface
│   ├── planner.py             # Core migration planning logic
│   ├── models.py              # Data models
│   ├── risk_scorer.py         # Risk assessment engine
│   └── reporters.py           # Output generation
├── tests/                     # Test suite
├── samples/                   # Example CBOM and scan reports
└── pyproject.toml            # Project configuration
```

## 📚 Integration with Other Tools

This tool works seamlessly with:

- **pq-ready-code-scanner**: Detects quantum-vulnerable code patterns
- **pq-surface-audit**: Audits cryptographic surface exposure
- **CycloneDX**: Industry-standard SBOM/CBOM format

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🔗 Resources

- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography/)
- [CycloneDX CBOM Specification](https://cyclonedx.org/capabilities/cbom/)
- [NCSC Quantum-Safe Transition Guidance](https://www.ncsc.gov.uk/collection/quantum-safe-transition-principles)

## 📧 Support

For issues, questions, or suggestions, please open an [issue](https://github.com/devgabrielleon-collab/cbom-pq-migration-planner/issues) on GitHub.
