import math

from asset_investment_simulator.demo import demo_assets, demo_systems
from asset_investment_simulator.engine import build_renewal_schedule, simulate
from asset_investment_simulator.scenarios import baseline, maintain_condition, target_condition


def test_simulation_covers_full_horizon_and_rollups():
    result = simulate(demo_assets(), baseline(), demo_systems())
    assert result["site_year"]["year"].min() == 2027
    assert result["site_year"]["year"].max() == 2040
    assert len(result["portfolio_year"]) == 14
    assert result["summary"]["sites"] == 3
    assert result["summary"]["caisses"] == 2


def test_maintain_condition_holds_opening_backlogs_in_real_terms():
    assets = demo_assets()
    result = simulate(assets, maintain_condition(), systems=None)
    first_site = result["site_year"][result["site_year"]["site_id"] == "C001-S01"]
    assert all(math.isclose(v, 615000.0, rel_tol=1e-9) for v in first_site["technical_backlog"])
    assert all(math.isclose(v, 300000.0, rel_tol=1e-9) for v in first_site["functional_backlog"])
    assert all(math.isclose(v, 120000.0, rel_tol=1e-9) for v in first_site["capacity_backlog"])


def test_target_condition_reaches_configured_2040_targets():
    config = target_condition(technical_ci=0.10, functional_ci=0.08, capacity_ci=0.05)
    result = simulate(demo_assets(), config, systems=None)
    end = result["site_year"][result["site_year"]["year"] == 2040]
    assert (end["technical_ci"] <= 0.100000001).all()
    assert (end["functional_ci"] <= 0.080000001).all()
    assert (end["capacity_ci"] <= 0.050000001).all()


def test_renewal_schedule_uses_wooldridge_cycle_logic():
    schedule = build_renewal_schedule(demo_assets(), demo_systems(), baseline())
    assert ("C001-S01", 2028) in schedule
    assert schedule[("C001-S01", 2028)] == 4100000 * 0.12


def test_rollup_ci_is_backlog_over_rollup_crv_not_average_site_ci():
    result = simulate(demo_assets(), baseline(), systems=None)
    row = result["portfolio_year"].iloc[0]
    expected = (row["technical_backlog"] + row["functional_backlog"] + row["capacity_backlog"]) / row["crv"]
    assert math.isclose(row["comprehensive_ci"], expected, rel_tol=1e-12)
