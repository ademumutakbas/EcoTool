import streamlit as st
import itertools

st.title("Skill Point Optimizasyon Aracı")

# ---------------- Kullanıcı girdileri ----------------
q_price_str = st.text_input("Entrepreneur ile üreteceğin ürünün PP başına market fiyatı (örn. 0.05)", "0.05")
q_bonus_str = st.text_input("Entrepreneur için Şirketlerinin bonusu % (örn. 31)", "31")

z_str = st.text_input("Energy ile PP başına maaş (örn. 0.07)", "0.07")
tax_str = st.text_input("Maaş vergisi % (örn. 5)", "5")

k_price_str = st.text_input("Kendi şirketinde ürettiğin ürünün PP başına fiyatı (örn. 0.05)", "0.05")
k_bonus_str = st.text_input("Şirketlerinin bonusu % (örn. 31)", "31")

engine_level = st.number_input("Automated Engine Seviyesi (1-7)", min_value=1, max_value=7, step=1)
S = st.number_input("Toplam Skill Puanı", min_value=1, step=1)
mevcut_sirket = st.number_input("Mevcut şirket sayısı (0 girersen kısıt kalkar)", min_value=0, max_value=12, step=1)

# Float dönüşümleri ve hata kontrolü
try:
    q_price = float(q_price_str)
    q_bonus = float(q_bonus_str)
    z = float(z_str)
    tax = float(tax_str)
    k_price = float(k_price_str)
    k_bonus = float(k_bonus_str)
except ValueError:
    st.error("Lütfen tüm değerleri doğru formatta girin (örn. 0.05, 31)")
    st.stop()

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
            max_Lc = max(0, 12 - mevcut_sirket)  # 12 şirket sınırı
            if Lc > max_Lc:
                continue

        Xp = 10 + 3*Lp
        Xg = (30 + 5*Lg) * Xp / 10
        Xw = (30 + 10*Lw) * Xp / 10
        Xc = mevcut_sirket + Lc  # mevcut + açılacak şirketler

        Z_total = 2.4*Q*Xg + 2.4*z*(1 - tax/100)*Xw + K*Xc

        if Z_total > best_Z:
            best_Z = Z_total
            best_combination =_

