import streamlit as st
import itertools
from PIL import Image

# ---------------- Dil Seçimi ----------------
lang = st.selectbox("Dil / Language", ["Türkçe", "English"])

# ---------------- Metin sözlüğü ----------------
texts = {
    "title": {"Türkçe": "Eco Skill Optimizer", "English": "Eco Skill Optimizer"},
    "input_labels": {
        "q_price": {"Türkçe": "Entrepreneur ile üreteceğin ürünün PP başına market fiyatı", 
                    "English": "Market price per PP for the product produced with Entrepreneur"},
        "q_bonus": {"Türkçe": "Şirketinin bonusu % (örn. 31)", "English": "Your company's bonus % (e.g. 31)"},
        "z": {"Türkçe": "Energy ile PP başına maaş (örn. 0.07)", "English": "Salary per PP with Energy (e.g. 0.07)"},
        "tax_rate": {"Türkçe": "Maaş vergisi % (örn. 5)", "English": "Salary tax % (e.g. 5)"},
        "k_price": {"Türkçe": "Kendi şirketinde ürettiğin ürünün PP başına market fiyatı (örn. 0.05)", 
                    "English": "Market price per PP for the product in your company (e.g. 0.05)"},
        "k_bonus": {"Türkçe": "Şirketlerinin bonusu % (örn. 31)", "English": "Your company's bonus % (e.g. 31)"},
        "engine_level": {"Türkçe": "Automated Engine Seviyesi (1-7)", "English": "Automated Engine Level (1-7)"},
        "S": {"Türkçe": "Toplam Skill Puanı", "English": "Total Skill Points"},
        "current_companies": {"Türkçe": "Mevcut şirket sayısı (0 girersen kısıt kalkar)", 
                              "English": "Current companies (0 to ignore limit)"}
    },
    "button": {"Türkçe": "Hesapla", "English": "Calculate"},
    "result_title": {"Türkçe": "En iyi kombinasyon:", "English": "Best combination:"},
    "result_labels": {
        "Lg": {"Türkçe": "Lg (Entrepreneurship)", "English": "Lg (Entrepreneurship)"},
        "Lw": {"Türkçe": "Lw (Energy)", "English": "Lw (Energy)"},
        "Lp": {"Türkçe": "Lp (Production)", "English": "Lp (Production)"},
        "Lc": {"Türkçe": "Lc (Company Limit)", "English": "Lc (Company Limit)"}
    },
    "total_companies": {"Türkçe": "Toplam şirket", "English": "Total companies"},
    "max_Z": {"Türkçe": "Max Z (Günlük Max Kazanç)", "English": "Max Z (Daily Max Profit)"},
    "invalid_number": {"Türkçe": "Lütfen geçerli bir sayı girin (örn. 0.05).",
                       "English": "Please enter a valid number (e.g. 0.05)."},
    "invalid_integer": {"Türkçe": "Lütfen geçerli bir tam sayı girin.", "English": "Please enter a valid integer."},
    "invalid_engine": {"Türkçe": "Lütfen 1 ile 7 arasında bir sayı girin.", "English": "Please enter a number between 1 and 7."},
    "warning_no_combination": {"Türkçe": "Geçerli bir kombinasyon bulunamadı!", 
                               "English": "No valid combination found!"}
}

st.title(texts["title"][lang])

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

INPUT_ICON_WIDTH = 100
RESULT_ICON_WIDTH = 50

# ---------------- Kullanıcı girdileri ----------------
def get_float_input_with_icon(label_key, img, default="0.05"):
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(img, width=INPUT_ICON_WIDTH)
    with col2:
        val_str = st.text_input(texts["input_labels"][label_key][lang], value=default)
        try:
            val = float(val_str)
            return val
        except ValueError:
            st.warning(texts["invalid_number"][lang])
            st.stop()

q_price = get_float_input_with_icon("q_price", images["market"])
q_bonus = get_float_input_with_icon("q_bonus", images["comp_bonus"])
z = get_float_input_with_icon("z", images["PP_maas"])
tax_rate = get_float_input_with_icon("tax_rate", images["tax"])
k_price = get_float_input_with_icon("k_price", images["market"])
k_bonus = get_float_input_with_icon("k_bonus", images["comp_bonus"])

