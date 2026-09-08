from pathlib import Path
import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Asset Investment Simulator", layout="wide")
st.title("Asset Investment Simulator")
st.caption("Caisse network portfolio decision support | 2027–2040")

HOW_TO = Path("docs/HOW_TO_USE.md").read_text(encoding="utf-8")
MODEL_GUIDE = Path("docs/MODEL_GUIDE.md").read_text(encoding="utf-8")
ARCH = Path("docs/ARCHITECTURE.md").read_text(encoding="utf-8")

tabs = st.tabs(["Portfolio", "Asset Register", "Scenario", "Review notes", "How to use", "Model guide", "Architecture"])

with tabs[0]:
    st.subheader("Portfolio hierarchy")
    st.write("Caisse Network Portfolio → 189 Caisse subportfolios → Site(s)")
    st.info("This version establishes the governed architecture and formula core. Scenario optimization and Monte Carlo are staged extensions, not yet production-calibrated forecasts.")

with tabs[1]:
    st.subheader("Import canonical Asset Register")
    uploaded = st.file_uploader("CSV or XLSX mapped to the canonical template", type=["csv", "xlsx"])
    if uploaded:
        df = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
        st.dataframe(df, use_container_width=True)
        required = {"caisse_id", "site_id", "site_name", "asset_type", "asset_status", "city", "province_code", "country_code", "gross_floor_area", "area_unit", "tenure_type", "source_system", "source_record_id"}
        missing = sorted(required - set(df.columns))
        if missing:
            st.error("Missing required fields: " + ", ".join(missing))
        else:
            st.success(f"Canonical structure validated: {len(df):,} sites across {df['caisse_id'].nunique():,} Caisses.")
    st.download_button("Download canonical Asset Register template", Path("data/templates/asset_register_template.csv").read_bytes(), "asset_register_template.csv")

with tabs[2]:
    st.subheader("Scenario framework")
    st.write("Strategy families: Baseline, Condition First, Network Optimization, Carbon First, Integrated 2040.")
    st.warning("A scenario is not a forecast. Results depend on supplied state, assumptions, actions, funding and uncertainty.")

with tabs[3]:
    st.subheader("Human review / AI feedback")
    scope = st.selectbox("Scope", ["Portfolio", "Caisse", "Site", "Scenario", "Model rule"])
    observation = st.text_area("Observation")
    proposed = st.text_area("Suggested change or question")
    payload = {"schema":"caisse.asset-investment-simulator.feedback.v1","scope":scope,"observation":observation,"suggested_change_or_question":proposed,
               "ai_instructions":["Treat observations as human review input, not approved rules.","Trace proposed changes to equations, assumptions, mappings or business rules.","Keep Wooldridge formulas separate from Caisse extensions.","Add regression tests for changes that alter scenario results."]}
    st.download_button("Export feedback JSON", json.dumps(payload, indent=2), "model_feedback.json", "application/json")

with tabs[4]: st.markdown(HOW_TO)
with tabs[5]: st.markdown(MODEL_GUIDE)
with tabs[6]: st.markdown(ARCH)
