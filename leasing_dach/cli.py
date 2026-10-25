# -*- coding: utf-8 -*-
"""
CLI fuer den DACH B2B Leasing- vs. Kreditkauf- & Eigenkapital-Vergleichsrechner 2026
"""

import argparse
import json
from .calculator import LeasingComparisonInput, calculate_leasing_vs_loan


def main():
    parser = argparse.ArgumentParser(
        description="DACH B2B Leasing- vs. Kreditkauf- & Eigenkapital-Vergleichsrechner 2026 (DE, AT, CH)"
    )
    parser.add_argument("--country", default="DE", choices=["DE", "AT", "CH"], help="Land (DE, AT, CH)")
    parser.add_argument("--asset", type=float, default=120_000.0, help="Anschaffungswert Netto")
    parser.add_argument("--months", type=int, default=48, help="Laufzeit in Monaten")
    parser.add_argument("--afa-years", type=float, default=6.0, help="Betriebsgewoehnliche AfA-Nutzungsdauer in Jahren")
    parser.add_argument("--residual-pct", type=float, default=20.0, help="Kalkulierter Restwert in Prozent (%%)")
    parser.add_argument("--down-pct", type=float, default=10.0, help="Leasing-Sonderzahlung in Prozent (%%)")
    parser.add_argument("--lease-factor", type=float, default=1.85, help="Monatlicher Leasingfaktor in Prozent (%%)")
    parser.add_argument("--loan-interest", type=float, default=5.40, help="Bankkredit-Zinssatz p.a. in Prozent (%%)")
    parser.add_argument("--tax-rate", type=float, default=30.0, help="Unternehmens-Steuersatz in Prozent (%%)")
    parser.add_argument("--wacc", type=float, default=6.50, help="Kalkulationszins / WACC p.a. in Prozent (%%)")
    parser.add_argument("--gewst-above", action="store_true", help="DE: Ueber 200.000 EUR Freibetrag gem. Paragraph 8 Nr. 1d GewStG")
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON")

    args = parser.parse_args()

    inp = LeasingComparisonInput(
        country=args.country,
        asset_value=args.asset,
        duration_months=args.months,
        afa_years=args.afa_years,
        residual_value_pct=args.residual_pct,
        leasing_down_payment_pct=args.down_pct,
        leasing_monthly_factor_pct=args.lease_factor,
        loan_interest_pct_pa=args.loan_interest,
        tax_rate_pct=args.tax_rate,
        discount_rate_wacc_pct_pa=args.wacc,
        gewst_above_threshold=args.gewst_above,
    )
    res = calculate_leasing_vs_loan(inp)

    if args.json:
        print(json.dumps(res.__dict__, indent=2, ensure_ascii=False))
    else:
        print("=" * 74)
        print(f"DACH B2B LEASING- VS. KREDITKAUF-ANALYSE 2026 ({res.country} / {res.currency})")
        print("=" * 74)
        print(f"BMF 40-90%% Regel          : {res.bmf_40_90_ratio_pct:.1f} % ({'KONFORM' if res.bmf_40_90_compliant else 'ACHTUNG'})")
        print(f"1. Gewerbeleasing (NPV)    : {res.npv_cost_lease:,.2f} {res.currency} (Netto n. St.: {res.net_cost_lease:,.2f})")
        print(f"2. Bankkreditkauf (NPV)    : {res.npv_cost_loan:,.2f} {res.currency} (Netto n. St.: {res.net_cost_loan:,.2f})")
        print(f"3. Eigenkapital-Kauf (NPV) : {res.npv_cost_cash:,.2f} {res.currency} (Netto n. St.: {res.net_cost_cash:,.2f})")
        print(f"Empfehlung (Barwert-Sieger): {res.best_option} (+{res.npv_advantage_over_second:,.2f} {res.currency} Vorteil)")
        print("=" * 74)


if __name__ == "__main__":
    main()
