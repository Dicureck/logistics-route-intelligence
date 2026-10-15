"""Portable self-contained HTML dashboard: data-driven, no external network calls."""
from html import escape
from pathlib import Path
import pandas as pd


def render_html(summary: pd.DataFrame, out: str | Path) -> None:
    if summary.empty:
        raise ValueError("No summary rows")
    cards = [
        ("DELIVERY ATTEMPTS", f"{int(summary['attempts'].sum()):,}"),
        ("SUCCESS RATE", f"{100 * summary['delivered'].sum()/summary['attempts'].sum():.1f}%"),
        ("ON-TIME / ATTEMPTS", f"{100 * summary['on_time'].sum()/summary['attempts'].sum():.1f}%"),
        ("ACTUAL / PLAN KM", f"{summary['actual_km'].sum()/summary['planned_km'].sum():.2f}x"),
    ]
    card_html = "".join(f'<section class="metric"><small>{escape(k)}</small><strong>{escape(v)}</strong></section>' for k,v in cards)
    bars = "".join(
        f'<div class="barrow"><span>{escape(str(z))}</span><div class="track"><div class="fill" style="width:{max(0,min(100,float(v))):.2f}%"></div></div><b>{float(v):.1f}%</b></div>'
        for z,v in zip(summary["zone"],summary["sla_on_time_pct"]))
    rows = "".join(f'<tr><td>{escape(str(x.zone))}</td><td>{int(x.attempts):,}</td><td>{float(x.delivery_success_pct):.1f}%</td><td>{float(x.geofence_coverage_pct):.1f}%</td><td>{float(x.distance_vs_plan_ratio):.2f}×</td></tr>' for x in summary.itertuples())
    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Route Intelligence | Synthetic Dashboard</title><style>
:root{{--bg:#080e1e;--panel:#14213a;--cyan:#51ddff;--violet:#a489ff;--text:#edf4ff}}*{{box-sizing:border-box}}body{{margin:0;background:linear-gradient(135deg,#080e1e,#15112d);color:var(--text);font:16px system-ui,Arial}}main{{max-width:1100px;margin:auto;padding:40px 20px}}h1{{font-size:clamp(28px,5vw,54px);margin:4px 0}}.accent{{color:var(--cyan)}}.subtitle,small{{color:#a4b7d5}}.pill{{color:var(--cyan);font-size:13px;letter-spacing:2px}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:28px 0}}.metric,.panel{{background:#14213ae6;border:1px solid #304568;border-radius:14px;padding:22px}}.metric strong{{font-size:32px;display:block;margin-top:12px;color:var(--cyan)}}.panel{{margin:20px 0}}.barrow{{display:grid;grid-template-columns:90px 1fr 65px;align-items:center;gap:16px;margin:17px 0}}.track{{height:14px;background:#22324e;border-radius:20px;overflow:hidden}}.fill{{height:100%;background:linear-gradient(90deg,var(--cyan),var(--violet))}}table{{width:100%;border-collapse:collapse}}td,th{{padding:12px;border-bottom:1px solid #344260;text-align:left}}th{{color:var(--cyan);font-size:12px}}.scroll{{overflow:auto}}footer{{margin:24px 0;color:#a4b7d5;font-size:13px}}
</style></head><body><main><p class="pill">MC // ENGINEERING LABS · OPERATIONS INTELLIGENCE</p><h1>Logistics <span class="accent">& Route Intelligence</span></h1><p class="subtitle">Deterministic, fully synthetic last-mile operations demonstration</p><div class="cards">{card_html}</div><section class="panel"><h2>SLA performance by zone</h2><p class="subtitle">Delivered within promise / all delivery attempts; unsuccessful attempts count as misses.</p>{bars}</section><section class="panel scroll"><h2>Operational breakdown</h2><table><thead><tr><th>ZONE</th><th>ATTEMPTS</th><th>DELIVERY SUCCESS</th><th>GEOFENCE COVERAGE</th><th>ACTUAL / PLAN KM</th></tr></thead><tbody>{rows}</tbody></table></section><footer>All data are synthetic. Geofence distances use Haversine, not street-network routing. No claims about real clients or real optimization outcomes.</footer></main></body></html>"""
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    Path(out).write_text(html,encoding="utf-8")
