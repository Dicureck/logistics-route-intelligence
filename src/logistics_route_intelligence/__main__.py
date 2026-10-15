"""python -m logistics_route_intelligence demo --out-dir path"""
import argparse
from pathlib import Path
from .core import make_deliveries, enrich, summarize
from .report import render_html

def main(argv=None):
    parser = argparse.ArgumentParser(description="Reproducible, fictional route KPI laboratory")
    parser.add_argument("command",choices=["demo"])
    parser.add_argument("--out-dir",default="build/demo")
    parser.add_argument("--rows",type=int,default=1200)
    parser.add_argument("--seed",type=int,default=2026)
    args=parser.parse_args(argv)
    destination=Path(args.out_dir)
    destination.mkdir(parents=True,exist_ok=True)
    raw=make_deliveries(n=args.rows,seed=args.seed)
    enriched=enrich(raw)
    summary=summarize(enriched)
    raw.to_csv(destination/"synthetic_deliveries.csv",index=False,float_format="%.6f")
    summary.to_csv(destination/"zone_kpis.csv",index=False,float_format="%.4f")
    render_html(summary,destination/"dashboard.html")
    print(f"Synthetic demo: {len(raw)} deliveries; output: {destination}")

if __name__=="__main__":main()
