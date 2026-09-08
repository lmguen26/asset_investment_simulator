"""Graph-compatible Caisse network representation.

The graph describes relationships; it is not the calculation engine.
"""
from __future__ import annotations
import networkx as nx
import pandas as pd


def build_portfolio_graph(assets: pd.DataFrame) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    graph.add_node("portfolio", kind="portfolio", label="Caisse Network Portfolio")
    for _, row in assets.iterrows():
        caisse_id = str(row["caisse_id"])
        site_id = str(row["site_id"])
        caisse_node = f"caisse:{caisse_id}"
        site_node = f"site:{site_id}"
        graph.add_node(caisse_node, kind="caisse", caisse_id=caisse_id,
                       label=row.get("caisse_name", caisse_id))
        graph.add_edge("portfolio", caisse_node, relation="HAS_CAISSE")
        graph.add_node(site_node, kind="site", site_id=site_id,
                       label=row.get("site_name", site_id))
        graph.add_edge(caisse_node, site_node, relation="HAS_SITE")
    return graph


def validate_caisse_hierarchy(assets: pd.DataFrame) -> list[str]:
    warnings: list[str] = []
    if assets["site_id"].duplicated().any():
        warnings.append("Duplicate site_id values detected.")
    missing = assets["caisse_id"].isna().sum()
    if missing:
        warnings.append(f"{missing} site(s) have no caisse_id.")
    return warnings
