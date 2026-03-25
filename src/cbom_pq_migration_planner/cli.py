from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from .models import BuildResult
from .parsers import parse_cyclonedx_bom, parse_code_scan_report, parse_surface_scan_report
from .planner import assign_migration_wave, build_executive_summary, build_milestones
from .report import write_outputs
from .scoring import build_summary, score_asset


app = typer.Typer(help='Generate cryptographic inventory and PQC migration roadmap.')


@app.callback()
def main() -> None:
    """CBOM PQ migration planning CLI."""
    return None



@app.command()
def build(
    sbom: str = typer.Option(..., help='Path to CycloneDX SBOM/CBOM JSON file.'),
    code_scan: Optional[str] = typer.Option(None, help='Optional code scan report JSON.'),
    surface_scan: Optional[str] = typer.Option(None, help='Optional surface scan report JSON.'),
    system_name: str = typer.Option('Unknown System', help='System or service name.'),
    owner: str = typer.Option('Unknown Owner', help='Owning team or business unit.'),
    output: str = typer.Option('./out', help='Output directory.'),
) -> None:
    assets = []
    assets.extend(parse_cyclonedx_bom(sbom, system_name, owner))
    if code_scan:
        assets.extend(parse_code_scan_report(code_scan, system_name, owner))
    if surface_scan:
        assets.extend(parse_surface_scan_report(surface_scan, system_name, owner))

    scored_assets = [assign_migration_wave(score_asset(asset)) for asset in assets]
    scored_assets.sort(key=lambda a: a.risk_score, reverse=True)

    result = BuildResult(
        summary=build_summary(scored_assets),
        assets=scored_assets,
        milestones=build_milestones(scored_assets),
    )
    executive_summary = build_executive_summary(scored_assets)
    write_outputs(output, result, executive_summary)
    typer.echo(f'Wrote outputs to {Path(output).resolve()}')


if __name__ == '__main__':
    app()
