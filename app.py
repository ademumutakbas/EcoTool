import streamlit as st
import itertools

st.title("Skill Point Optimizasyon Aracı")

# ---------------- Kullanıcı girdileri ----------------
q_price_str = st.text_input("Entrepreneur ile üreteceğin ürünün PP başına market fiyatı (örn. 0.05)", "0.05")
q_bonus_str = st.text_input("Şirketinin bonusu % (örn. 31)", "31")

z_str = st.text_input("Energy ile PP başına maaş (örn. 0.07)", "0.07")
tax_str = st.text_input("Maaş vergisi % (örn. 5)", "5")

k_price_str = st.text_input("Kendi şirketinde ürettiğin ürünün PP başına fiyatı (örn. 0.05)", "0.05")
k_bonus_str = st.text_input("Şirketinin bonusu % (örn. 31)", "31")

engine_level_str = st.text_input("Automated Engine Seviyesi (1-7)", "4")
S_str = st.text_input("Toplam Skill Puanı", "56")
mevcut_sirket_str = st.text_input("Mevcut şirket sayısı (0 girersen kısıt kalkar)", "0")

if st.button("Hesapla"):
    try:
        # ---------------- Hesaplamalar ----------------
        q_price = float(q_price_str)
        q_bonus = float(q_bonus_str)
        z = float(z_str)
        tax = float(tax_str)
        k_price = float(k_price_str)
        k_bonus = float(k_bonus_str)
        engine_level = int(engine_level_str)
        S = int(S_str)
        mevcut_sirket = int(mevcut_sirket_str)

        Q = q_price * (1 + q_bonus/100)
        engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
        if engine_level not in engine_values:
            st.error("Automated Engine seviyesi 1-7 arasında olmalı!")
        else:
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
                    max_Lc = min(10, 12 - mevcut_sirket)  # max 12 şirket
                    if Lc > max_Lc:
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
            else:
                st.warning("Hiçbir kombinasyon mevcut skill puanı ile mümkün değil!")

    except ValueError:
        st.error("Lütfen tüm değerleri geçerli sayılar olarak girin!")

