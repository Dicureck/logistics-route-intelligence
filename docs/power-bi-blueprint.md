# Power BI implementation blueprint

This repo **does not contain a PBIX**. A reproducible CSV export and modeling instructions are supplied so a Power BI model can be built and audited without a proprietary template.

## Import model

Load `build/demo/synthetic_deliveries.csv`; name the table `Deliveries`. Use correct date and numeric types. Use a Date dimension with a one-to-many relationship `Calendar[Date]` → `Deliveries[service_date]`. Mark it as a Date table. Add a Zones dimension keyed by `zone`.

## DAX measures

```DAX
Delivery Attempts = COUNTROWS(Deliveries)
Delivered = CALCULATE([Delivery Attempts], Deliveries[status] = "delivered")
Delivery Success % = DIVIDE([Delivered], [Delivery Attempts])
On-Time Deliveries = CALCULATE([Delivery Attempts], Deliveries[status] = "delivered", Deliveries[actual_minutes] <= Deliveries[promised_minutes])
On-Time SLA % = DIVIDE([On-Time Deliveries], [Delivery Attempts])
Distance Ratio = DIVIDE(SUM(Deliveries[actual_km]), SUM(Deliveries[planned_km]))
```

If the Power BI engine rejects a column-to-column filter expression in `CALCULATE`, implement the on-time count with `COUNTROWS(FILTER(Deliveries, Deliveries[status] = "delivered" && Deliveries[actual_minutes] <= Deliveries[promised_minutes]))`.

## Recommended report pages

1. **Executive overview**: KPI cards, trends by service_date, failure breakdown by zone.
2. **Route performance**: distribution of actual/planned distance ratios, time performance, per-driver drilldown.
3. **Territory quality**: map of the fabricated delivery coordinates, radial geofences and coverage trends.
4. **Operational QA**: missing coordinates, unexpected statuses, duplicated delivery IDs, zero denominators.

Apply tooltips with numerator and denominator, label synthetic data prominently, and avoid presenting generated rates as customer performance.
