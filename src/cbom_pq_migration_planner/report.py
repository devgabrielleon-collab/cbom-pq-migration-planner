from __future__ import annotations

import json
from pathlib import Path
from jinja2 import Environment, BaseLoader, select_autoescape

from .models import BuildResult


HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CBOM PQ Migration Planner</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; color: #1f2937; }
    h1, h2 { margin-bottom: 0.3rem; }
    .cards { display: grid; grid-template-columns: repeat(4, minmax(180px, 1fr)); gap: 12px; margin: 20px 0; }
    .card { border: 1px solid #d1d5db; border-radius: 12px; padding: 16px; }
    .muted { color: #6b7280; }
    table { width: 100%; border-collapse: collapse; margin-top: 18px; }
    th, td { border: 1px solid #e5e7eb; padding: 10px; text-align: left; font-size: 14px; }
    th { background: #f9fafb; }
    .high { color: #b91c1c; font-weight: bold; }
    .medium { color: #92400e; font-weight: bold; }
    .low { color: #065f46; font-weight: bold; }
    code { background: #f3f4f6; padding: 2px 6px; border-radius: 6px; }
  </style>
</head>
<body>
  <h1>CBOM PQ Migration Planner</h1>
  <p class="muted">Cryptographic inventory and post-quantum migration roadmap</p>

  <div class="cards">
    <div class="card"><div class="muted">Total assets</div><div><strong>{{ result.summary.total_assets }}</strong></div></div>
    <div class="card"><div class="muted">High risk</div><div><strong>{{ result.summary.by_risk_level.get('high', 0) }}</strong></div></div>
    <div class="card"><div class="muted">Quantum-vulnerable</div><div><strong>{{ result.summary.by_pq_status.get('quantum-vulnerable', 0) }}</strong></div></div>
    <div class="card"><div class="muted">Wave 1</div><div><strong>{{ result.summary.by_migration_wave.get('Wave 1 — by 2028', 0) }}</strong></div></div>
  </div>

  <h2>Milestones</h2>
  {% for wave, items in result.milestones.items() %}
    <h3>{{ wave }}</h3>
    <table>
      <thead>
        <tr>
          <th>Asset</th>
          <th>Algorithm / Protocol</th>
          <th>Score</th>
          <th>Replacement</th>
        </tr>
      </thead>
      <tbody>
      {% for item in items %}
        <tr>
          <td>{{ item.asset_name }}</td>
          <td>{{ item.algorithm_family }}</td>
          <td>{{ item.risk_score }}</td>
          <td>{{ item.recommended_replacement }}</td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  {% endfor %}

  <h2>Asset inventory</h2>
  <table>
    <thead>
      <tr>
        <th>Asset</th>
        <th>Source</th>
        <th>Type</th>
        <th>Algorithm / Protocol</th>
        <th>Risk</th>
        <th>Wave</th>
      </tr>
    </thead>
    <tbody>
    {% for asset in result.assets %}
      <tr>
        <td>{{ asset.asset_name }}</td>
        <td>{{ asset.source }}</td>
        <td>{{ asset.asset_type }}</td>
        <td>{{ asset.algorithm_family or asset.protocol_type }}</td>
        <td class="{{ asset.risk_level }}">{{ asset.risk_level }} ({{ asset.risk_score }})</td>
        <td>{{ asset.migration_wave }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""


def write_outputs(output_dir: str | Path, result: BuildResult, executive_summary: str) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    with open(out / 'inventory.json', 'w', encoding='utf-8') as f:
        json.dump([asset.to_dict() for asset in result.assets], f, indent=2, ensure_ascii=False)

    with open(out / 'migration_plan.json', 'w', encoding='utf-8') as f:
        json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

    with open(out / 'executive_summary.md', 'w', encoding='utf-8') as f:
        f.write(executive_summary)

    env = Environment(loader=BaseLoader(), autoescape=select_autoescape())
    template = env.from_string(HTML_TEMPLATE)
    rendered = template.render(result=result.to_dict())
    with open(out / 'dashboard.html', 'w', encoding='utf-8') as f:
        f.write(rendered)
