import streamlit as st
import itertools

st.title("Skill Point Optimizasyon Aracı")

# ---------------- Kullanıcı girdileri ----------------
q_price_str = st.text_input("Entrepreneur ile üreteceğin ürünün PP başına market fiyatı (örn. 0.05)", "0.05")
q_bonus_str = st.text_input("Şirketinin bonusu % (örn. 31)", "31")

z_str = st.text_input("Energy ile PP başına maaş (örn. 0.07)", "0.07")
tax_str = st.text_input("Maaş vergisi % (örn. 5)", "5")

k_price_str = st.text_input("Kendi şirketinde ürettiğin ürünün PP başına fiyatı (örn. 0.05)", "0.05")
k_bonus_str = st.text_input("Şirketlerinin bonusu % (örn. 31)", "31")

engine_level = st.number_input("Automated Engine Seviyesi (1-7)", min_value=1, max_value=7, step=1)
S = st.number_input("Toplam Skill Puanı", min_value=1, step=1)
current_companies = st.number_input("Mevcut şirket sayısı (0 girersen kısıt kalkar)", min_value=0, max_value=12, step=1)

if st.button("Hesapla"):
    try:
        # String girişleri float'a çevir
        q_price = float(q_price_str)
        q_bonus = float(q_bonus_str)
        z = float(z_str)
        tax_rate = float(tax_str)
        k_price = float(k_price_str)
        k_bonus = float(k_bonus_str)
    except ValueError:
        st.error("Lütfen geçerli bir sayı girin (nokta kullanın, virgül değil)!")
    else:
        # ---------------- Hesaplamalar ----------------
        Q = q_price * (1 + q_bonus/100)

        engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
        K = k_price * (1 + k_bonus/100) * engine_values[engine_level]

        levels = range(0, 11)

        def skill_cost(level):
            return level * (level + 1) // 2

        # ---------------- Lc seviyeleri ----------------
        base_companies = 2
        opened_companies = max(current_companies - base_companies, 0)
        lc_start = 0
        lc_max = opened_companies if current_companies > 0 else 10
        lc_levels = list(range(lc_start, lc_max + 1))

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
        else:
            st.error("Geçerli bir kombinasyon bulunamadı!")

st.markdown("---")
st.markdown("Made by [Monarch](https://app.warera.io/user/681f630b1353a30ceefec393)")


