import streamlit as st
import itertools

st.title("Skill Point Optimizasyon Aracı")

# ---------------- Kullanıcı girdileri ----------------
q_price = st.number_input("Entrepreneur ile üreteceğin ürünün PP başına market fiyatı", min_value=0.0, format="%.3f")
q_bonus = st.number_input("Şirketinin bonusu %", min_value=0.0, format="%.1f")

z = st.number_input("Energy ile PP başına maaş", min_value=0.0, format="%.3f")
tax = st.number_input("Maaş vergisi %", min_value=0.0, format="%.1f")

k_price = st.number_input("Kendi şirketinde ürettiğin ürünün PP başına fiyatı", min_value=0.0, format="%.3f")
k_bonus = st.number_input("Şirketinin bonusu %", min_value=0.0, format="%.1f")

engine_level = st.number_input("Automated Engine Seviyesi (1-7)", min_value=1, max_value=7, step=1)
S = st.number_input("Toplam Skill Puanı", min_value=1, step=1)
mevcut_sirket = st.number_input("Mevcut şirket sayısı (0 girersen kısıt kalkar)", min_value=0, max_value=12, step=1)

if st.button("Hesapla"):
    # ---------------- Hesaplamalar ----------------
    Q = q_price * (1 + q_bonus/100)

    engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
    K = k_price * (1 + k_bonus/100) * engine_values[engine_level]

    def skill_cost(level):
        return max(level*(level+1)//2 - 1, 0)

    best_Z = -1
    best_combination = None
    best_total_companies = None

    levels = range(0, 11)

    for Lg, Lw, Lp, Lc in itertools.product(levels, repeat=4):
        cost = skill_cost(Lg) + skill_cost(Lw) + skill_cost(Lp) + skill_cost(Lc)
        if cost > S:
            continue

        # Şirket kısıtı
        if mevcut_sirket > 0:
            mevcut_Lc = mevcut_sirket - 2
            if Lc > mevcut_Lc:
                continue

        Xp = 10 + 3*Lp
        Xg = (30 + 5*Lg) * Xp / 10
        Xw = (30 + 10*Lw) * Xp / 10
        Xc = 2 + Lc

        Z_total = 2.4*Q*Xg + 2.4*z*(1 - tax/100)*Xw + K*Xc

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
        - Max Z: {round(best_Z, 2)}
        """)
