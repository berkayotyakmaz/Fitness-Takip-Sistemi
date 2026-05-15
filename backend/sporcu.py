"""
Sporcu sınıfı
─────────────────────────────────────────────────────────
Ödev spec'ine göre temel attribute'lar: sporcu_id, ad, kilo, boy
Ek alanlar: dogum_yili (yaş hesabı için), cinsiyet (BMR formülü),
hedef_kilo, kayit_tarihi.

Metod: ilerleme_kaydet() — ölçüm anına ait kilo + tarih döndürür,
veri yöneticisi bu kaydı saklar.
"""

from datetime import date, datetime
from typing import Optional


class Sporcu:
    """Bir fitness kullanıcısı."""

    def __init__(
        self,
        sporcu_id: int,
        ad: str,
        kilo: float,
        boy: float,
        dogum_yili: int = 2000,
        cinsiyet: str = "erkek",
        hedef_kilo: Optional[float] = None,
        kayit_tarihi: Optional[str] = None,
    ):
        self.sporcu_id = sporcu_id
        self.ad = ad
        self.kilo = float(kilo)        # kg
        self.boy = float(boy)          # cm
        self.dogum_yili = int(dogum_yili)
        self.cinsiyet = cinsiyet       # "erkek" / "kadin"
        self.hedef_kilo = float(hedef_kilo) if hedef_kilo is not None else None
        self.kayit_tarihi = kayit_tarihi or date.today().isoformat()

    # ─── Hesaplanan özellikler ────────────────────────────
    @property
    def yas(self) -> int:
        return date.today().year - self.dogum_yili

    @property
    def vki(self) -> float:
        """Vücut Kitle İndeksi (BMI)."""
        m = self.boy / 100
        if m <= 0:
            return 0.0
        return round(self.kilo / (m * m), 1)

    @property
    def vki_kategori(self) -> str:
        v = self.vki
        if v == 0:
            return "—"
        if v < 18.5:
            return "Zayıf"
        if v < 25:
            return "Normal"
        if v < 30:
            return "Fazla Kilolu"
        return "Obez"

    @property
    def bmr(self) -> int:
        """Bazal Metabolizma Hızı — Mifflin-St Jeor formülü (kcal/gün)."""
        if self.cinsiyet == "erkek":
            v = 10 * self.kilo + 6.25 * self.boy - 5 * self.yas + 5
        else:
            v = 10 * self.kilo + 6.25 * self.boy - 5 * self.yas - 161
        return int(round(v))

    # ─── Metod: spec'te istenen ───────────────────────────
    def ilerleme_kaydet(self, yeni_kilo: float, not_metni: str = "") -> dict:
        """
        Yeni bir ölçüm kaydı üretir. Veri yöneticisi bunu
        takip listesine ekler ve sporcunun güncel kilosunu günceller.
        """
        yeni_kilo = float(yeni_kilo)
        kayit = {
            "sporcu_id": self.sporcu_id,
            "tarih": date.today().isoformat(),
            "olculen_kilo": yeni_kilo,
            "onceki_kilo": self.kilo,
            "fark": round(yeni_kilo - self.kilo, 2),
            "not": not_metni,
            "olusturma": datetime.now().isoformat(timespec="seconds"),
        }
        # güncel kiloyu da güncelliyoruz
        self.kilo = yeni_kilo
        return kayit

    # ─── Serileştirme ─────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "sporcu_id": self.sporcu_id,
            "ad": self.ad,
            "kilo": self.kilo,
            "boy": self.boy,
            "dogum_yili": self.dogum_yili,
            "cinsiyet": self.cinsiyet,
            "hedef_kilo": self.hedef_kilo,
            "kayit_tarihi": self.kayit_tarihi,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Sporcu":
        return cls(
            sporcu_id=d["sporcu_id"],
            ad=d["ad"],
            kilo=d["kilo"],
            boy=d["boy"],
            dogum_yili=d.get("dogum_yili", 2000),
            cinsiyet=d.get("cinsiyet", "erkek"),
            hedef_kilo=d.get("hedef_kilo"),
            kayit_tarihi=d.get("kayit_tarihi"),
        )

    def __repr__(self):
        return f"<Sporcu #{self.sporcu_id} {self.ad} {self.kilo}kg/{self.boy}cm>"
