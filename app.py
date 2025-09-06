import streamlit as st
import itertools
from PIL import Image

st.set_page_config(page_title="Eco Skill Optimizer")

# ---------------- Dil seçimi ----------------
lang = st.radio("Language / Dil", ["TR", "EN"])

texts = {
    "input_labels": {
        "q_price": {"TR": "Entrepreneur ürünü piyasa fiyatı (PP başına)", 
                    "EN": "Market price per PP (Entrepreneur)"},
        "q_bonus": {"TR": "Şirket bonusu % (örn. 31 için 31 yaz)", 
                    "EN": "Company bonus % (e.g. 31)"},
        "z": {"TR": "Enerji maaşı (PP başına)", 
              "EN": "Salary per PP (Energy)"},
        "tax_rate": {"TR": "Maaş vergisi % (örn. 31 için 31 yaz)", 
                     "EN": "Salary tax % (e.g. 31)"},
        "k_price": {"TR": "Kendi şirketinde ürün fiyatı (PP başına)", 
                    "EN": "Market price per PP (Own company)"},
        "k_bonus": {"TR": "Kendi şirket bonusu % (örn. 31 için 31 yaz)", 
                    "EN": "Companies' bonus % (e.g. 31)"},
        "engine_level": {"TR": "Automated Engine Seviyesi (1-7)", 
                         "EN": "Automated Engine Level (1-7)"},
        "S": {"TR": "Toplam Skill Puanı (Güncel Seviye × 4)", 
              "EN": "Total Skill Points = Current Level × 4"},
        "current_companies": {"TR": "Mevcut şirket sayısı (0 = sınırsız)", 
                              "EN": "Current companies (0 = no limit)"}
    },
    "results": {
        "title": {"TR": "En iyi kombinasyon:", "EN": "Best combination:"},
        "Lg": {"TR": "Lg (Entrepreneurship)", "EN": "Lg (Entrepreneurship)"},
        "Lw": {"TR": "Lw (Energy)", "EN": "Lw (Energy)"},
        "Lp": {"TR": "Lp (Production)", "EN": "Lp (Production)"},
        "Lc": {"TR": "Lc (Company Limit)", "EN": "Lc (Company Limit)"},
        "total_companies": {"TR": "Toplam şirket", "EN": "Total companies"},
        "max_z": {"TR": "Max Z (Günlük Max Kazanç)", "EN": "Max Z (Daily Profit)"}
    }
}

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

INPUT_ICON_WIDTH = 100  # input ikonları
RESULT_ICON_WIDTH = 50  # sonuç ikonları

# ---------------- Fonksiyon ----------------
def get_float_input_with_icon(label_key, img, default="0.05"):
    col1, col2 = st.columns([1,5])
    with col1:
        st.image(img, width=INPUT_ICON_WIDTH)
    with col2:
        val_str = st.text_input(texts["input_labels"][label_key][lang], value=default, key=f"{label_key}_{lang}")
        try:
            val = float(val_str)
            return val
        except ValueError:
            st.warning("Lütfen geçerli bir sayı girin (örn. 0.05). / Enter a valid number (e.g., 0.05).")
            st.stop()

def get_int_input_with_icon(label_key, img, default="4"):
    col1, col2 = st.columns([1,5])
    with col1:
        st.image(img, width=INPUT_ICON_WIDTH)
    with col2:
        val_str = st.text_input(texts["input_labels"][label_key][lang], value=default, key=f"{label_key}_{lang}")
        try:
            val = int(val_str)
            return val
        except ValueError:
            st.warning("Lütfen geçerli bir tam sayı girin. / Enter a valid integer.")
            st.stop()

# ---------------- Kullanıcı girdileri ----------------
q_price = get_float_input_with_icon("q_price", images["market"], default="0.05")
q_bonus = get_float_input_with_icon("q_bonus", images["comp_bonus"], default="31")
z = get_float_input_with_icon("z", images["PP_maas"], default="0.07")
tax_rate = get_float_input_with_icon("tax_rate", images["tax"], default="8")
k_price = get_float_input_with_icon("k_price", images["market"], default="0.05")
k_bonus = get_float_input_with_icon("k_bonus", images["comp_bonus"], default="31")

engine_level = get_int_input_with_icon("engine_level", images["automated_engine"], default="3")
S = get_int_input_with_icon("S", images["skill_point"], default="56")
current_companies = get_int_input_with_icon("current_companies", images["companies"], default="6")

# ---------------- Hesaplama ----------------
if st.button("Hesapla"):
    Q = q_price * (1 + q_bonus/100)
    engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
    K = k_price * (1 + k_bonus/100) * engine_values[engine_level]

    levels = range(0, 11)
    def skill_cost(level):
        return level*(level+1)//2

    base_companies = 2
    opened_companies = max(current_companies - base_companies, 0)
    if current_companies == 0:
        lc_levels = range(0, 11)
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
        st.markdown(f"### {texts['results']['title'][lang]}")
        def show_result(label_key, img, value):
            col1, col2 = st.columns([1,5])
            with col1:
                st.image(img, width=RESULT_ICON_WIDTH)
            with col2:
                st.write(f"{texts['results'][label_key][lang]}: {value}")
        show_result("Lg", images["entrepreneurship"], best_combination[0])
        show_result("Lw", images["energy"], best_combination[1])
        show_result("Lp", images["production"], best_combination[2])
        show_result("Lc", images["company_limit"], best_combination[3])

        st.write(f"{texts['results']['total_companies'][lang]}: {best_total_companies}")
        st.write(f"{texts['results']['max_z'][lang]}: {round(best_Z,2)}")
    else:
        st.warning("Geçerli bir kombinasyon bulunamadı! / No valid combination found!")

# ---------------- Alt bilgi ----------------
st.markdown("Made by [Monarch](https://app.warera.io/user/681f630b1353a30ceefec393)")

