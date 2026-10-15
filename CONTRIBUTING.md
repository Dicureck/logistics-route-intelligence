# Contribution guide

1. Open an issue explaining the behavior, reproduction steps, and expected result.
2. Add deterministic tests for changes to metrics, data generation, or validation.
3. Keep example data fictional, small, and reproducible. No customer data or credentials.
4. Run `python -m pytest -q` locally. Document any integration tests requiring external tooling.
5. Avoid publishing benchmark claims unless the environment and protocol are disclosed.
