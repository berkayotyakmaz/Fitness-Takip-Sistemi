"""
service.py
----------
Platform iş mantığı katmanı.
Kurs, öğrenci, eğitmen yönetimi ve JSON dosyasında kalıcılık.
"""

import json
import os
from typing import List, Optional
from .models import Kurs, Ogrenci, Egitmen


class PlatformService:
    """Online kurs platformunun servis katmanı"""

    def __init__(self, data_path: str = "data/platform.json"):
        self.data_path = data_path
        self.kurslar: List[Kurs] = []
        self.ogrenciler: List[Ogrenci] = []
        self._sonraki_kurs_id = 1
        self._sonraki_ogrenci_id = 1
        self.yukle()

    # ---------- Kalıcılık ----------
    def yukle(self) -> None:
        if not os.path.exists(self.data_path):
            self._ornek_veri_olustur()
            self.kaydet()
            return
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.kurslar = [Kurs.from_dict(k) for k in data.get("kurslar", [])]
            self.ogrenciler = [Ogrenci.from_dict(o) for o in data.get("ogrenciler", [])]
            self._sonraki_kurs_id = data.get("sonraki_kurs_id", 1)
            self._sonraki_ogrenci_id = data.get("sonraki_ogrenci_id", 1)
        except (json.JSONDecodeError, KeyError):
            self._ornek_veri_olustur()
            self.kaydet()

    def kaydet(self) -> None:
        os.makedirs(os.path.dirname(self.data_path) or ".", exist_ok=True)
        data = {
            "kurslar": [k.to_dict() for k in self.kurslar],
            "ogrenciler": [o.to_dict() for o in self.ogrenciler],
            "sonraki_kurs_id": self._sonraki_kurs_id,
            "sonraki_ogrenci_id": self._sonraki_ogrenci_id,
        }
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _ornek_veri_olustur(self) -> None:
        """İlk açılışta gösterim için örnek veri"""
        e1 = Egitmen("Dr. Ayşe Demir", "Yapay Zeka")
        e2 = Egitmen("Prof. Mehmet Kaya", "Veri Bilimi")
        e3 = Egitmen("Zeynep Yılmaz", "Web Geliştirme")
        e4 = Egitmen("Can Aksoy", "Siber Güvenlik")

        self.kurslar = [
            Kurs(1, "Derin Öğrenmeye Giriş", e1, 30),
            Kurs(2, "Python ile Veri Analizi", e2, 25),
            Kurs(3, "Modern React & TypeScript", e3, 40),
            Kurs(4, "Etik Hacking 101", e4, 20),
        ]
        self.ogrenciler = [
            Ogrenci(1, "Beko Yıldız", "beko@ornek.com"),
            Ogrenci(2, "Selin Arslan", "selin@ornek.com"),
            Ogrenci(3, "Emre Çelik", "emre@ornek.com"),
        ]
        self._sonraki_kurs_id = 5
        self._sonraki_ogrenci_id = 4

    # ---------- Kurs İşlemleri ----------
    def kurs_ekle(self, kurs_adi: str, egitmen_ad: str, uzmanlik: str,
                  kontenjan: int) -> Kurs:
        kurs = Kurs(
            kurs_id=self._sonraki_kurs_id,
            kurs_adi=kurs_adi,
            egitmen=Egitmen(egitmen_ad, uzmanlik),
            kontenjan=kontenjan,
        )
        self.kurslar.append(kurs)
        self._sonraki_kurs_id += 1
        self.kaydet()
        return kurs

    def kurs_sil(self, kurs_id: int) -> bool:
        kurs = self.kurs_bul(kurs_id)
        if not kurs:
            return False
        # Öğrencilerden de bu kursu sil
        for ogr_id in list(kurs.kayitli_ogrenciler):
            ogr = self.ogrenci_bul(ogr_id)
            if ogr and kurs_id in ogr.kayitli_kurslar:
                ogr.kayitli_kurslar.remove(kurs_id)
        self.kurslar.remove(kurs)
        self.kaydet()
        return True

    def kurs_bul(self, kurs_id: int) -> Optional[Kurs]:
        return next((k for k in self.kurslar if k.kurs_id == kurs_id), None)

    # ---------- Öğrenci İşlemleri ----------
    def ogrenci_ekle(self, ad: str, email: str) -> Ogrenci:
        ogr = Ogrenci(
            ogrenci_id=self._sonraki_ogrenci_id,
            ad=ad,
            email=email,
        )
        self.ogrenciler.append(ogr)
        self._sonraki_ogrenci_id += 1
        self.kaydet()
        return ogr

    def ogrenci_sil(self, ogrenci_id: int) -> bool:
        ogr = self.ogrenci_bul(ogrenci_id)
        if not ogr:
            return False
        # Kurslardan da bu öğrenciyi sil
        for kurs_id in list(ogr.kayitli_kurslar):
            kurs = self.kurs_bul(kurs_id)
            if kurs and ogrenci_id in kurs.kayitli_ogrenciler:
                kurs.kayitli_ogrenciler.remove(ogrenci_id)
        self.ogrenciler.remove(ogr)
        self.kaydet()
        return True

    def ogrenci_bul(self, ogrenci_id: int) -> Optional[Ogrenci]:
        return next((o for o in self.ogrenciler if o.ogrenci_id == ogrenci_id), None)

    # ---------- Kayıt İşlemleri ----------
    def kursa_kayit(self, kurs_id: int, ogrenci_id: int) -> tuple[bool, str]:
        kurs = self.kurs_bul(kurs_id)
        ogr = self.ogrenci_bul(ogrenci_id)
        if not kurs or not ogr:
            return False, "Kurs veya öğrenci bulunamadı."
        ok, msg = kurs.ogrenci_kaydet(ogr)
        if ok:
            self.kaydet()
        return ok, msg

    def kayit_iptal(self, kurs_id: int, ogrenci_id: int) -> tuple[bool, str]:
        kurs = self.kurs_bul(kurs_id)
        ogr = self.ogrenci_bul(ogrenci_id)
        if not kurs or not ogr:
            return False, "Kurs veya öğrenci bulunamadı."
        ok, msg = kurs.ogrenci_cikar(ogr)
        if ok:
            self.kaydet()
        return ok, msg

    # ---------- İstatistikler ----------
    def toplam_kayit_sayisi(self) -> int:
        return sum(len(k.kayitli_ogrenciler) for k in self.kurslar)

    def ortalama_doluluk(self) -> float:
        if not self.kurslar:
            return 0.0
        return sum(k.doluluk_yuzdesi() for k in self.kurslar) / len(self.kurslar)
