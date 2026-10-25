# -*- coding: utf-8 -*-
"""
Finanzmathematisches Kernmodul für den 3-Wege-Investitionsvergleich:
Gewerbeleasing (Voll-/Teilamortisation) vs. Bankkreditkauf (Annuitätendarlehen + AfA) vs. Eigenkapital-Barkauf
inkl. BMF-Leasingerlass-Prüfung (40-90%-Regel), § 8 Nr. 1d GewStG Hinzurechnung und Barwert/Kapitalwert (NPV).

Rechtlicher Hinweis (§ 2 RDG / § 5 StBerG):
Rein mathematisch-betriebswirtschaftliches Modell ohne Rechts-, Steuer- oder Finanzierungsberatung.
"""

from dataclasses import dataclass
from typing import Dict, Any


COUNTRY_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "DE": {
        "currency": "EUR",
        "legal_norm": "BMF-Leasingerlasse (40-90%-Regel) & § 8 Nr. 1d GewStG (20% Miet-/Leasing-Hinzurechnung ab 200k € Freibetrag)",
        "default_tax_rate_pct": 30.0,
    },
    "AT": {
        "currency": "EUR",
        "legal_norm": "EStR 2000 Rz 135 ff. (Leasing-Zurechnungskriterien) & § 22 KStG (23 % KÖSt)",
        "default_tax_rate_pct": 23.0,
    },
    "CH": {
        "currency": "CHF",
        "legal_norm": "OR / Schweizer Handbuch der Wirtschaftsprüfung (HWP) & kantonale Gewinnsteuer",
        "default_tax_rate_pct": 15.0,
    },
}


@dataclass
class LeasingComparisonInput:
    country: str = "DE"
    asset_value: float = 120_000.0
    duration_months: int = 48
    afa_years: float = 6.0
    residual_value_pct: float = 20.0
    leasing_down_payment_pct: float = 10.0
    leasing_monthly_factor_pct: float = 1.85
    loan_interest_pct_pa: float = 5.40
    tax_rate_pct: float = 30.0
    discount_rate_wacc_pct_pa: float = 6.50
    gewst_above_threshold: bool = False


@dataclass
class LeasingComparisonResult:
    country: str
    currency: str
    legal_norm: str
    bmf_40_90_ratio_pct: float
    bmf_40_90_compliant: bool
    monthly_lease_rate: float
    monthly_loan_rate: float
    gross_cost_lease: float
    gross_cost_loan: float
    gross_cost_cash: float
    tax_shield_lease: float
    tax_shield_loan: float
    tax_shield_cash: float
    net_cost_lease: float
    net_cost_loan: float
    net_cost_cash: float
    npv_cost_lease: float
    npv_cost_loan: float
    npv_cost_cash: float
    best_option: str
    npv_advantage_over_second: float


def check_bmf_40_90_rule(duration_months: int, afa_years: float) -> Dict[str, Any]:
    if duration_months <= 0 or afa_years <= 0:
        raise ValueError("duration_months and afa_years must be positive")
    afa_months = float(afa_years) * 12.0
    ratio_pct = (float(duration_months) / afa_months) * 100.0
    compliant = 40.0 <= ratio_pct <= 90.0
    return {
        "ratio_pct": round(ratio_pct, 2),
        "compliant": compliant,
    }


