import streamlit as st

# =========================
# 🔹 Tema & CSS Cafcaf
# =========================
st.set_page_config(page_title="⚔️ Eco Skill Optimizer", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: #f1f5f9;
        font-family: monospace;
    }
    h1, h2, h3 {
        color: #f97316;
        text-shadow: 2px 2px #000000;
    }
    .stTextInput > div > div > input {
        background-color: #111827;
        color: #f97316;
        border: 2px solid #f97316;
        border-radius: 12px;
        font-size: 16px;
        padding: 6px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #f97316, #ec4899);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 20px;
        transition: 0.3s;
        border: none;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #ec4899, #f97316);
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# 🔹 Başlık
# =========================
st.markdown("## ⚔️ Eco Skill Optimizer")
st.markdown("Optimize et, level atla, ekonomini büyüt 🚀")

# =========================
# 🔹 Varsayılan Değerler
# =========================
default_values = [0.05, 31, 0.07, 8, 0.05, 31, 3, 56, 6]
labels = [
    "Entrepreneurship Katsayı",
    "Entrepreneurship Base Point",
    "Energy Katsayı",
    "Energy Base Point",
    "Production Katsayı",
    "Production Base Point",
    "Company Limit Katsayı",
    "Company Limit Base Point",
    "Level Sayısı"
]

# Kullanıcı girişi
inputs = []
cols = st.columns(3)
for i, label in enumerate(labels):
    with cols[i % 3]:
        val = st.number_input(label, value=default_values[i], step=1.0 if isinstance(default_values[i], int) else 0.01)
        inputs.append(val)

# =========================
# 🔹 Hesaplama Fonksiyonu
# =========================
def calculate(inputs):
    ent_coef, ent_base, en_coef, en_base, prod_coef, prod_base, comp_coef, comp_base, level = inputs
    
    skill_points = level * 4

    ent_score = ent_base + ent_coef * skill_points
    en_score = en_base + en_coef * skill_points
    prod_score = prod_base + prod_coef * skill_points
    comp_score = comp_base + comp_coef * skill_points

    return {
        "Entrepreneurship": ent_score,
        "Energy": en_score,
        "Production": prod_score,
        "Company Limit": comp_score,
        "Total Skill Points": skill_points
    }

# =========================
# 🔹 Buton & Sonuç
# =========================
if st.button("🚀 Hesapla"):
    results = calculate(inputs)
    st.success("✅ Hesaplama Tamamlandı!")

    st.subheader("📊 Sonuçlar")
    for k, v in results.items():
        st.markdown(f"**{k}:** {v:.2f}")
