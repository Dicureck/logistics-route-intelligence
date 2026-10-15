<p align="center"><img src="assets/banner.svg" alt="Logistics & Route Intelligence | Melissa Castro" width="100%" /></p>

<p align="center">
  <a href="https://github.com/Dicureck/logistics-route-intelligence/actions/workflows/ci.yml"><img src="https://github.com/Dicureck/logistics-route-intelligence/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-111B32?logo=python&logoColor=53D6FF" alt="Python 3.10+"></img>
  <img src="https://img.shields.io/badge/pandas-data%20analysis-25213A?logo=pandas&logoColor=A68CFF" alt="pandas"></img>
  <img src="https://img.shields.io/badge/Data-100%25%20synthetic-113149" alt="All data synthetic"></img>
</p>

# Logistics & Route Intelligence

**An independent analytics engineering lab for fictional last-mile operations.** Generate deterministic delivery records, measure service-level performance, compare planned vs actual distance, assess simple coordinate-based geofences, and publish an offline HTML KPI dashboard.

> **Not a real client deployment.** All drivers, deliveries, dates, route IDs, coordinates and metrics are generated. This project demonstrates methodology; it makes no performance claims about any business.

## Synthetic dashboard preview

![Synthetic route KPI preview](assets/dashboard-preview.svg)

A [self-contained HTML example](examples/synthetic-dashboard.html) is included. The command below regenerates it from seed `2026`.

## Quick start

```bash
python -m venv .venv
# Activate your virtual environment for your operating system.
python -m pip install -e '.[dev]'
python -m pytest -q
python -m logistics_route_intelligence demo --rows 1200 --seed 2026 --out-dir build/demo
```

Open `build/demo/dashboard.html` locally. The generated directory also contains `synthetic_deliveries.csv` and `zone_kpis.csv`; generated files are not committed. For a different simulation, change the seed or row count.

## Architecture

```text
Synthetic generation (seed + schema)
    ↓
Raw deliveries CSV → enrichment → zone KPI aggregation
    ↓                                 ↓
Offline HTML dashboard         Power BI CSV import
```

## Engineering artifacts

| Artifact | What's inside |
|:--|:--|
| `src/logistics_route_intelligence/core.py` | Reproducible generation, Haversine distance and metrics |
| `src/logistics_route_intelligence/report.py` | Standalone HTML dashboard renderer |
| `tests/` | Determinism, referential integrity, SLA policy, geography checks |
| [Metric definitions](docs/metrics.md) | Explicit numerator/denominator contracts |
| [Power BI blueprint](docs/power-bi-blueprint.md) | Suggested model, DAX measures, report layout |
| [Engineering decisions](docs/design-notes.md) | Tradeoffs and scope boundaries |

## Interpretation guardrails

**On-time SLA denominator = all attempts, including unsuccessful deliveries.** A distance ratio is descriptive, not evidence of a causal improvement. Great-circle geofences are not street-network routes. Review [metric contracts](docs/metrics.md) before using the examples.

## Portfolio context

Designed by **Melissa Castro** as an original public demonstration of operational analytics methods. Not sourced from, representative of, or endorsed by any employer or client. MIT licensed.
