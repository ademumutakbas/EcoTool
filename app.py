import streamlit as st
import itertools
from PIL import Image

st.title("Eco Skill Optimizer")

# ---------------- Fotoğrafları yükle ----------------
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

ICON_WIDTH = 40  # input ikonları için boyut
RESULT_ICON_WIDTH = 50  # sonuç ikonları için boyut

# ---------------- Kullanıcı girdileri ----------------
def get_float_input_with_icon(label, img, default="0.05"):
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(img, width=ICON_WIDTH)
    with col2:
        val_str = st.text_input(label, value=default)
        try:
            val = float(val_str)
            return val
        except ValueError:
            st.warning("Lütfen geçerli bir sayı girin (örn. 0.05).")
            st.stop()

q_price = get_float_input_with_icon("Entrepreneur ile üreteceğin ürünün PP başına market fiyatı", images["market"])
q_bonus = get_float_input_with_icon("Şirketinin bonusu % (örn. 31)", images["comp_bonus"])

z = get_float_input_with_icon("Energy ile PP başına maaş (örn. 0.07)", images["PP_maas"])
tax_rate = get_float_input_with_icon("Maaş vergisi % (örn. 5)", images["tax"])

k_price = get_float_input_with_icon("Kendi şirketinde ürettiğin ürünün PP başına market fiyatı (örn. 0.05)", images["market"])
k_bonus = get_float_input_with_icon("Şirketlerinin bonusu % (örn. 31)", images["comp_bonus"])

engine_level_str = st.text_input("Automated Engine Seviyesi (1-7)", "4")
try:
    engine_level = int(engine_level_str)
    if engine_level < 1 or engine_level > 7:
        raise ValueError
except ValueError:
    st.warning("Lütfen 1 ile 7 arasında bir sayı girin.")
    st.stop()

S_str = st.text_input("Toplam Skill Puanı", "56")
try:
    S = int(S_str)
except ValueError:
    st.warning("Lütfen geçerli bir tam sayı girin.")
    st.stop()

current_companies_str = st.text_input("Mevcut şirket sayısı (0 girersen kısıt kalkar)", "0")
try:
    current_companies = int(current_companies_str)
    if current_companies < 0 or current_companies > 12:
        raise ValueError
except ValueError:
    st.warning("0-12 arasında bir sayı girin.")
    st.stop()

# ---------------- Hesaplama ----------------
if st.button("Hesapla"):
    Q = q_price * (1 + q_bonus/100)
    engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
    K = k_price * (1 + k_bonus/100) * engine_values[engine_level]

    levels = range(0, 11)  # Skill seviyeleri 0-10
    def skill_cost(level):
        return level*(level+1)//2

    base_companies = 2
    opened_companies = max(current_companies - base_companies, 0)
    if current_companies == 0:
        lc_levels = range(0, 11)  # kısıt yok
    else:
        lc_max = opened_companies
        lc_levels = range(0, lc_max+1)

    best_Z = -1
    best_combination = None
    best_total_companies = None

    for Lg, Lw, Lp, Lc in itertools.product(levels, levels, levels, lc_levels):
        cost = skill_cost(Lg) + skill_cost(Lw) + skill_cost(Lp) + skill_cost(Lc)
        if cost > S:
            continue

        Xp = 10 + 3*Lp
        Xg = (30 + 5*Lg) * Xp / 10
        Xw = (30 + 10*Lw) * Xp / 10
        Xc = base_companies + Lc
        Z_net = z*(1 - tax_rate/100)
        Z_total = 2.4*Q*Xg + 2.4*Z_net*Xw + K*Xc

        if Z_total > best_Z:
            best_Z = Z_total
            best_combination = (Lg,Lw,Lp,Lc)
            best_total_companies = Xc

    # ---------------- Sonuç ----------------
    if best_combination:
        st.markdown("### En iyi kombinasyon:")
        result_cols = st.columns([1, 5])
        with result_cols[0]:
            st.image(images["entrepreneurship"], width=RESULT_ICON_WIDTH)
        with result_cols[1]:
            st.write(f"Lg (Entrepreneurship): {best_combination[0]}")

        result_cols = st.columns([1, 5])
        with result_cols[0]:
            st.image(images["energy"], width=RESULT_ICON_WIDTH)
        with result_cols[1]:
            st.write(f"Lw (Energy): {best_combination[1]}")

        result_cols = st.columns([1, 5])
        with result_cols[0]:
            st.image(images["production"], width=RESULT_ICON_WIDTH)
        with result_cols[1]:
            st.write(f"Lp (Production): {best_combination[2]}")

        result_cols = st.columns([1, 5])
        with result_cols[0]:
            st.image(images["company_limit"], width=RESULT_ICON_WIDTH)
        with result_cols[1]:
            st.write(f"Lc (Company Limit): {best_combination[3]}")

        st.write(f"Toplam şirket: {best_total_companies}")
        st.write(f"Max Z (Günlük Max Kazanç): {round(best_Z,2)}")

    else:
        st.warning("Geçerli bir kombinasyon bulunamadı!")

# ---------------- Alt bilgi ----------------
st.markdown("Made by [Monarch](https://app.warera.io/user/681f630b1353a30ceefec393)")

