# Engineering decisions

- **Determinism:** random seed and per-row ID allow reproducible regression tests.
- **No identifiable locations:** invented coordinates around a fictional center; not a reconstruction of commercial territories.
- **SLA policy:** incomplete deliveries count as misses, so rates cannot improve merely by dropping failures.
- **Geography:** Haversine is a basic diagnostic metric; production routing requires road networks and traffic conditions.
- **Publication boundary:** no employer schemas, customer identifiers, pricing, or operational records.
- **Preview:** a self-contained HTML document uses no web fonts, external libraries, or tracking URLs.
- **Limitations:** no vehicle routing optimization, no real dispatch capacity model, no proof of operational improvement.
