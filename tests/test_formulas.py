import pytest
from asset_investment_simulator.formulas import (
    technical_backlog, functional_backlog, capacity_backlog,
    condition_indices, current_replacement_value, present_value, annual_equivalent,
)


def test_technical_backlog_uses_additive_rates():
    assert technical_backlog(100, 0.02, 0.03, 10, 8) == pytest.approx(107)


def test_functional_and_capacity_have_no_physical_deterioration():
    assert functional_backlog(100, 0.03, 10, 8) == pytest.approx(105)
    assert capacity_backlog(100, 0.03, 10, 8) == pytest.approx(105)


def test_condition_indices():
    result = condition_indices(10, 20, 30, 100)
    assert result == pytest.approx({"technical_ci": .1, "functional_ci": .2, "capacity_ci": .3, "comprehensive_ci": .6})


def test_crv():
    assert current_replacement_value(7000, 500, 1.1, 1.05) == pytest.approx(4_042_500)


def test_pv_and_ae():
    pv = present_value([100, 100], .05)
    assert pv == pytest.approx(185.941043, rel=1e-6)
    assert annual_equivalent(pv, .05, 2) == pytest.approx(100)
