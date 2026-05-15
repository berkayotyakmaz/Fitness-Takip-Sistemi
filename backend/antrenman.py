"""
Antrenman sınıfı
─────────────────────────────────────────────────────────
Spec: antrenman_id, tur (tür), sure
Genişletmeler:
- yogunluk: "dusuk" / "orta" / "yuksek"
- not: serbest açıklama

MET değerleri (Compendium of Physical Activities) ile
yakılan_kalori(sporcu_kilo) hesaplanır:
   kcal = MET * 3.5 * kg / 200 * dakika
"""

from datetime import datetime
from typing import Optional


# Aktivite türü → orta yoğunlukta MET değeri
MET_TABLOSU = {
    "Koşu":         9.8,
    "Yürüyüş":      3.8,
    "Bisiklet":     7.5,
    "Yüzme":        8.0,
    "Ağırlık":      6.0,
    "HIIT":        10.0,
    "Yoga":         3.0,
    "Pilates":      4.0,
    "Futbol":       8.5,
    "Basketbol":    7.5,
    "İp Atlama":   12.0,
    "Kardio":       7.0,
}

# Yoğunluk çarpanı
YOGUNLUK_CARPAN = {
    "dusuk": 0.85,
    "orta":  1.00,
    "yuksek": 1.18,
}


class Antrenman:
    def __init__(
        self,
        antrenman_id: int,
        sporcu_id: int,
        tur: str,
        sure: int,                # dakika
        yogunluk: str = "orta",
        not_metni: str = "",
        tarih: Optional[str] = None,
        olusturma: Optional[str] = None,
    ):
        self.antrenman_id = antrenman_id
        self.sporcu_id = sporcu_id
        self.tur = tur
        self.sure = int(sure)
        self.yogunluk = yogunluk if yogunluk in YOGUNLUK_CARPAN else "orta"
        self.not_metni = not_metni
        self.tarih = tarih or datetime.now().date().isoformat()
        self.olusturma = olusturma or datetime.now().isoformat(timespec="seconds")

    # ─── Hesaplama ────────────────────────────────────────
    def yakilan_kalori(self, sporcu_kilo: float) -> int:
        """Sporcunun kilosuna göre tahmini yakılan kalori."""
        met = MET_TABLOSU.get(self.tur, 6.0)
        carpan = YOGUNLUK_CARPAN[self.yogunluk]
        kcal = met * carpan * 3.5 * sporcu_kilo / 200.0 * self.sure
        return int(round(kcal))

    @property
    def yogunluk_etiket(self) -> str:
        return {"dusuk": "Düşük", "orta": "Orta", "yuksek": "Yüksek"}[self.yogunluk]

    # ─── Serileştirme ─────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "antrenman_id": self.antrenman_id,
            "sporcu_id": self.sporcu_id,
            "tur": self.tur,
            "sure": self.sure,
            "yogunluk": self.yogunluk,
            "not_metni": self.not_metni,
            "tarih": self.tarih,
            "olusturma": self.olusturma,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Antrenman":
        return cls(
            antrenman_id=d["antrenman_id"],
            sporcu_id=d["sporcu_id"],
            tur=d["tur"],
            sure=d["sure"],
            yogunluk=d.get("yogunluk", "orta"),
            not_metni=d.get("not_metni", ""),
            tarih=d.get("tarih"),
            olusturma=d.get("olusturma"),
        )

    def __repr__(self):
        return f"<Antrenman #{self.antrenman_id} {self.tur} {self.sure}dk>"
