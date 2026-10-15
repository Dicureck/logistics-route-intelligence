import pandas as pd
import pytest
from logistics_route_intelligence.core import ZONES, make_deliveries, enrich, haversine_km, summarize
from logistics_route_intelligence.report import render_html

def test_deterministic_generation():
    pd.testing.assert_frame_equal(make_deliveries(30,seed=1),make_deliveries(30,seed=1))

def test_unique_identifiers():
    assert make_deliveries(250).delivery_id.is_unique

def test_different_seeds():
    assert not make_deliveries(20,1).equals(make_deliveries(20,2))

def test_zero_rows_rejected():
    with pytest.raises(ValueError):make_deliveries(0)

def test_haversine_identity_and_symmetry():
    assert haversine_km(10,-70,10,-70)==0
    assert haversine_km(10,-70,11,-70)==pytest.approx(haversine_km(11,-70,10,-70))

def test_sla_denominator_includes_failures():
    base=make_deliveries(2)
    base.loc[0,"status"]="failed"
    base.loc[1,"status"]="delivered"
    base.loc[1,"actual_minutes"]=1
    base["zone"]="Central"
    x=summarize(enrich(base)).iloc[0]
    assert x.attempts==2 and x.on_time==1 and x.sla_on_time_pct==50

def test_geofence_center_included():
    x=make_deliveries(1)
    lat,lon=ZONES[x.loc[0,"zone"]]
    x.loc[0,"latitude"]=lat;x.loc[0,"longitude"]=lon
    assert bool(enrich(x).loc[0,"inside_geofence"])

def test_summary_counts_conserved():
    e=enrich(make_deliveries(500))
    assert int(summarize(e).attempts.sum())==500

def test_invalid_zone_rejected():
    df=make_deliveries(1);df.loc[0,"zone"]="Unknown"
    with pytest.raises(ValueError,match="zone"):enrich(df)

def test_html_contains_synthetic_disclaimer(tmp_path):
    path=tmp_path/"demo.html";render_html(summarize(enrich(make_deliveries(50))),path)
    assert "All data are synthetic" in path.read_text()
