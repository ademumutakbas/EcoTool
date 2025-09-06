import streamlit as st
import itertools
from PIL import Image

st.set_page_config(page_title="EcoTool", page_icon="⚔️", layout="wide")

# ---------------- CSS Tasarım ----------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: #f1f5f9;
        font-family: 'Trebuchet MS', sans-serif;
    }
    h1 {
        color: #facc15;
        text-shadow: 2px 2px #000;
        text-align: center;
        font-size: 48px !important;
        margin-bottom: 0px;
    }
    .slogan {
        text-align: center;
        font-size: 20px;
        color: #e2e8f0;
        margin-bottom: 30px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #f97316, #ec4899);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 24px;
        transition: 0.3s;
        border: none;
        box-shadow: 0px 0px 12px rgba(249,115,22,0.6);
    }
    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #ec4899, #f97316);
        box-shadow: 0px 0px 18px rgba(236,72,153,0.8);
    }
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: #f1f5f9;
        border: 1px solid #f97316;
        border-radius: 8px;
        padding: 6px;
    }
    .result-box {
        background: rgba(17,24,39,0.85);
        border-radius: 10px;
        padding: 10px;
        margin: 8px 0;
        border: 1px solid #f97316;
        box-shadow: 0 0 6px rgba(249,115,22,0.4);
        font-size: 16px;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
    }
    .footer a {
        color: #f97316;
        font-weight: bold;
        text-decoration: none;
        transition: 0.3s;
    }
    .footer a:hover {
        color: #ec4899;
        text-shadow: 0px 0px 8px #ec4899;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Başlık ----------------
st.markdown("<h1>EcoTool ⚔️</h1>", unsafe_allow_html=True)
st.markdown("<div class='slogan'>Optimize your skills, maximize your profit 🚀</div>", unsafe_allow_html=True)

# ---------------- Dil seçimi ----------------
lang = st.radio("🌍 Language / Dil", ["TR", "EN"], horizontal=True)

texts = {
    "input_labels": {
        "q_price": {"TR": "Entrepreneur piyasa fiyatı (PP)", "EN": "Market price per PP (Entrepreneur)"},
        "q_bonus": {"TR": "Şirket bonusu %", "EN": "Company bonus %"},
        "z": {"TR": "Enerji maaşı (PP başına)", "EN": "Salary per PP (Energy)"},
        "tax_rate": {"TR": "Maaş vergisi %", "EN": "Salary tax %"},
        "k_price": {"TR": "Kendi şirket fiyatı (PP)", "EN": "Own company price per PP"},
        "k_bonus": {"TR": "Kendi şirket bonusu %", "EN": "Own company bonus %"},
        "engine_level": {"TR": "Automated Engine (1-7)", "EN": "Automated Engine (1-7)"},
        "S": {"TR": "Toplam Skill Puanı", "EN": "Total Skill Points"},
        "current_companies": {"TR": "Mevcut şirket sayısı (0 = sınırsız)", "EN": "Current companies (0 = no limit)"}
    },
    "results": {
        "title": {"TR": "🔥 En iyi kombinasyon:", "EN": "🔥 Best combination:"},
        "Lg": {"TR": "Lg (Entrepreneurship)", "EN": "Lg (Entrepreneurship)"},
        "Lw": {"TR": "Lw (Energy)", "EN": "Lw (Energy)"},
        "Lp": {"TR": "Lp (Production)", "EN": "Lp (Production)"},
        "Lc": {"TR": "Lc (Company Limit)", "EN": "Lc (Company Limit)"},
        "total_companies": {"TR": "Toplam şirket", "EN": "Total companies"},
        "max_z": {"TR": "Max Z (Günlük Max Kazanç)", "EN": "Max Z (Daily Profit)"}
    }
}

# ---------------- Grid düzeniyle inputlar ----------------
cols = st.columns(3)
q_price = cols[0].text_input(texts["input_labels"]["q_price"][lang], "0.05")
q_bonus = cols[1].text_input(texts["input_labels"]["q_bonus"][lang], "31")
z = cols[2].text_input(texts["input_labels"]["z"][lang], "0.07")

cols = st.columns(3)
tax_rate = cols[0].text_input(texts["input_labels"]["tax_rate"][lang], "8")
k_price = cols[1].text_input(texts["input_labels"]["k_price"][lang], "0.05")
k_bonus = cols[2].text_input(texts["input_labels"]["k_bonus"][lang], "31")

cols = st.columns(3)
engine_level = cols[0].text_input(texts["input_labels"]["engine_level"][lang], "3")
S = cols[1].text_input(texts["input_labels"]["S"][lang], "56")
current_companies = cols[2].text_input(texts["input_labels"]["current_companies"][lang], "6")

# ---------------- Hesaplama ----------------
if st.button("🚀 Hesapla"):
    try:
        q_price = float(q_price)
        q_bonus = float(q_bonus)
        z = float(z)
        tax_rate = float(tax_rate)
        k_price = float(k_price)
        k_bonus = float(k_bonus)
        engine_level = int(engine_level)
        S = int(S)
        current_companies = int(current_companies)
    except ValueError:
        st.warning("⚠️ Geçerli sayılar girin.")
        st.stop()

    Q = q_price * (1 + q_bonus/100)
    engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
    K = k_price * (1 + k_bonus/100) * engine_values[engine_level]

    levels = range(0, 11)
    def skill_cost(level): return level*(level+1)//2

    base_companies = 2
    opened_companies = max(current_companies - base_companies, 0)
    if current_companies == 0:
        lc_levels = range(0, 11)
    else:
        lc_levels = range(0, opened_companies+1)

    best_Z, best_combination, best_total_companies = -1, None, None
    for Lg, Lw, Lp, Lc in itertools.product(levels, levels, levels, lc_levels):
        if skill_cost(Lg)+skill_cost(Lw)+skill_cost(Lp)+skill_cost(Lc) > S:
            continue
        Xp = 10 + 3*Lp
        Xg = (30 + 5*Lg) * Xp / 10
        Xw = (30 + 10*Lw) * Xp / 10
        Xc = base_companies + Lc
        Z_net = z*(1 - tax_rate/100)
        Z_total = 2.4*Q*Xg + 2.4*Z_net*Xw + K*Xc
        if Z_total > best_Z:
            best_Z, best_combination, best_total_companies = Z_total, (Lg,Lw,Lp,Lc), Xc

    if best_combination:
        st.markdown(f"### {texts['results']['title'][lang]}")
        st.markdown(f"<div class='result-box'>{texts['results']['Lg'][lang]}: {best_combination[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-box'>{texts['results']['Lw'][lang]}: {best_combination[1]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-box'>{texts['results']['Lp'][lang]}: {best_combination[2]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-box'>{texts['results']['Lc'][lang]}: {best_combination[3]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-box'>{texts['results']['total_companies'][lang]}: {best_total_companies}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-box'>{texts['results']['max_z'][lang]}: {round(best_Z,2)}</div>", unsafe_allow_html=True)
    else:
        st.warning("❌ Geçerli bir kombinasyon bulunamadı.")

# ---------------- Alt bilgi ----------------
st.markdown("<div class='footer'>Made by <a href='https://app.warera.io/user/681f630b1353a30ceefec393' target='_blank'>Monarch</a></div>", unsafe_allow_html=True)
