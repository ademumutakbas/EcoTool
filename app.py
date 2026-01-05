import streamlit as st
import itertools

st.set_page_config(
    page_title="Eco Skill Optimizer",
    layout="centered"
)

# ===================== CSS =====================
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.block {
    background: rgba(255,255,255,0.04);
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 20px;
}

.title {
    font-size: 18px;
    font-weight: 600;
}

.note {
    font-size: 13px;
    color: #9aa0a6;
    margin-top: 4px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ===================== LANGUAGE =====================
lang = st.radio("Language / Dil", ["TR", "EN"], horizontal=True)

TEXT = {
    "TR": {
        "companies": "Toplam şirket sayısı (1–12, 0 = sınırsız)",
        "companies_note": "0 girildiğinde fabrika sayısındaki sınır kalkar.",

        "engine": "Automated Engine Seviyesi (1–7)",
        "engine_note": "Tüm fabrikaların eşit seviyede olduğu varsayılır.",

        "bonus": "Sahip olduğunuz şirketlerin üretim bonusu (%)",
        "bonus_note": "Tüm fabrikaların aynı ürünü ürettiği ve aynı bölgede çalıştığı varsayılır.",

        "price": "Üretilen ürünün market satış fiyatı (PP başına)",
        "price_note": "Tek çeşit ürün ürettiğiniz baz alınır. Maksimum kâr sağlayan ürünü siz belirlemelisiniz.",

        "salary": "Çalıştığınız yerde aldığınız maaş (PP başına)",
        "tax": "Aldığınız maaşın vergisi (%)",

        "skill": "Toplam Skill Puanı (Güncel Seviye × 4)",

        "calc": "Hesapla",
        "result": "En iyi kombinasyon",
        "profit": "Günlük Maksimum BTC Kazancı"
    },
    "EN": {
        "companies": "Total number of companies (1–12, 0 = unlimited)",
        "companies_note": "Entering 0 removes the factory limit.",

        "engine": "Automated Engine Level (1–7)",
        "engine_note": "All factories are assumed to be at the same level.",

        "bonus": "Production bonus of owned companies (%)",
        "bonus_note": "All factories are assumed to produce the same product and operate in the same region.",

        "price": "Market selling price of produced product (per PP)",
        "price_note": "Single product production is assumed. You must choose the most profitable product.",

        "salary": "Salary you earn (per PP)",
        "tax": "Salary tax (%)",

        "skill": "Total Skill Points (Current Level × 4)",

        "calc": "Calculate",
        "result": "Best combination",
        "profit": "Maximum Daily BTC Profit"
    }
}

T = TEXT[lang]

# ===================== INPUT BLOCK =====================
def image_input_block(image_path, title, note, input_func):
    st.markdown('<div class="block">', unsafe_allow_html=True)

    col_img, col_input = st.columns([1.4, 4])

    with col_img:
        st.image(image_path, use_container_width=True)

    with col_input:
        st.markdown(f'<div class="title">{title}</div>', unsafe_allow_html=True)
        if note:
            st.markdown(f'<div class="note">{note}</div>', unsafe_allow_html=True)
        value = input_func()

    st.markdown('</div>', unsafe_allow_html=True)
    return value

# ===================== INPUTS =====================
companies = image_input_block(
    "images/companies.png",
    T["companies"],
    T["companies_note"],
    lambda: st.number_input("", min_value=0, max_value=12, value=6, label_visibility="collapsed")
)

engine_level = image_input_block(
    "images/automated_engine.png",
    T["engine"],
    T["engine_note"],
    lambda: st.number_input("", min_value=1, max_value=7, value=3, label_visibility="collapsed")
)

bonus = image_input_block(
    "images/comp_bonus.png",
    T["bonus"],
    T["bonus_note"],
    lambda: st.number_input("", value=31.0, label_visibility="collapsed")
)

price = image_input_block(
    "images/market.png",
    T["price"],
    T["price_note"],
    lambda: st.number_input("", value=0.05, label_visibility="collapsed")
)

salary = image_input_block(
    "images/PP_maas.png",
    T["salary"],
    "",
    lambda: st.number_input("", value=0.07, label_visibility="collapsed")
)

tax = image_input_block(
    "images/tax.png",
    T["tax"],
    "",
    lambda: st.number_input("", value=8.0, label_visibility="collapsed")
)

skill_points = image_input_block(
    "images/skill_point.png",
    T["skill"],
    "",
    lambda: st.number_input("", min_value=0, value=56, label_visibility="collapsed")
)

# ===================== CALCULATION =====================
if st.button(T["calc"]):
    engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
    K = price * (1 + bonus/100) * engine_values[int(engine_level)]

    levels = range(0, 11)

    def skill_cost(lvl):
        return lvl * (lvl + 1) // 2

    base_companies = 2
    lc_levels = range(0, 11) if companies == 0 else range(0, max(companies - base_companies, 0) + 1)

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

    st.markdown(f"## {T['result']}")
    st.write("Entrepreneurship:", best_combo[0])
    st.write("Energy:", best_combo[1])
    st.write("Production:", best_combo[2])
    st.write("Company Limit:", best_combo[3])
    st.write(f"**{T['profit']}: {round(best_profit, 2)} BTC**")
