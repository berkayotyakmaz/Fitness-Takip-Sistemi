"""
models.py
---------
Online Kurs Platformu - Veri Modelleri
Sınıflar: Egitmen, Ogrenci, Kurs
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Egitmen:
    """Eğitmen sınıfı"""
    ad: str
    uzmanlik: str

    def __str__(self) -> str:
        return f"{self.ad} ({self.uzmanlik})"

    def to_dict(self) -> dict:
        return {"ad": self.ad, "uzmanlik": self.uzmanlik}

    @staticmethod
    def from_dict(d: dict) -> "Egitmen":
        return Egitmen(ad=d["ad"], uzmanlik=d["uzmanlik"])


@dataclass
class Ogrenci:
    """Öğrenci sınıfı"""
    ogrenci_id: int
    ad: str
    email: str
    kayitli_kurslar: List[int] = field(default_factory=list)  # kurs_id listesi

    def kurs_listesi(self, tum_kurslar: List["Kurs"]) -> List["Kurs"]:
        """Öğrencinin kayıtlı olduğu kursları döndürür"""
        return [k for k in tum_kurslar if k.kurs_id in self.kayitli_kurslar]

    def __str__(self) -> str:
        return f"#{self.ogrenci_id} {self.ad}"

    def to_dict(self) -> dict:
        return {
            "ogrenci_id": self.ogrenci_id,
            "ad": self.ad,
            "email": self.email,
            "kayitli_kurslar": self.kayitli_kurslar,
        }

    @staticmethod
    def from_dict(d: dict) -> "Ogrenci":
        return Ogrenci(
            ogrenci_id=d["ogrenci_id"],
            ad=d["ad"],
            email=d["email"],
            kayitli_kurslar=d.get("kayitli_kurslar", []),
        )


@dataclass
class Kurs:
    """Kurs sınıfı"""
    kurs_id: int
    kurs_adi: str
    egitmen: Egitmen
    kontenjan: int
    kayitli_ogrenciler: List[int] = field(default_factory=list)  # ogrenci_id listesi

    def ogrenci_kaydet(self, ogrenci: Ogrenci) -> tuple[bool, str]:
        """Kursa öğrenci kaydı yapar. (basarili, mesaj) döndürür."""
        if ogrenci.ogrenci_id in self.kayitli_ogrenciler:
            return False, f"{ogrenci.ad} zaten bu kursa kayıtlı."
        if len(self.kayitli_ogrenciler) >= self.kontenjan:
            return False, f"Kontenjan dolu! ({self.kontenjan} kişi)"
        self.kayitli_ogrenciler.append(ogrenci.ogrenci_id)
        if self.kurs_id not in ogrenci.kayitli_kurslar:
            ogrenci.kayitli_kurslar.append(self.kurs_id)
        return True, f"{ogrenci.ad} kursa başarıyla kaydedildi."

    def ogrenci_cikar(self, ogrenci: Ogrenci) -> tuple[bool, str]:
        """Kurstan öğrenci kaydını siler"""
        if ogrenci.ogrenci_id not in self.kayitli_ogrenciler:
            return False, "Öğrenci bu kursa kayıtlı değil."
        self.kayitli_ogrenciler.remove(ogrenci.ogrenci_id)
        if self.kurs_id in ogrenci.kayitli_kurslar:
            ogrenci.kayitli_kurslar.remove(self.kurs_id)
        return True, "Kayıt iptal edildi."

    def doluluk_yuzdesi(self) -> float:
        if self.kontenjan == 0:
            return 0.0
        return (len(self.kayitli_ogrenciler) / self.kontenjan) * 100

    def bos_kontenjan(self) -> int:
        return self.kontenjan - len(self.kayitli_ogrenciler)

    def to_dict(self) -> dict:
        return {
            "kurs_id": self.kurs_id,
            "kurs_adi": self.kurs_adi,
            "egitmen": self.egitmen.to_dict(),
            "kontenjan": self.kontenjan,
            "kayitli_ogrenciler": self.kayitli_ogrenciler,
        }

    @staticmethod
    def from_dict(d: dict) -> "Kurs":
        return Kurs(
            kurs_id=d["kurs_id"],
            kurs_adi=d["kurs_adi"],
            egitmen=Egitmen.from_dict(d["egitmen"]),
            kontenjan=d["kontenjan"],
            kayitli_ogrenciler=d.get("kayitli_ogrenciler", []),
        )