# Diğer inputlar
col1, col2 = st.columns([1,5])
with col1: st.image(images["automated_engine"], width=INPUT_ICON_WIDTH)
with col2:
    engine_level_str = st.text_input(texts["input_labels"]["engine_level"][lang], "4")
try:
    engine_level = int(engine_level_str)
    if engine_level < 1 or engine_level > 7:
        raise ValueError
except ValueError:
    st.warning(texts["invalid_engine"][lang])
    st.stop()

col1, col2 = st.columns([1,5])
with col1: st.image(images["skill_point"], width=INPUT_ICON_WIDTH)
with col2:
    S_str = st.text_input(texts["input_labels"]["S"][lang], "56")
try:
    S = int(S_str)
except ValueError:
    st.warning(texts["invalid_integer"][lang])
    st.stop()

col1, col2 = st.columns([1,5])
with col1: st.image(images["companies"], width=INPUT_ICON_WIDTH)
with col2:
    current_companies_str = st.text_input(texts["input_labels"]["current_companies"][lang], "0")
try:
    current_companies = int(current_companies_str)
    if current_companies < 0 or current_companies > 12:
        raise ValueError
except ValueError:
    st.warning("0-12 arasında bir sayı girin.")
    st.stop()

# ---------------- Hesaplama ----------------
if st.button(texts["button"][lang]):
    Q = q_price * (1 + q_bonus/100)
    engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
    K = k_price * (1 + k_bonus/100) * engine_values[engine_level]

    levels = range(0, 11)
    def skill_cost(level):
        return level*(level+1)//2

    base_companies = 2
    opened_companies = max(current_companies - base_companies, 0)
    lc_levels = range(0, 11) if current_companies==0 else range(0, opened_companies+1)

    best_Z = -1
    best_combination = None
    best_total_companies = None

    for Lg, Lw, Lp, Lc in itertools.product(levels, levels, levels, lc_levels):
        cost = skill_cost(Lg)+skill_cost(Lw)+skill_cost(Lp)+skill_cost(Lc)
        if cost > S: continue
        Xp = 10 + 3*Lp
        Xg = (30+5*Lg)*Xp/10
        Xw = (30+10*Lw)*Xp/10
        Xc = base_companies + Lc
        Z_net = z*(1-tax_rate/100)
        Z_total = 2.4*Q*Xg + 2.4*Z_net*Xw + K*Xc
        if Z_total>best_Z:
            best_Z=Z_total
            best_combination=(Lg,Lw,Lp,Lc)
            best_total_companies=Xc

    # ---------------- Sonuç ----------------
    if best_combination:
        st.markdown(f"### {texts['result_title'][lang]}")
        # Lg
        col1, col2 = st.columns([1,5])
        with col1: st.image(images["entrepreneurship"], width=RESULT_ICON_WIDTH)
        with col2: st.write(f"{texts['result_labels']['Lg'][lang]}: {best_combination[0]}")
        # Lw
        col1, col2 = st.columns([1,5])
        with col1: st.image(images["energy"], width=RESULT_ICON_WIDTH)
        with col2: st.write(f"{texts['result_labels']['Lw'][lang]}: {best_combination[1]}")
        # Lp
        col1, col2 = st.columns([1,5])
        with col1: st.image(images["production"], width=RESULT_ICON_WIDTH)
        with col2: st.write(f"{texts['result_labels']['Lp'][lang]}: {best_combination[2]}")
        # Lc
        col1, col2 = st.columns([1,5])
        with col1: st.image(images["company_limit"], width=RESULT_ICON_WIDTH)
        with col2: st.write(f"{texts['result_labels']['Lc'][lang]}: {best_combination[3]}")

        st.write(f"{texts['total_companies'][lang]}: {best_total_companies}")
        st.write(f"{texts['max_Z'][lang]}: {round(best_Z,2)}")
    else:
        st.warning(texts["warning_no_combination"][lang])

# ---------------- Alt bilgi ----------------
st.markdown("Made by [Monarch](https://app.warera.io/user/681f630b1353a30ceefec393)")
