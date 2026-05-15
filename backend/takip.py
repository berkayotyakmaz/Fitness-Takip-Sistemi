"""
Takip sınıfı
─────────────────────────────────────────────────────────
Spec attribute: tarih, kalori
Genişletmeler:
- takip_id, sporcu_id (hangi sporcuya ait olduğu)
- alinan_kalori (gün içinde tüketilen)
- yakilan_kalori (antrenmanlardan)
- adim, su_litre, uyku_saat — günlük metrikler
- not_metni
"""

from datetime import date, datetime
from typing import Optional


class Takip:
    def __init__(
        self,
        takip_id: int,
        sporcu_id: int,
        tarih: Optional[str] = None,
        kalori: int = 0,                # spec: net/hedeflenen kalori
        alinan_kalori: int = 0,         # gün içi tüketim
        yakilan_kalori: int = 0,        # antrenmanlardan
        adim: int = 0,
        su_litre: float = 0.0,
        uyku_saat: float = 0.0,
        not_metni: str = "",
        olusturma: Optional[str] = None,
    ):
        self.takip_id = takip_id
        self.sporcu_id = sporcu_id
        self.tarih = tarih or date.today().isoformat()
        self.kalori = int(kalori)
        self.alinan_kalori = int(alinan_kalori)
        self.yakilan_kalori = int(yakilan_kalori)
        self.adim = int(adim)
        self.su_litre = float(su_litre)
        self.uyku_saat = float(uyku_saat)
        self.not_metni = not_metni
        self.olusturma = olusturma or datetime.now().isoformat(timespec="seconds")

    @property
    def net_kalori(self) -> int:
        """Alınan – Yakılan."""
        return self.alinan_kalori - self.yakilan_kalori

    def to_dict(self) -> dict:
        return {
            "takip_id": self.takip_id,
            "sporcu_id": self.sporcu_id,
            "tarih": self.tarih,
            "kalori": self.kalori,
            "alinan_kalori": self.alinan_kalori,
            "yakilan_kalori": self.yakilan_kalori,
            "adim": self.adim,
            "su_litre": self.su_litre,
            "uyku_saat": self.uyku_saat,
            "not_metni": self.not_metni,
            "olusturma": self.olusturma,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Takip":
        return cls(
            takip_id=d["takip_id"],
            sporcu_id=d["sporcu_id"],
            tarih=d.get("tarih"),
            kalori=d.get("kalori", 0),
            alinan_kalori=d.get("alinan_kalori", 0),
            yakilan_kalori=d.get("yakilan_kalori", 0),
            adim=d.get("adim", 0),
            su_litre=d.get("su_litre", 0.0),
            uyku_saat=d.get("uyku_saat", 0.0),
            not_metni=d.get("not_metni", ""),
            olusturma=d.get("olusturma"),
        )

    def __repr__(self):
        return f"<Takip #{self.takip_id} {self.tarih} {self.alinan_kalori}kcal>"


class OlcumKaydi:
    """ilerleme_kaydet() metodu tarafından üretilen kilo ölçüm kaydı."""

    def __init__(
        self,
        olcum_id: int,
        sporcu_id: int,
        tarih: str,
        olculen_kilo: float,
        onceki_kilo: float,
        not_metni: str = "",
        olusturma: Optional[str] = None,
    ):
        self.olcum_id = olcum_id
        self.sporcu_id = sporcu_id
        self.tarih = tarih
        self.olculen_kilo = float(olculen_kilo)
        self.onceki_kilo = float(onceki_kilo)
        self.not_metni = not_metni
        self.olusturma = olusturma or datetime.now().isoformat(timespec="seconds")

    @property
    def fark(self) -> float:
        return round(self.olculen_kilo - self.onceki_kilo, 2)

    def to_dict(self) -> dict:
        return {
            "olcum_id": self.olcum_id,
            "sporcu_id": self.sporcu_id,
            "tarih": self.tarih,
            "olculen_kilo": self.olculen_kilo,
            "onceki_kilo": self.onceki_kilo,
            "not_metni": self.not_metni,
            "olusturma": self.olusturma,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "OlcumKaydi":
        return cls(
            olcum_id=d["olcum_id"],
            sporcu_id=d["sporcu_id"],
            tarih=d["tarih"],
            olculen_kilo=d["olculen_kilo"],
            onceki_kilo=d["onceki_kilo"],
            not_metni=d.get("not_metni", ""),
            olusturma=d.get("olusturma"),
        )

    def __repr__(self):
        return f"<OlcumKaydi #{self.olcum_id} {self.tarih} {self.olculen_kilo}kg>"
