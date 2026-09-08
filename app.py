from pathlib import Path
import json
import pandas as pd
import streamlit as st

from asset_investment_simulator.demo import demo_assets, demo_systems
from asset_investment_simulator.engine import simulate, validate_assets
from asset_investment_simulator.scenarios import SCENARIOS

st.set_page_config(page_title="Asset Investment Simulator", layout="wide")
st.title("Asset Investment Simulator")
st.caption("Caisse network portfolio decision support | deterministic 2027–2040 engine")

HOW_TO = Path("docs/HOW_TO_USE.md").read_text(encoding="utf-8")
MODEL_GUIDE = Path("docs/MODEL_GUIDE.md").read_text(encoding="utf-8")
ARCH = Path("docs/ARCHITECTURE.md").read_text(encoding="utf-8")

def read_upload(uploaded):
    return pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)

if "assets" not in st.session_state:
    st.session_state.assets = demo_assets()
if "systems" not in st.session_state:
    st.session_state.systems = demo_systems()

tabs = st.tabs(["Portfolio", "Asset Register", "Scenario", "Calculation audit", "Review notes", "How to use", "Model guide", "Architecture"])

with tabs[0]:
    st.subheader("Portfolio hierarchy")
    st.write("Caisse Network Portfolio → 189 Caisse subportfolios → Site(s)")
    assets = st.session_state.assets
    c1, c2, c3 = st.columns(3)
    c1.metric("Loaded sites", f"{assets['site_id'].nunique():,}")
    c2.metric("Loaded Caisses", f"{assets['caisse_id'].nunique():,}")
    c3.metric("Gross area", f"{assets['gross_floor_area'].sum():,.0f}")
    st.info("Demo data are loaded initially. Import the canonical Asset Register to replace them. Stochastic simulation and optimization remain separate later layers.")

with tabs[1]:
    st.subheader("Import canonical Asset Register")
    uploaded = st.file_uploader("CSV or XLSX mapped to the canonical template", type=["csv", "xlsx"], key="asset_upload")
    if uploaded:
        df = read_upload(uploaded)
        errors = validate_assets(df)
        st.dataframe(df, use_container_width=True)
        if errors:
            for error in errors:
                st.error(error)
        else:
            st.session_state.assets = df
            st.success(f"Validated: {len(df):,} sites across {df['caisse_id'].nunique():,} Caisses.")
    systems_upload = st.file_uploader("Optional system-renewal table", type=["csv", "xlsx"], key="system_upload")
    if systems_upload:
        st.session_state.systems = read_upload(systems_upload)
        st.success(f"Loaded {len(st.session_state.systems):,} system records.")
    st.download_button("Download canonical Asset Register template", Path("data/templates/asset_register_template.csv").read_bytes(), "asset_register_template.csv")

with tabs[2]:
    st.subheader("Deterministic scenario")
    scenario_name = st.selectbox("Scenario", list(SCENARIOS))
    config = SCENARIOS[scenario_name]()
    st.caption("Scenario policy is separate from Wooldridge formulas. All default monetary calculations use real/constant currency.")
    result = simulate(st.session_state.assets, config, st.session_state.systems)
    summary = result["summary"]
    cols = st.columns(5)
    cols[0].metric("PV TOTEX", f"${summary['pv_totex']/1_000_000:,.1f}M")
    cols[1].metric("2040 comprehensive CI", f"{summary['ending_comprehensive_ci']:.3f}")
    cols[2].metric("2040 technical CI", f"{summary['ending_technical_ci']:.3f}")
    cols[3].metric("Cumulative CAPEX", f"${summary['cumulative_capex']/1_000_000:,.1f}M")
    cols[4].metric("Carbon change", f"{summary['carbon_reduction_fraction']:.1%}")
    portfolio = result["portfolio_year"].set_index("year")
    st.markdown("#### Condition trajectory")
    st.line_chart(portfolio[["technical_ci", "functional_ci", "capacity_ci", "comprehensive_ci"]])
    st.markdown("#### Annual investment and operations")
    st.bar_chart(portfolio[["sustainment_funding", "improvement_funding", "development_funding", "annual_opex"]])
    st.markdown("#### Energy and carbon")
    st.line_chart(portfolio[["carbon_kgco2e", "carbon_target_kgco2e"]])
    st.warning("A scenario is not a forecast. It is the deterministic consequence of the loaded state, assumptions and funding policy.")
    st.download_button("Download site-year results CSV", result["site_year"].to_csv(index=False), "site_year_results.csv", "text/csv")
    st.download_button("Download Caisse-year results CSV", result["caisse_year"].to_csv(index=False), "caisse_year_results.csv", "text/csv")

with tabs[3]:
    st.subheader("Calculation audit")
    scenario_name_audit = st.selectbox("Audit scenario", list(SCENARIOS), key="audit_scenario")
    audit = simulate(st.session_state.assets, SCENARIOS[scenario_name_audit](), st.session_state.systems)
    site_ids = audit["site_year"]["site_id"].drop_duplicates().tolist()
    chosen_site = st.selectbox("Site", site_ids)
    audit_rows = audit["site_year"][audit["site_year"]["site_id"] == chosen_site]
    st.dataframe(audit_rows, use_container_width=True)
    st.caption("Audit fields expose opening backlog, deterioration, requirements, funding and ending backlog for each year and investment class.")
    st.json(audit["provenance"])

with tabs[4]:
    st.subheader("Human review / AI feedback")
    scope = st.selectbox("Scope", ["Portfolio", "Caisse", "Site", "Scenario", "Model rule"])
    observation = st.text_area("Observation")
    proposed = st.text_area("Suggested change or question")
    payload = {
        "schema":"caisse.asset-investment-simulator.feedback.v1",
        "scope":scope,
        "observation":observation,
        "suggested_change_or_question":proposed,
        "ai_instructions":[
            "Treat observations as human review input, not approved rules.",
            "Trace proposed changes to equations, assumptions, mappings or business rules.",
            "Keep Wooldridge formulas separate from Caisse extensions.",
            "Add regression tests for changes that alter scenario results.",
        ],
    }
    st.download_button("Export feedback JSON", json.dumps(payload, indent=2), "model_feedback.json", "application/json")

with tabs[5]: st.markdown(HOW_TO)
with tabs[6]: st.markdown(MODEL_GUIDE)
with tabs[7]: st.markdown(ARCH)