def calculate_leasing_vs_loan(inp: LeasingComparisonInput) -> LeasingComparisonResult:
    c = inp.country.upper().strip()
    if c not in COUNTRY_DEFAULTS:
        raise ValueError(f"Unsupported country '{inp.country}'. Choose from DE, AT, CH.")
    if inp.asset_value <= 0:
        raise ValueError("asset_value must be positive")
    if inp.duration_months < 6:
        raise ValueError("duration_months must be at least 6")
    if inp.afa_years <= 0:
        raise ValueError("afa_years must be positive")

    std = COUNTRY_DEFAULTS[c]
    bmf = check_bmf_40_90_rule(inp.duration_months, inp.afa_years)

    asset = float(inp.asset_value)
    months = int(inp.duration_months)
    afa_months = float(inp.afa_years) * 12.0
    tax_rate = float(inp.tax_rate_pct) / 100.0
    wacc_month = (float(inp.discount_rate_wacc_pct_pa) / 100.0) / 12.0

    # 1. Gewerbeleasing
    down_payment = asset * (float(inp.leasing_down_payment_pct) / 100.0)
    monthly_lease = asset * (float(inp.leasing_monthly_factor_pct) / 100.0)
    residual_buyout = asset * (float(inp.residual_value_pct) / 100.0)

    # Falls DE und über 200.000 € Freibetrag nach § 8 Nr. 1d GewStG:
    # 20% Finanzierungsanteil * 25% Hinzurechnung = 5% nicht abzugsfähig bei ~15% GewSt => ~0.75%-Punkte geringerer Steuervorteil
    lease_tax_rate = max(0.0, tax_rate - 0.0075) if (c == "DE" and inp.gewst_above_threshold) else tax_rate

    total_lease_payments = down_payment + (monthly_lease * months)
    gross_cost_lease = total_lease_payments + residual_buyout
    tax_shield_lease = total_lease_payments * lease_tax_rate + (residual_buyout * tax_rate * 0.5)
    net_cost_lease = gross_cost_lease - tax_shield_lease

    npv_lease = down_payment * (1.0 - lease_tax_rate)
    for m in range(1, months + 1):
        npv_lease += (monthly_lease * (1.0 - lease_tax_rate)) / ((1.0 + wacc_month) ** m)
    npv_lease += (residual_buyout * (1.0 - tax_rate * 0.5)) / ((1.0 + wacc_month) ** months)

    # 2. Bankkreditkauf (Annuitätendarlehen + AfA)
    r_loan_m = (float(inp.loan_interest_pct_pa) / 100.0) / 12.0
    if r_loan_m > 0:
        monthly_loan = asset * (r_loan_m * ((1.0 + r_loan_m) ** months)) / (((1.0 + r_loan_m) ** months) - 1.0)
    else:
        monthly_loan = asset / months

    gross_cost_loan = monthly_loan * months
    total_loan_interest = gross_cost_loan - asset

    afa_per_month = asset / afa_months
    total_afa_in_period = min(asset, afa_per_month * months)
    remaining_book_val = max(0.0, asset - total_afa_in_period)

    tax_shield_loan = (total_afa_in_period + total_loan_interest) * tax_rate + (remaining_book_val * tax_rate * 0.7)
    net_cost_loan = gross_cost_loan - tax_shield_loan

    npv_loan = 0.0
    balance = asset
    for m in range(1, months + 1):
        interest_m = balance * r_loan_m
        principal_m = monthly_loan - interest_m
        balance = max(0.0, balance - principal_m)
        afa_m = afa_per_month if m <= afa_months else 0.0
        tax_save_m = (interest_m + afa_m) * tax_rate
        npv_loan += (monthly_loan - tax_save_m) / ((1.0 + wacc_month) ** m)
    npv_loan -= (remaining_book_val * tax_rate * 0.7) / ((1.0 + wacc_month) ** months)

    # 3. Barkauf (Eigenkapital in t=0)
    gross_cost_cash = asset
    tax_shield_cash = total_afa_in_period * tax_rate + (remaining_book_val * tax_rate * 0.7)
    net_cost_cash = gross_cost_cash - tax_shield_cash

    npv_cash = asset
    for m in range(1, months + 1):
        afa_m = afa_per_month if m <= afa_months else 0.0
        tax_save_m = afa_m * tax_rate
        npv_cash -= tax_save_m / ((1.0 + wacc_month) ** m)
    npv_cash -= (remaining_book_val * tax_rate * 0.7) / ((1.0 + wacc_month) ** months)

    options = sorted(
        [
            ("Gewerbeleasing", npv_lease),
            ("Bankkreditkauf", npv_loan),
            ("Barkauf", npv_cash),
        ],
        key=lambda x: x[1],
    )
    best_option = options[0][0]
    npv_advantage = options[1][1] - options[0][1]

    return LeasingComparisonResult(
        country=c,
        currency=std["currency"],
        legal_norm=std["legal_norm"],
        bmf_40_90_ratio_pct=bmf["ratio_pct"],
        bmf_40_90_compliant=bmf["compliant"],
        monthly_lease_rate=round(monthly_lease, 2),
        monthly_loan_rate=round(monthly_loan, 2),
        gross_cost_lease=round(gross_cost_lease, 2),
        gross_cost_loan=round(gross_cost_loan, 2),
        gross_cost_cash=round(gross_cost_cash, 2),
        tax_shield_lease=round(tax_shield_lease, 2),
        tax_shield_loan=round(tax_shield_loan, 2),
        tax_shield_cash=round(tax_shield_cash, 2),
        net_cost_lease=round(net_cost_lease, 2),
        net_cost_loan=round(net_cost_loan, 2),
        net_cost_cash=round(net_cost_cash, 2),
        npv_cost_lease=round(npv_lease, 2),
        npv_cost_loan=round(npv_loan, 2),
        npv_cost_cash=round(npv_cash, 2),
        best_option=best_option,
        npv_advantage_over_second=round(npv_advantage, 2),
    )
