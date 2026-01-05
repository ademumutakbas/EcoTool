import streamlit as st
import itertools
from PIL import Image
import os

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Eco Skill Optimizer",
    layout="centered"
)

# -------------------------------------------------
# Custom CSS
# -------------------------------------------------
st.markdown("""
<style>
.small-note {
    font-size: 13px;
    color: #8a8a8a;
    margin-top: -6px;
    margin-bottom: 8px;
}

.stTextInput input {
    height: 48px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Language
# -------------------------------------------------
lang = st.radio("Language / Dil", ["TR", "EN"], horizontal=True)

# -------------------------------------------------
# Texts
# -------------------------------------------------
T = {
    "companies": {
        "title": {
            "TR": "Toplam şirket sayısı (1–12, 0 = sınırsız)",
            "EN": "Total number of companies (1–12, 0 = unlimited)"
        },
        "note": {
            "TR": "0 girildiğinde fabrika sayısındaki sınır kalkar.",
            "EN": "If 0 is entered, the factory limit is removed."
        }
    },
    "engine": {
        "title": {
            "TR": "Automated Engine Seviyesi (1–7)",
            "EN": "Automated Engine Level (1–7)"
        },
        "note": {
            "TR": "Bütün fabrikalarınızın eşit seviyede olduğu varsayılır.",
            "EN": "All factories are assumed to be at the same level."
        }
    },
    "bonus": {
        "title": {
            "TR": "Sahip olduğunuz şirketlerin üretim bonusu (%)",
            "EN": "Production bonus of your companies (%)"
        },
        "note": {
            "TR": "Tüm fabrikaların aynı ürünü ürettiği varsayılır.",
            "EN": "All factories are assumed to produce the same product."
        }
    },
    "price": {
        "title": {
            "TR": "Ürün market satış fiyatı (PP başına)",
            "EN": "Market sale price (per PP)"
        },
        "note": {
            "TR": "Tek ürün üzerinden hesaplanır.",
            "EN": "Calculated for a single product."
        }
    },
    "salary": {
        "title": {
            "TR": "Maaş (PP başına)",
            "EN": "Salary (per PP)"
        },
        "note": {"TR": "", "EN": ""}
    },
    "tax": {
        "title": {
            "TR": "Vergi oranı (%)",
            "EN": "Tax rate (%)"
        },
        "note": {"TR": "", "EN": ""}
    },
    "skill": {
        "title": {
            "TR": "Toplam Skill Puanı",
            "EN": "Total Skill Points"
        },
        "note": {
            "TR": "Seviye × 4",
            "EN": "Level × 4"
        }
    },
    "result": {
        "title": {"TR": "En İyi Skill Dağılımı", "EN": "Best Skill Distribution"},
        "profit": {"TR": "Günlük Maksimum BTC", "EN": "Maximum Daily BTC"},
        "companies": {"TR": "Toplam Şirket", "EN": "Total Companies"}
    }
}

# -------------------------------------------------
# Images
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def img(path):
    return Image.open(os.path.join(BASE_DIR, path))

images = {
    "companies": img(".devcontainer/companies.png"),
    "engine": img(".devcontainer/automated_engine.png"),
    "bonus": img(".devcontainer/comp_bonus.png"),
    "market": img(".devcontainer/market.png"),
    "salary": img(".devcontainer/PP_maas.png"),
    "tax": img(".devcontainer/tax.png"),
    "skill": img(".devcontainer/skill_point.png"),
    "entrepreneurship": img(".devcontainer/entrepreneurship.png"),
    "energy": img(".devcontainer/energy.png"),
    "production": img(".devcontainer/production.png"),
    "company_limit": img(".devcontainer/company_limit.png")
}

# -------------------------------------------------
# Input with icon (FINAL)
# -------------------------------------------------
def input_with_icon(title, note, icon, default, key):
    st.markdown(f"### {title}")
    if note:
        st.markdown(f"<div class='small-note'>{note}</div>", unsafe_allow_html=True)

    col_icon, col_input = st.columns([2, 6])

    with col_icon:
        st.markdown(
            "<div style='display:flex; align-items:center; height:48px;'>",
            unsafe_allow_html=True
        )
        st.image(icon, width=52)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_input:
        return st.text_input(
            "",
            value=default,
            key=key,
            label_visibility="collapsed"
        )

# -------------------------------------------------
# Inputs
# -------------------------------------------------
current_companies = int(input_with_icon(
    T["companies"]["title"][lang],
    T["companies"]["note"][lang],
    images["companies"],
    "6",
    "companies"
))

engine_level = int(input_with_icon(
    T["engine"]["title"][lang],
    T["engine"]["note"][lang],
    images["engine"],
    "3",
    "engine"
))

company_bonus = float(input_with_icon(
    T["bonus"]["title"][lang],
    T["bonus"]["note"][lang],
    images["bonus"],
    "31",
    "bonus"
))

price_pp = float(input_with_icon(
    T["price"]["title"][lang],
    T["price"]["note"][lang],
    images["market"],
    "0.05",
    "price"
))

z = float(input_with_icon(
    T["salary"]["title"][lang],
    T["salary"]["note"][lang],
    images["salary"],
    "0.07",
    "salary"
))

tax_rate = float(input_with_icon(
    T["tax"]["title"][lang],
    T["tax"]["note"][lang],
    images["tax"],
    "8",
    "tax"
))

S = int(input_with_icon(
    T["skill"]["title"][lang],
    T["skill"]["note"][lang],
    images["skill"],
    "56",
    "skill"
))

# -------------------------------------------------
# Calculation
# -------------------------------------------------
if st.button("Hesapla / Calculate 🚀"):

    Q = price_pp * (1 + company_bonus / 100)
    engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
    K = Q * engine_values[engine_level]

    def skill_cost(l): return l * (l + 1) // 2

    levels = range(11)
    base_companies = 2

    lc_levels = range(11) if current_companies == 0 else range(max(current_companies - base_companies, 0) + 1)

    best_Z = -1

    for Lg, Lw, Lp, Lc in itertools.product(levels, levels, levels, lc_levels):
        if skill_cost(Lg)+skill_cost(Lw)+skill_cost(Lp)+skill_cost(Lc) > S:
            continue

        Xp = 10 + 3 * Lp
        Xg = (30 + 5 * Lg) * Xp / 10
        Xw = (30 + 10 * Lw) * Xp / 10
        Xc = base_companies + Lc

        Z = (
            2.4 * Q * Xg +
            2.4 * z * (1 - tax_rate / 100) * Xw +
            K * Xc
        )

        if Z > best_Z:
            best_Z = Z
            best_combo = (Lg, Lw, Lp, Lc)
            best_companies = Xc

    st.markdown("---")
    st.markdown(f"## 🔝 {T['result']['title'][lang]}")

    def result_row(label, icon, value):
        col1, col2 = st.columns([1, 6])
        with col1:
            st.image(icon, width=40)
        with col2:
            st.markdown(f"**{label}:** {value}")

    result_row("Entrepreneurship", images["entrepreneurship"], best_combo[0])
    result_row("Energy", images["energy"], best_combo[1])
    result_row("Production", images["production"], best_combo[2])
    result_row("Company Limit", images["company_limit"], best_combo[3])

    st.markdown(f"**{T['result']['companies'][lang]}:** {best_companies}")
    st.markdown(f"**{T['result']['profit'][lang]}:** `{round(best_Z, 2)}`")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.markdown(
    "Made by [Monarch](https://app.warera.io/user/681f630b1353a30ceefec393)",
    unsafe_allow_html=True
)
