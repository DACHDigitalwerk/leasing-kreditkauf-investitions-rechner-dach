# -*- coding: utf-8 -*-
"""
Unit-Tests fuer leasing_dach (DACH B2B Leasing- vs. Kreditkauf- & Eigenkapital-Vergleichsrechner 2026)
"""

import pytest
from leasing_dach import (
    LeasingComparisonInput,
    calculate_leasing_vs_loan,
    check_bmf_40_90_rule,
)


def test_bmf_40_90_rule_compliant():
    """Prueft, dass 48 Monate bei 6 Jahren (72 Monate = 66,67 %) BMF-konform sind."""
    res = check_bmf_40_90_rule(48, 6.0)
    assert res["compliant"] is True
    assert res["ratio_pct"] == pytest.approx(66.67, rel=1e-2)


def test_bmf_40_90_rule_non_compliant_too_short():
    """Prueft, dass 20 Monate bei 6 Jahren (< 40 %) nicht konform sind."""
    res = check_bmf_40_90_rule(20, 6.0)
    assert res["compliant"] is False
    assert res["ratio_pct"] < 40.0


def test_bmf_40_90_rule_non_compliant_too_long():
    """Prueft, dass 68 Monate bei 6 Jahren (> 90 %) nicht konform sind."""
    res = check_bmf_40_90_rule(68, 6.0)
    assert res["compliant"] is False
    assert res["ratio_pct"] > 90.0


def test_default_de_comparison():
    """Prueft die Standardberechnung fuer eine CNC-Maschine (120.000 EUR, 48 Monate, DE)."""
    inp = LeasingComparisonInput()
    res = calculate_leasing_vs_loan(inp)
    assert res.country == "DE"
    assert res.currency == "EUR"
    assert res.bmf_40_90_compliant is True
    assert res.monthly_lease_rate == pytest.approx(2_220.0)
    assert res.monthly_loan_rate > 2_500.0
    assert res.best_option in ("Gewerbeleasing", "Bankkreditkauf", "Barkauf")


def test_gewst_addback_reduces_lease_tax_shield():
    """Prueft, dass die gewerbesteuerliche Hinzurechnung nach § 8 Nr. 1d GewStG den Steuervorteil beim Leasing mindert."""
    res_within = calculate_leasing_vs_loan(LeasingComparisonInput(gewst_above_threshold=False))
    res_above = calculate_leasing_vs_loan(LeasingComparisonInput(gewst_above_threshold=True))
    assert res_above.tax_shield_lease < res_within.tax_shield_lease
    assert res_above.npv_cost_lease > res_within.npv_cost_lease


def test_austria_koest_23_mode():
    """Prueft den oesterreichischen Modus (AT, EUR, EStR & 23 % KOeSt)."""
    inp = LeasingComparisonInput(country="AT", tax_rate_pct=23.0)
    res = calculate_leasing_vs_loan(inp)
    assert res.country == "AT"
    assert res.currency == "EUR"
    assert "EStR" in res.legal_norm


def test_switzerland_chf_mode():
    """Prueft den Schweizer Modus (CH, CHF, OR)."""
    inp = LeasingComparisonInput(country="CH", asset_value=100_000.0, tax_rate_pct=15.0)
    res = calculate_leasing_vs_loan(inp)
    assert res.country == "CH"
    assert res.currency == "CHF"
    assert res.gross_cost_cash == pytest.approx(100_000.0)


def test_higher_wacc_favors_financed_options_over_cash():
    """Prueft, dass ein hoher Opportunitaetszins (WACC) den Barwert-Vorteil von Leasing/Kredit gegenueber Barkauf erhoeht."""
    res_low_wacc = calculate_leasing_vs_loan(LeasingComparisonInput(discount_rate_wacc_pct_pa=2.0))
    res_high_wacc = calculate_leasing_vs_loan(LeasingComparisonInput(discount_rate_wacc_pct_pa=14.0))
    diff_low = res_low_wacc.npv_cost_cash - res_low_wacc.npv_cost_lease
    diff_high = res_high_wacc.npv_cost_cash - res_high_wacc.npv_cost_lease
    assert diff_high > diff_low


def test_full_amortization_zero_residual():
    """Prueft Vollamortisations-Leasing (Restwert = 0 %)."""
    inp = LeasingComparisonInput(residual_value_pct=0.0, leasing_down_payment_pct=0.0, leasing_monthly_factor_pct=2.25, duration_months=48)
    res = calculate_leasing_vs_loan(inp)
    assert res.gross_cost_lease == pytest.approx(120_000.0 * 0.0225 * 48)


def test_invalid_inputs_raise_value_error():
    """Prueft Fehlerbehandlung bei ungueltigem Land oder negativen Werten."""
    with pytest.raises(ValueError):
        calculate_leasing_vs_loan(LeasingComparisonInput(country="FR"))
    with pytest.raises(ValueError):
        calculate_leasing_vs_loan(LeasingComparisonInput(asset_value=-5000))
    with pytest.raises(ValueError):
        check_bmf_40_90_rule(0, 5.0)
