# Metric contracts

| Measure | Numerator | Denominator | Interpretation |
|:--|:--|:--|:--|
| Delivery success (%) | Successful deliveries | All attempted deliveries | Completion rate |
| On-time SLA (%) | Successfully delivered within promised minutes | **All attempts** | Failed deliveries also miss SLA |
| Geofence coverage (%) | Delivery coordinates within 2.6 km of the fictional zone center | All attempts | Coordinate/radius coverage only; **not** address accuracy |
| Actual / planned km | Sum of actual route km | Sum of planned route km | Greater than 1 implies excess distance, not proven inefficiency |

The Haversine formula measures great-circle distance, **not drive time, network distance, route optimization, or legal service area**. Zone coordinates, stop points, drivers, dates, and durations are entirely fabricated. The generated dashboard does not establish a causal effect of changes.
