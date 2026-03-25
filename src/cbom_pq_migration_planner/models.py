from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class CryptoAsset:
    asset_id: str
    source: str
    source_ref: str
    system_name: str
    owner: str
    asset_name: str
    asset_type: str
    component_name: str = ""
    algorithm_family: str = ""
    primitive: str = ""
    protocol_type: str = ""
    version: str = ""
    key_type: str = ""
    key_size: int = 0
    state: str = "unknown"
    issuer: str = ""
    subject: str = ""
    exposure: str = "internal"
    criticality: str = "medium"
    data_sensitivity: str = "medium"
    crypto_agility: str = "medium"
    long_lived_data: bool = False
    pq_status: str = "unknown"
    recommended_replacement: str = ""
    rationale: str = ""
    risk_score: int = 0
    risk_level: str = "unscored"
    migration_wave: str = "unassigned"
    target_milestone: str = ""
    evidence: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BuildSummary:
    total_assets: int
    by_risk_level: Dict[str, int]
    by_pq_status: Dict[str, int]
    by_migration_wave: Dict[str, int]


@dataclass
class BuildResult:
    summary: BuildSummary
    assets: List[CryptoAsset]
    milestones: Dict[str, List[Dict[str, Any]]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": {
                "total_assets": self.summary.total_assets,
                "by_risk_level": self.summary.by_risk_level,
                "by_pq_status": self.summary.by_pq_status,
                "by_migration_wave": self.summary.by_migration_wave,
            },
            "assets": [asset.to_dict() for asset in self.assets],
            "milestones": self.milestones,
        }
