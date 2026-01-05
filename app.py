import streamlit as st
import itertools
from PIL import Image

st.set_page_config(page_title="Eco Skill Optimizer", layout="centered")

# ---------------- Language ----------------
lang = st.radio("Language / Dil", ["TR", "EN"], horizontal=True)

TEXT = {
    "TR": {
        "companies": "Toplam şirket sayısı (1–12, 0 = sınırsız)",
        "engine": "Automated Engine Seviyesi (1–7)",
        "bonus": "Sahip olduğunuz şirketlerin üretim bonusu (%)",
        "price": "Üretilen ürünün market satış fiyatı (PP başına)",
        "salary": "Çalıştığınız yerde aldığınız maaş (PP başına)",
        "tax": "Aldığınız maaşın vergisi (%)",
        "skill": "Toplam Skill Puanı (Güncel Seviye × 4)",
        "calc": "Hesapla"
    },
    "EN": {
        "companies": "Total number of companies (1–12, 0 = unlimited)",
        "engine": "Automated Engine Level (1–7)",
        "bonus": "Production bonus of owned companies (%)",
        "price": "Market selling price of produced product (per PP)",
        "salary": "Salary you earn (per PP)",
        "tax": "Salary tax (%)",
        "skill": "Total Skill Points (Current Level × 4)",
        "calc": "Calculate"
    }
}

T = TEXT[lang]

# ---------------- Images ----------------
images = {
    "companies": Image.open(".devcontainer/companies.png"),
    "engine": Image.open(".devcontainer/automated_engine.png"),
    "bonus": Image.open(".devcontainer/comp_bonus.png"),
    "market": Image.open(".devcontainer/market.png"),
    "salary": Image.open(".devcontainer/PP_maas.png"),
    "tax": Image.open(".devcontainer/tax.png"),
}

# ---------------- Input Helper ----------------
def input_with_image(img, label, default):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(img, use_container_width=True)
    with col2:
        return st.number_input(label, value=default)

# ---------------- Inputs ----------------
companies = input_with_image(images["companies"], T["companies"], 6)
engine_level = input_with_image(images["engine"], T["engine"], 3)
bonus = input_with_image(images["bonus"], T["bonus"], 31.0)
price = input_with_image(images["market"], T["price"], 0.05)
salary = input_with_image(images["salary"], T["salary"], 0.07)
tax = input_with_image(images["tax"], T["tax"], 8.0)
skill_points = st.number_input(T["skill"], value=56)

# ---------------- Calculation ----------------
if st.button(T["calc"]):
    engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
    K = price * (1 + bonus/100) * engine_values[int(engine_level)]

    levels = range(0, 11)

    def skill_cost(lvl):
        return lvl * (lvl + 1) // 2

    base_companies = 2
    lc_levels = range(0, 11) if companies == 0 else range(0, max(int(companies) - base_companies, 0) + 1)

    best_profit = -1
    best_combo = None

    for Lg, Lw, Lp, Lc in itertools.product(levels, levels, levels, lc_levels):
        cost = skill_cost(Lg) + skill_cost(Lw) + skill_cost(Lp) + skill_cost(Lc)
        if cost > skill_points:
            continue

        Xp = 10 + 3 * Lp
        Xg = (30 + 5 * Lg) * Xp / 10
        Xw = (30 + 10 * Lw) * Xp / 10
        Xc = base_companies + Lc

        net_salary = salary * (1 - tax / 100)
        profit = 2.4 * price * (1 + bonus/100) * Xg + 2.4 * net_salary * Xw + K * Xc

        if profit > best_profit:
            best_profit = profit
            best_combo = (Lg, Lw, Lp, Lc)

    st.subheader("Best Combination / En İyi Kombinasyon")
    st.write("Entrepreneurship:", best_combo[0])
    st.write("Energy:", best_combo[1])
    st.write("Production:", best_combo[2])
    st.write("Company Limit:", best_combo[3])
    st.write("Max Profit:", round(best_profit, 2))
