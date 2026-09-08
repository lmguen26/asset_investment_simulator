# Asset Investment Simulator

Python/Streamlit decision-support application for long-range Caisse network portfolio investment planning.

## Purpose

The simulator evaluates 2027–2040 portfolio strategies across three complementary modelling paradigms:

1. **Wooldridge deterministic core** — condition, backlog, sustainment, improvement, development, CRV and economic formulas.
2. **Caisse portfolio/network model** — 189 Caisse subportfolios containing sites, service relationships, energy/carbon, leases and portfolio actions.
3. **Uncertainty and decision support** — proxy models, Monte Carlo and later constrained network optimization.

The graph/network model does **not** replace the equations. It describes relationships and constraints in which the quantitative models operate.

## Canonical Wooldridge terminology

| Driver | Condition dimension | Investment class |
|---|---|---|
| Deterioration | Technical Backlog / Technical Condition Index | Sustainment |
| Obsolescence | Functional Backlog / Functional Condition Index | Improvement |
| Capacity | Capacity Backlog / Capacity Condition Index | Development |

Operations is the fourth investment cash-flow class. Comprehensive Condition combines Technical, Functional and Capacity backlog relative to CRV.

## Portfolio hierarchy

`Caisse Network Portfolio -> Caisse (189 subportfolios) -> Site(s)`

A Caisse is an organizational/subportfolio entity. A site is a physical/service location. Closing a site does not necessarily remove a service: services may be redistributed, consolidated or replaced by another service point such as an ATM.

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```bash
pytest -q
```

## Asset Register workflow

The supported ingestion pattern is:

`Raw Asset Register -> external field mapping -> canonical OSCRE-aligned import template -> validation -> simulator`

Use `data/templates/asset_register_template.csv` as the target export format. Exact OSCRE IDM entity/attribute identifiers must be validated against the selected licensed OSCRE use-case schema; this repository therefore says **OSCRE-aligned**, not OSCRE-conformant.

Condition, energy, carbon and service data should remain linked data products rather than being fabricated as Asset Register identity attributes.

## Documentation

- `docs/HOW_TO_USE.md` — operating instructions
- `docs/MODEL_GUIDE.md` — principles, formulas, terminology and limitations
- `docs/ARCHITECTURE.md` — deterministic + graph/network + stochastic architecture
- `docs/ASSET_REGISTER_MAPPING.md` — canonical import profile and mapping workflow
- `docs/AI_FEEDBACK_LOOP.md` — human notes and JSON feedback contract

## Modelling rule

Any code change that alters a 2040 curve must identify the equation, assumption, data mapping or business rule responsible and add/update regression tests.

## Important interpretation

A scenario is not a forecast. A 2040 result is the consequence of initial conditions, assumptions, funding strategy, portfolio actions and uncertainty under the selected scenario.
