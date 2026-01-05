import streamlit as st

st.set_page_config(layout="centered")

# ---------------- CSS ----------------
st.markdown("""
<style>
.block {
    background: rgba(255,255,255,0.04);
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 18px;
}

.flex {
    display: flex;
    align-items: center;
    gap: 18px;
}

.flex img {
    width: 110px;
    max-height: 110px;
    object-fit: contain;
}

.title {
    font-size: 19px;
    font-weight: 600;
}

.note {
    font-size: 13px;
    color: #9aa0a6;
    margin-top: 4px;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LANGUAGE ----------------
lang = st.radio("Language / Dil", ["TR", "EN"], horizontal=True)

TEXT = {
    "TR": {
        "companies": "Toplam şirket sayısı (1–12, 0 = sınırsız)",
        "companies_note": "0 girildiğinde fabrika sayısındaki sınır kalkar."
    },
    "EN": {
        "companies": "Total number of companies (1–12, 0 = unlimited)",
        "companies_note": "Entering 0 removes the factory limit."
    }
}

T = TEXT[lang]

# ---------------- BLOCK FUNCTION ----------------
def image_input_block(image_path, title, note, **kwargs):
    st.markdown('<div class="block">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="flex">
        <img src="data:image/png;base64,{image_to_base64(image_path)}">
        <div style="flex:1">
            <div class="title">{title}</div>
            <div class="note">{note}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    value = st.number_input("", label_visibility="collapsed", **kwargs)
    st.markdown('</div>', unsafe_allow_html=True)
    return value

# ---------------- IMAGE UTILITY ----------------
import base64
def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ---------------- INPUT ----------------
companies = image_input_block(
    "images/companies.png",
    T["companies"],
    T["companies_note"],
    min_value=0,
    max_value=12,
    value=6
)
