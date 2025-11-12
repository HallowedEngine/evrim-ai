# -*- coding: utf-8 -*-
import random
import string
import sys

if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')

# === AYARLAR ===
hedef = "Merhaba, ben Grok'um!"
karakterler = string.ascii_letters + " ,.!?'" + "ğüşöçİĞÜŞÖÇ"
populasyon_boyutu = 200
mutasyon_orani = 0.12
nesil_sayisi = 3000
elit_sayisi = 30
# ===============

def rastgele_birey():
    return ''.join(random.choice(karakterler) for _ in range(len(hedef)))

# YENİ: GÜÇLÜ UYGUNLUK FONKSİYONU
def uygunluk(birey):
    if len(birey) != len(hedef):
        return -999
    
    skor = 0
    for i, (a, b) in enumerate(zip(birey, hedef)):
        if a == b:
            skor += 10  # DOĞRU YERDE = YÜKSEK PUAN
        elif a in hedef:
            skor += 1   # YANLIŞ YERDE = AZ PUAN
        # Boşluk ve noktalama için ekstra ödül
        if a == ' ' and b == ' ':
            skor += 3
        if a in ",!'" and b in ",!'":
            skor += 2
    return skor

def caprazlama(e1, e2):
    # Daha akıllı çaprazlama: Rastgele değil, blok halinde
    basla = random.randint(0, len(hedef)//3)
    bitir = random.randint(2*len(hedef)//3, len(hedef))
    cocuk = e1[:basla] + e2[basla:bitir] + e1[bitir:]
    return cocuk

def mutasyon(birey):
    b = list(birey)
    degisim_sayisi = max(1, int(mutasyon_orani * len(b)))
    for _ in range(degisim_sayisi):
        i = random.randint(0, len(b)-1)
        # Hedefteki harflerden birini seç (öğrenme!)
        if random.random() < 0.7 and hedef[i] in karakterler:
            b[i] = hedef[i]  # Hedefe yönlendir!
        else:
            b[i] = random.choice(karakterler)
    return ''.join(b)

# === EVRİM BAŞLASIN ===
pop = [rastgele_birey() for _ in range(populasyon_boyutu)]
print(f"Evrim V2 başlıyor! Hedef: \"{hedef}\"")

en_iyi_global = ""
en_skor_global = -1

for n in range(nesil_sayisi):
    skorlar = [(b, uygunluk(b)) for b in pop]
    skorlar.sort(key=lambda x: x[1], reverse=True)
    
    en_iyi = skorlar[0][0]
    en_skor = skorlar[0][1]
    
    if en_skor > en_skor_global:
        en_iyi_global = en_iyi
        en_skor_global = en_skor
        if en_iyi == hedef:
            print(f"\nBAŞARI! Nesil {n}: \"{en_iyi}\"")
            break
    
    if n % 200 == 0 or en_skor > 120:
        print(f"Nesil {n:4} | En iyi: \"{en_iyi}\" | Skor: {en_skor}")

    # Elitizm: En iyi 30 birey doğrudan geçer
    elit = [b for b, s in skorlar[:elit_sayisi]]
    
    # Yeni nesil
    yeni_pop = elit[:]  # Elitler korunur
    while len(yeni_pop) < populasyon_boyutu:
        e1, e2 = random.sample(elit, 2)  # Aynı birey olmasın
        cocuk = caprazlama(e1, e2)
        cocuk = mutasyon(cocuk)
        if len(cocuk) != len(hedef):
            cocuk = (cocuk + rastgele_birey(len(hedef))[:len(hedef)])[:len(hedef)]
        yeni_pop.append(cocuk)
    
    pop = yeni_pop

else:
    print(f"\nZaman doldu. En iyi: \"{en_iyi_global}\" (Skor: {en_skor_global})")