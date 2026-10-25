# 🚜 DACH B2B Leasing- vs. Kreditkauf- & Eigenkapital-Vergleichsrechner 2026 (`leasing_dach`)

[![CI & Pytest](https://github.com/DACHDigitalwerk/leasing-kreditkauf-investitions-rechner-dach/actions/workflows/ci.yml/badge.svg)](https://github.com/DACHDigitalwerk/leasing-kreditkauf-investitions-rechner-dach/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Live Web-App](https://img.shields.io/badge/Live_Web_App-100%25_Client_Side-10b981)](https://dachdigitalwerk.github.io/leasing-kreditkauf-rechner/)

Finanzmathematische Python-Bibliothek und CLI (`dach-leasing`) für den **3-Wege-Investitionsvergleich zwischen Gewerbeleasing (Voll-/Teilamortisation), Bankkreditkauf (Annuitätendarlehen + AfA) und Eigenkapital-Barkauf** für Maschinen, IT-Infrastruktur und Fuhrpark in **Deutschland (DE), Österreich (AT) und der Schweiz (CH)**.

---

## 🌐 Interaktive Web-Applikation & B2B-Fachratgeber (100 % Client-Side)

Nutzen Sie den kostenlosen Online-Rechner mit **druckfertigem DIN-A4 Investitions- & Leasing-Vergleichsblatt** direkt im Browser:

- 🚀 **[DACH B2B Leasing- vs. Kreditkauf- & Eigenkapital-Vergleichsrechner 2026](https://dachdigitalwerk.github.io/leasing-kreditkauf-rechner/)**
- 📘 **[Leasing oder Kreditkauf 2026? Der große Barwert-Vergleich für Maschinen & Fuhrpark](https://dachdigitalwerk.github.io/leasing-oder-kreditkauf-maschinen-fuhrpark-rechner-2026.html)**
- ⚖️ **[Gewerbeleasing Steuervorteil: Betriebsausgabenabzug, AfA & § 8 Nr. 1d GewStG](https://dachdigitalwerk.github.io/gewerbeleasing-steuervorteil-betriebsausgaben-afa-vergleich.html)**
- 📊 **[Vollamortisation vs. Teilamortisation (Restwertleasing): BMF 40–90 %-Regel](https://dachdigitalwerk.github.io/restwertleasing-vollamortisation-teilamortisation-berechnen.html)**
- 🏠 **[DACH Digitalwerk – Alle 32 Self-Serve Web-Tools im Überblick](https://dachdigitalwerk.github.io/)**

---

## ✨ Kernfunktionen

1. **BMF 40–90 %-Regel & Steuerliche Bilanzneutralität:**
   - Prüft automatisch, ob die Grundmietzeit zwischen 40 % und 90 % der betriebsgewöhnlichen Nutzungsdauer (AfA) liegt (Zurechnung beim Leasinggeber = 100 % sofortiger Betriebsausgabenabzug der Leasingraten).
2. **Vollständige Steuer- & § 8 Nr. 1d GewStG-Analyse:**
   - Berücksichtigt Ertragsteuersätze (DE KSt/GewSt ~30 %, AT KÖSt 23 %, CH Gewinnsteuer ~12–19 %) sowie optional die gewerbesteuerliche Hinzurechnung nach **§ 8 Nr. 1d GewStG** (20 % × 25 % oberhalb des 200.000-€-Freibetrags).
3. **Kapitalwert / Barwert (NPV) der Nachsteuer-Cashflows:**
   - Diskontiert sämtliche monatlichen Auszahlungen und Steuerersparnisse mit dem individuellen Kalkulationszinssatz (WACC / Opportunitätszins).

---

## 📦 Installation & CLI-Nutzung

```bash
pip install -e .
dach-leasing --country DE --asset 120000 --months 48 --afa-years 6 --lease-factor 1.85
```

---

## ⚠️ Rechtlicher Hinweis (§ 2 RDG / § 5 StBerG)

Dieses Paket dient ausschließlich der unverbindlichen finanzmathematischen und betriebswirtschaftlichen Modellberechnung. Es stellt keine Steuer-, Rechts-, Bilanzierungs- oder Finanzierungsberatung dar.
