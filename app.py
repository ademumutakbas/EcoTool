import streamlit as st
import itertools

st.title("Eco Skill Optimizer")

# ---------------- Kullanıcı girdileri (text_input ile float dönüşümü) ----------------
def get_float_input(label, default="0.05"):
    val_str = st.text_input(label, value=default)
    try:
        val = float(val_str)
        return val
    except ValueError:
        st.warning("Lütfen geçerli bir sayı girin (örn. 0.05).")
        st.stop()

q_price = get_float_input("Entrepreneur ile üreteceğin ürünün PP başına market fiyatı (örn. 0.05)")
q_bonus = get_float_input("Şirketinin bonusu % (örn. 31)")

z = get_float_input("Energy ile PP başına maaş (örn. 0.07)")
tax_rate = get_float_input("Maaş vergisi % (örn. 5)")

k_price = get_float_input("Kendi şirketinde ürettiğin ürünün PP başına market fiyatı (örn. 0.05)")
k_bonus = get_float_input("Şirketlerinin bonusu % (örn. 31)")

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

if st.button("Hesapla"):
    # ---------------- Hesaplamalar ----------------
    Q = q_price * (1 + q_bonus/100)

    engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
    K = k_price * (1 + k_bonus/100) * engine_values[engine_level]

    levels = range(0, 11)  # Skill seviyeleri 0-10

    def skill_cost(level):
        """Level N için gerekli skill point = 1 + 2 + ... + N"""
        return level * (level + 1) // 2

    # ---------------- Lc seviyeleri ----------------
    base_companies = 2
    opened_companies = max(current_companies - base_companies, 0)
    if current_companies == 0:
        lc_levels = range(0, 11)  # kısıt yok, 12 şirket varsay
    else:
        lc_max = opened_companies
        lc_levels = range(0, lc_max + 1)

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

        Z_net = z * (1 - tax_rate/100)
        Z_total = 2.4*Q*Xg + 2.4*Z_net*Xw + K*Xc

        if Z_total > best_Z:
            best_Z = Z_total
            best_combination = (Lg, Lw, Lp, Lc)
            best_total_companies = Xc

    # ---------------- Sonuç ----------------
    if best_combination:
        st.success(f"""
**En iyi kombinasyon:**
- Lg (Entrepreneurship): {best_combination[0]}
- Lw (Energy): {best_combination[1]}
- Lp (Production): {best_combination[2]}
- Lc (Company Limit): {best_combination[3]}
- Toplam şirket: {best_total_companies}
- Max Z (Günlük Max Kazanç): {round(best_Z, 2)}
""")
    else:
        st.warning("Geçerli bir kombinasyon bulunamadı!")

# ---------------- Alt bilgi: Made by Monarch ----------------
st.markdown("[Made by Monarch](https://app.warera.io/region/6813b70c9403bc4170a5db34)")

