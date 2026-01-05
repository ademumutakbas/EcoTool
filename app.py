import streamlit as st
import itertools
from PIL import Image
import os

st.set_page_config(
    page_title="Eco Skill Optimizer",
    layout="centered"
)

# ---------------- Genel stil ----------------
st.markdown("""
<style>
.small-note {
    font-size: 13px;
    color: #777;
    margin-top: -8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Dil ----------------
lang = st.radio("Language / Dil", ["TR", "EN"], horizontal=True)

# ---------------- Path ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def img(path):
    return Image.open(os.path.join(BASE_DIR, path))

# ---------------- Görseller ----------------
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

INPUT_ICON_WIDTH = 90
RESULT_ICON_WIDTH = 45

# ---------------- Input fonksiyonları ----------------
def float_input(title, note, img_icon, default, key):
    st.markdown(f"### {title}")
    if note:
        st.markdown(f"<div class='small-note'>{note}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(img_icon, width=INPUT_ICON_WIDTH)
    with col2:
        return st.text_input("", value=default, key=key)

def int_input(title, note, img_icon, default, key):
    st.markdown(f"### {title}")
    if note:
        st.markdown(f"<div class='small-note'>{note}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(img_icon, width=INPUT_ICON_WIDTH)
    with col2:
        return st.text_input("", value=default, key=key)

# ---------------- INPUTLAR ----------------
current_companies = int(
    int_input(
        "Toplam şirket sayısı (1–12, 0 = sınırsız)",
        "0 girildiğinde fabrika sayısındaki sınır kalkar.",
        images["companies"],
        "6",
        "companies"
    )
)

engine_level = int(
    int_input(
        "Automated Engine Seviyesi (1–7)",
        "Bütün fabrikalarınızın eşit seviyede olduğu varsayılır.",
        images["engine"],
        "3",
        "engine"
    )
)

company_bonus = float(
    float_input(
        "Sahip olduğunuz şirketlerin üretim bonusu (%)",
        "Bütün fabrikalarınızın aynı ürünü ürettiği ve aynı bölgede olduğu varsayılmalıdır.",
        images["bonus"],
        "31",
        "bonus"
    )
)

price_pp = float(
    float_input(
        "Kendi şirketlerinizde üretilen ürünün market satış fiyatı (PP başına)",
        "Tek çeşit ürün ürettiğiniz baz alınır. Maksimum kâr sağlayan ürünü kendiniz belirlemelisiniz.",
        images["market"],
        "0.05",
        "price"
    )
)

z = float(
    float_input(
        "Çalıştığınız yerde aldığınız maaş (PP başına)",
        "",
        images["salary"],
        "0.07",
        "salary"
    )
)

tax_rate = float(
    float_input(
        "Aldığınız maaşın vergisi (%)",
        "",
        images["tax"],
        "8",
        "tax"
    )
)

S = int(
    int_input(
        "Toplam Skill Puanı",
        "Güncel Seviye × 4",
        images["skill"],
        "56",
        "skill"
    )
)

# ---------------- HESAPLAMA ----------------
if st.button("Hesapla 🚀"):

    Q = price_pp * (1 + company_bonus / 100)
    engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
    K = Q * engine_values[engine_level]

    def skill_cost(l): return l * (l + 1) // 2

    levels = range(11)
    base_companies = 2

    if current_companies == 0:
        lc_levels = range(11)
    else:
        lc_levels = range(max(current_companies - base_companies, 0) + 1)

    best_Z = -1
    best_combo = None
    best_companies = None

    for Lg, Lw, Lp, Lc in itertools.product(levels, levels, levels, lc_levels):
        if skill_cost(Lg)+skill_cost(Lw)+skill_cost(Lp)+skill_cost(Lc) > S:
            continue

        Xp = 10 + 3*Lp
        Xg = (30 + 5*Lg) * Xp / 10
        Xw = (30 + 10*Lw) * Xp / 10
        Xc = base_companies + Lc

        Z = (
            2.4 * Q * Xg +
            2.4 * z * (1 - tax_rate/100) * Xw +
            K * Xc
        )

        if Z > best_Z:
            best_Z = Z
            best_combo = (Lg, Lw, Lp, Lc)
            best_companies = Xc

    # ---------------- SONUÇ ----------------
    st.markdown("---")
    st.markdown("## 🔝 En İyi Skill Dağılımı")

    def result_row(label, img_icon, value):
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(img_icon, width=RESULT_ICON_WIDTH)
        with col2:
            st.markdown(f"**{label}:** {value}")

    result_row("Entrepreneurship", images["entrepreneurship"], best_combo[0])
    result_row("Energy", images["energy"], best_combo[1])
    result_row("Production", images["production"], best_combo[2])
    result_row("Company Limit", images["company_limit"], best_combo[3])

    st.markdown(f"**Toplam Şirket:** {best_companies}")
    st.markdown(f"**Günlük Maksimum BTC Kazancı:** `{round(best_Z, 2)}`")

# ---------------- Footer ----------------
st.markdown("---")
st.markdown(
    "Made by [Monarch](https://app.warera.io/user/681f630b1353a30ceefec393)",
    unsafe_allow_html=True
)
