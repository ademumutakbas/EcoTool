import streamlit as st
import itertools
from PIL import Image

st.set_page_config(page_title="Eco Skill Optimizer")

# ---------------- Dil seçimi ----------------
lang = st.radio("Language / Dil", ["TR", "EN"])

texts = {
    "input_labels": {
        "price_pp": {
            "TR": "Ürün piyasa fiyatı (PP başına)",
            "EN": "Product market price per PP"
        },
        "company_bonus": {
            "TR": "Şirket bonusu (%)",
            "EN": "Company bonus (%)"
        },
        "z": {
            "TR": "Enerji maaşı (PP başına)",
            "EN": "Salary per PP (Energy)"
        },
        "tax_rate": {
            "TR": "Maaş vergisi (%)",
            "EN": "Salary tax (%)"
        },
        "engine_level": {
            "TR": "Automated Engine Seviyesi (1-7)",
            "EN": "Automated Engine Level (1-7)"
        },
        "S": {
            "TR": "Toplam Skill Puanı (Güncel Seviye × 4)",
            "EN": "Total Skill Points (Current Level × 4)"
        },
        "current_companies": {
            "TR": "Mevcut şirket sayısı (0 = sınırsız)",
            "EN": "Current companies (0 = no limit)"
        }
    },
    "results": {
        "title": {"TR": "En iyi kombinasyon:", "EN": "Best combination:"},
        "Lg": {"TR": "Entrepreneurship Level", "EN": "Entrepreneurship Level"},
        "Lw": {"TR": "Energy Level", "EN": "Energy Level"},
        "Lp": {"TR": "Production Level", "EN": "Production Level"},
        "Lc": {"TR": "Company Limit Level", "EN": "Company Limit Level"},
        "total_companies": {"TR": "Toplam şirket", "EN": "Total companies"},
        "max_z": {"TR": "Günlük Max BTC Kazancı", "EN": "Max Daily BTC Profit"}
    }
}

# ---------------- Fotoğraflar ----------------
images = {
    "market": Image.open(".devcontainer/market.png"),
    "comp_bonus": Image.open(".devcontainer/comp_bonus.png"),
    "PP_maas": Image.open(".devcontainer/PP_maas.png"),
    "tax": Image.open(".devcontainer/tax.png"),
    "automated_engine": Image.open(".devcontainer/automated_engine.png"),
    "skill_point": Image.open(".devcontainer/skill_point.png"),
    "companies": Image.open(".devcontainer/companies.png"),
    "entrepreneurship": Image.open(".devcontainer/entrepreneurship.png"),
    "energy": Image.open(".devcontainer/energy.png"),
    "production": Image.open(".devcontainer/production.png"),
    "company_limit": Image.open(".devcontainer/company_limit.png")
}

INPUT_ICON_WIDTH = 100
RESULT_ICON_WIDTH = 50

# ---------------- Fonksiyonlar ----------------
def get_float_input_with_icon(label_key, img, default):
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(img, width=INPUT_ICON_WIDTH)
    with col2:
        val_str = st.text_input(
            texts["input_labels"][label_key][lang],
            value=default,
            key=f"{label_key}_{lang}"
        )
        try:
            return float(val_str)
        except ValueError:
            st.warning("Geçerli bir sayı giriniz / Enter a valid number")
            st.stop()

def get_int_input_with_icon(label_key, img, default):
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(img, width=INPUT_ICON_WIDTH)
    with col2:
        val_str = st.text_input(
            texts["input_labels"][label_key][lang],
            value=default,
            key=f"{label_key}_{lang}"
        )
        try:
            return int(val_str)
        except ValueError:
            st.warning("Geçerli bir tam sayı giriniz / Enter a valid integer")
            st.stop()

# ---------------- Kullanıcı girdileri ----------------
price_pp = get_float_input_with_icon("price_pp", images["market"], "0.05")
company_bonus = get_float_input_with_icon("company_bonus", images["comp_bonus"], "31")

z = get_float_input_with_icon("z", images["PP_maas"], "0.07")
tax_rate = get_float_input_with_icon("tax_rate", images["tax"], "8")

engine_level = get_int_input_with_icon("engine_level", images["automated_engine"], "3")
S = get_int_input_with_icon("S", images["skill_point"], "56")
current_companies = get_int_input_with_icon("current_companies", images["companies"], "6")

# ---------------- Hesaplama ----------------
if st.button("Hesapla"):

    Q = price_pp * (1 + company_bonus / 100)

    engine_values = {1: 24, 2: 48, 3: 72, 4: 96, 5: 120, 6: 144, 7: 168}
    K = price_pp * (1 + company_bonus / 100) * engine_values[engine_level]

    levels = range(0, 11)

    def skill_cost(level):
        return level * (level + 1) // 2

    base_companies = 2
    opened_companies = max(current_companies - base_companies, 0)

    if current_companies == 0:
        lc_levels = range(0, 11)
    else:
        lc_levels = range(0, opened_companies + 1)

    best_Z = -1
    best_combination = None
    best_total_companies = None

    for Lg, Lw, Lp, Lc in itertools.product(levels, levels, levels, lc_levels):
        cost = (
            skill_cost(Lg) +
            skill_cost(Lw) +
            skill_cost(Lp) +
            skill_cost(Lc)
        )

        if cost > S:
            continue

        Xp = 10 + 3 * Lp
        Xg = (30 + 5 * Lg) * Xp / 10
        Xw = (30 + 10 * Lw) * Xp / 10
        Xc = base_companies + Lc

        Z_net = z * (1 - tax_rate / 100)
        Z_total = 2.4 * Q * Xg + 2.4 * Z_net * Xw + K * Xc

        if Z_total > best_Z:
            best_Z = Z_total
            best_combination = (Lg, Lw, Lp, Lc)
            best_total_companies = Xc

    # ---------------- Sonuç ----------------
    if best_combination:
        st.markdown(f"### {texts['results']['title'][lang]}")

        def show_result(label_key, img, value):
            col1, col2 = st.columns([1, 5])
            with col1:
                st.image(img, width=RESULT_ICON_WIDTH)
            with col2:
                st.write(f"{texts['results'][label_key][lang]}: {value}")

        show_result("Lg", images["entrepreneurship"], best_combination[0])
        show_result("Lw", images["energy"], best_combination[1])
        show_result("Lp", images["production"], best_combination[2])
        show_result("Lc", images["company_limit"], best_combination[3])

        st.write(f"{texts['results']['total_companies'][lang]}: {best_total_companies}")
        st.write(f"{texts['results']['max_z'][lang]}: {round(best_Z, 2)}")
    else:
        st.warning("Geçerli kombinasyon bulunamadı / No valid combination found")

# ---------------- Alt bilgi ----------------
st.markdown(
    "Made by [Monarch](https://app.warera.io/user/681f630b1353a30ceefec393)"
)
