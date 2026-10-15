"""Deterministic synthetic route dataset and explicitly-defined KPI calculations."""
from __future__ import annotations

from datetime import date, timedelta
from math import asin, cos, radians, sin, sqrt
from random import Random
import pandas as pd

ZONES = {"North": (10.035, -70.010), "Central": (10.000, -70.000),
         "South": (9.970, -69.985), "East": (10.005, -69.953)}
GEOFENCE_RADIUS_KM = 2.6


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in km using Earth's mean radius; not road distance."""
    dlat, dlon = radians(lat2-lat1), radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 6371.0088 * 2 * asin(min(1.0, sqrt(a)))


def make_deliveries(n: int = 1200, seed: int = 2026) -> pd.DataFrame:
    if n < 1:
        raise ValueError("n must be positive")
    rng = Random(seed)
    rows = []
    names = list(ZONES)
    for idx in range(n):
        zone = names[idx % len(names)]
        center = ZONES[zone]
        lat = center[0] + rng.uniform(-0.030, 0.030)
        lon = center[1] + rng.uniform(-0.030, 0.030)
        planned_km = round(rng.uniform(2, 24), 2)
        actual_km = round(planned_km * rng.uniform(0.93, 1.55), 2)
        promised_mins = rng.choice([30, 45, 60, 90])
        actual_mins = max(5, round(promised_mins * rng.uniform(0.62, 1.66)))
        delivered = rng.random() >= 0.07
        rows.append({
            "delivery_id": f"SYN-{idx+1:06d}",
            "service_date": str(date(2026, 1, 1) + timedelta(days=idx % 56)),
            "route_id": f"R{idx % 36 + 1:03d}",
            "driver_id": f"D{idx % 12 + 1:03d}",
            "zone": zone,
            "latitude": round(lat, 6), "longitude": round(lon, 6),
            "planned_km": planned_km, "actual_km": actual_km,
            "promised_minutes": promised_mins, "actual_minutes": actual_mins,
            "status": "delivered" if delivered else "failed",
        })
    return pd.DataFrame(rows)


def enrich(df: pd.DataFrame, radius_km: float = GEOFENCE_RADIUS_KM) -> pd.DataFrame:
    """Recompute features from raw columns; does not infer causal route improvements."""
    if radius_km <= 0:
        raise ValueError("radius_km must be positive")
    required = {"zone", "latitude", "longitude", "planned_km", "actual_km",
                "promised_minutes", "actual_minutes", "status"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if not df["zone"].isin(ZONES).all():
        raise ValueError("Unknown zone")
    if (df["planned_km"] <= 0).any() or (df["actual_km"] < 0).any():
        raise ValueError("Invalid distance")
    if (df["promised_minutes"] <= 0).any() or (df["actual_minutes"] < 0).any():
        raise ValueError("Invalid time")
    result = df.copy()
    result["is_delivered"] = result["status"].eq("delivered")
    result["is_on_time"] = result["is_delivered"] & result["actual_minutes"].le(result["promised_minutes"])
    result["distance_ratio"] = result["actual_km"] / result["planned_km"]
    result["geofence_distance_km"] = result.apply(
        lambda x: haversine_km(x["latitude"], x["longitude"], *ZONES[x["zone"]]), axis=1)
    result["inside_geofence"] = result["geofence_distance_km"].le(radius_km)
    return result


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """Zone-level metrics; late+failed deliveries count as SLA misses.

    On-time rate = on-time delivered / all attempted deliveries.
    Delivery success = delivered / all attempts.
    Km ratio = sum(actual km) / sum(planned km), not average of ratios.
    """
    if df.empty:
        raise ValueError("No deliveries")
    required = {"zone", "is_delivered", "is_on_time", "inside_geofence", "actual_km", "planned_km"}
    if not required.issubset(df.columns):
        raise ValueError("Call enrich() before summarize()")
    g = df.groupby("zone", sort=True).agg(
        attempts=("is_delivered", "size"), delivered=("is_delivered", "sum"),
        on_time=("is_on_time", "sum"), inside_geofence=("inside_geofence", "sum"),
        actual_km=("actual_km", "sum"), planned_km=("planned_km", "sum")
    ).reset_index()
    g["delivery_success_pct"] = (100*g["delivered"]/g["attempts"]).round(2)
    g["sla_on_time_pct"] = (100*g["on_time"]/g["attempts"]).round(2)
    g["geofence_coverage_pct"] = (100*g["inside_geofence"]/g["attempts"]).round(2)
    g["distance_vs_plan_ratio"] = (g["actual_km"]/g["planned_km"]).round(3)
    return g
