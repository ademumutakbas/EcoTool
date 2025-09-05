import itertools

# ---------------- Kullanıcı girdileri ----------------
q_price = float(input("Entrepreneur ile üreteceğin ürünün PP başına marketteki fiyatı (Virgül yerine NOKTA kullan): "))
q_bonus = float(input("Şirketinin bonusu %: "))

z = float(input("Energy ile PP başına maaş: "))
tax_rate = float(input("Maaş vergisi %: "))

k_price = float(input("Kendi şirketinde ürettiğin ürünün PP başına marketteki fiyatı: "))
k_bonus = float(input("Şirketinin bonusu %: "))
engine_level = int(input("Automated Engine Seviyesi (1-7): "))

S = int(input("Toplam Skill Puanı: "))
current_companies = int(input("Mevcut şirket sayısı: "))

# ---------------- Hesaplamalar ----------------
Q = q_price * (1 + q_bonus/100)

engine_values = {1:24,2:48,3:72,4:96,5:120,6:144,7:168}
if engine_level not in engine_values:
    raise ValueError("Automated Engine seviyesi 1-7 arasında olmalı!")

K = k_price * (1 + k_bonus/100) * engine_values[engine_level]

levels = range(0, 11)  # Skill seviyeleri 0-10

def skill_cost(level):
    """Level N için gerekli skill point = 1 + 2 + ... + N"""
    return level * (level + 1) // 2

# ---------------- Lc seviyeleri (Company Limit) ----------------
base_companies = 2  # oyun başında verilen 2 base şirket

if current_companies == 0:
    # kullanıcı 0 girerse kısıt kalkıyor, 12 şirket hakkı varmış gibi hesapla
    lc_levels = range(0, 11)
else:
    # açılabilir maksimum şirket = mevcut şirket - 2 (base)
    opened_companies = max(current_companies - base_companies, 0)
    lc_levels = range(0, opened_companies + 1)

best_Z = -1
best_combination = None

for Lg, Lw, Lp, Lc in itertools.product(levels, levels, levels, lc_levels):
    cost = skill_cost(Lg) + skill_cost(Lw) + skill_cost(Lp) + skill_cost(Lc)
    if cost > S:
        continue

    Xp = 10 + 3*Lp
    Xg = (30 + 5*Lg) * Xp / 10
    Xw = (30 + 10*Lw) * Xp / 10
    Xc = current_companies + Lc if current_companies > 0 else base_companies + Lc  # toplam şirket

    Z_net = z * (1 - tax_rate/100)  # maaş vergisi uygulanıyor

    Z_total = 2.4*Q*Xg + 2.4*Z_net*Xw + K*Xc

    if Z_total > best_Z:
        best_Z = Z_total
        best_combination = (Lg, Lw, Lp, Lc)

# ---------------- Sonuç ----------------
if best_combination:
    print("\nEn iyi kombinasyon:")
    print("Lg (Entrepreneurship):", best_combination[0])
    print("Lw (Energy):", best_combination[1])
    print("Lp (Production):", best_combination[2])
    print("Lc (Company Limit):", best_combination[3])
    print("Toplam şirket:", current_companies + best_combination[3] if current_companies > 0 else base_companies + best_combination[3])
    print("Max Z (Günlük Max Kazanç):", round(best_Z, 2))
else:
    print("Geçerli bir kombinasyon bulunamadı!")
