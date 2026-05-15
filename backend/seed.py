"""İlk açılışta demo veri yükle."""

from datetime import date, timedelta
from .veri_yoneticisi import VeriYoneticisi
from .antrenman import Antrenman
from .takip import Takip


def seed(vy: VeriYoneticisi):
    if vy.sporcular:
        return  # zaten veri var

    s1 = vy.sporcu_ekle("Beko Demir", kilo=78.0, boy=180,
                        dogum_yili=2002, cinsiyet="erkek", hedef_kilo=72.0)
    s2 = vy.sporcu_ekle("Elif Kaya", kilo=62.0, boy=168,
                        dogum_yili=2000, cinsiyet="kadin", hedef_kilo=58.0)
    s3 = vy.sporcu_ekle("Mert Yılmaz", kilo=85.0, boy=175,
                        dogum_yili=1998, cinsiyet="erkek", hedef_kilo=80.0)

    bugun = date.today()
    # Beko: son 7 günde çeşitli antrenmanlar
    plan = [
        (0, "Koşu", 35, "orta"),
        (1, "Ağırlık", 50, "yuksek"),
        (1, "Yürüyüş", 25, "dusuk"),
        (2, "HIIT", 20, "yuksek"),
        (3, "Bisiklet", 60, "orta"),
        (4, "Yüzme", 40, "orta"),
        (5, "Ağırlık", 55, "yuksek"),
        (6, "Yoga", 30, "dusuk"),
    ]
    for gun_geri, tur, sure, yog in plan:
        t = (bugun - timedelta(days=gun_geri)).isoformat()
        vy.antrenman_ekle(s1.sporcu_id, tur, sure, yog, tarih=t)

    # Elif: birkaç antrenman
    for i, (tur, sure, yog) in enumerate([
        ("Pilates", 45, "orta"),
        ("Koşu", 30, "orta"),
        ("Yoga", 40, "dusuk"),
    ]):
        t = (bugun - timedelta(days=i)).isoformat()
        vy.antrenman_ekle(s2.sporcu_id, tur, sure, yog, tarih=t)

    # Mert: birkaç antrenman
    for i, (tur, sure, yog) in enumerate([
        ("Basketbol", 60, "yuksek"),
        ("Ağırlık", 50, "orta"),
    ]):
        t = (bugun - timedelta(days=i*2)).isoformat()
        vy.antrenman_ekle(s3.sporcu_id, tur, sure, yog, tarih=t)

    # Beko için bugünün takip kaydı
    vy.takip_kaydet(
        s1.sporcu_id, bugun.isoformat(),
        alinan_kalori=2350, adim=8420, su_litre=2.4,
        uyku_saat=7.2, hedef_kalori=2500,
        not_metni="Bacak günü — squat PR'ı denedim."
    )
    # Beko için bir ölçüm kaydı (eski)
    s1.kilo = 79.5  # önceki kilo
    vy.ilerleme_kaydet(s1.sporcu_id, 78.0, "Haftalık tartım")
    # Elif takip
    vy.takip_kaydet(
        s2.sporcu_id, bugun.isoformat(),
        alinan_kalori=1680, adim=6200, su_litre=1.8,
        uyku_saat=6.5, hedef_kalori=1800,
    )
