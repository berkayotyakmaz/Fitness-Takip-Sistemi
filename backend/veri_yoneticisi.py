"""
VeriYoneticisi
─────────────────────────────────────────────────────────
Tüm verileri data/ klasöründeki JSON dosyalarında tutar.
GUI yalnızca bu sınıfla konuşur — sınıflar arası
referansları (sporcu_id) burada çözer.
"""

import json
import os
from datetime import date, datetime, timedelta
from typing import List, Optional

from .sporcu import Sporcu
from .antrenman import Antrenman
from .takip import Takip, OlcumKaydi


class VeriYoneticisi:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

        self.sporcular: List[Sporcu] = []
        self.antrenmanlar: List[Antrenman] = []
        self.takipler: List[Takip] = []
        self.olcumler: List[OlcumKaydi] = []

        self._load()

    # ─── Dosya yolları ────────────────────────────────────
    def _path(self, name: str) -> str:
        return os.path.join(self.data_dir, name)

    # ─── Yükleme / Kayıt ──────────────────────────────────
    def _load(self):
        try:
            with open(self._path("sporcular.json"), encoding="utf-8") as f:
                self.sporcular = [Sporcu.from_dict(d) for d in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            self.sporcular = []

        try:
            with open(self._path("antrenmanlar.json"), encoding="utf-8") as f:
                self.antrenmanlar = [Antrenman.from_dict(d) for d in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            self.antrenmanlar = []

        try:
            with open(self._path("takipler.json"), encoding="utf-8") as f:
                self.takipler = [Takip.from_dict(d) for d in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            self.takipler = []

        try:
            with open(self._path("olcumler.json"), encoding="utf-8") as f:
                self.olcumler = [OlcumKaydi.from_dict(d) for d in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            self.olcumler = []

    def kaydet(self):
        with open(self._path("sporcular.json"), "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.sporcular], f, ensure_ascii=False, indent=2)
        with open(self._path("antrenmanlar.json"), "w", encoding="utf-8") as f:
            json.dump([a.to_dict() for a in self.antrenmanlar], f, ensure_ascii=False, indent=2)
        with open(self._path("takipler.json"), "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.takipler], f, ensure_ascii=False, indent=2)
        with open(self._path("olcumler.json"), "w", encoding="utf-8") as f:
            json.dump([o.to_dict() for o in self.olcumler], f, ensure_ascii=False, indent=2)

    # ─── ID üretimi ───────────────────────────────────────
    def _yeni_id(self, items, attr: str) -> int:
        if not items:
            return 1
        return max(getattr(x, attr) for x in items) + 1

    # ─── SPORCU CRUD ──────────────────────────────────────
    def sporcu_ekle(self, ad: str, kilo: float, boy: float,
                    dogum_yili: int = 2000, cinsiyet: str = "erkek",
                    hedef_kilo: Optional[float] = None) -> Sporcu:
        s = Sporcu(
            sporcu_id=self._yeni_id(self.sporcular, "sporcu_id"),
            ad=ad, kilo=kilo, boy=boy,
            dogum_yili=dogum_yili, cinsiyet=cinsiyet,
            hedef_kilo=hedef_kilo,
        )
        self.sporcular.append(s)
        self.kaydet()
        return s

    def sporcu_guncelle(self, sporcu_id: int, **alanlar):
        s = self.sporcu_bul(sporcu_id)
        if not s:
            return None
        for k, v in alanlar.items():
            if hasattr(s, k):
                setattr(s, k, v)
        self.kaydet()
        return s

    def sporcu_sil(self, sporcu_id: int):
        self.sporcular = [s for s in self.sporcular if s.sporcu_id != sporcu_id]
        self.antrenmanlar = [a for a in self.antrenmanlar if a.sporcu_id != sporcu_id]
        self.takipler = [t for t in self.takipler if t.sporcu_id != sporcu_id]
        self.olcumler = [o for o in self.olcumler if o.sporcu_id != sporcu_id]
        self.kaydet()

    def sporcu_bul(self, sporcu_id: int) -> Optional[Sporcu]:
        return next((s for s in self.sporcular if s.sporcu_id == sporcu_id), None)

    # ─── ANTRENMAN ────────────────────────────────────────
    def antrenman_ekle(self, sporcu_id: int, tur: str, sure: int,
                       yogunluk: str = "orta", not_metni: str = "",
                       tarih: Optional[str] = None) -> Antrenman:
        a = Antrenman(
            antrenman_id=self._yeni_id(self.antrenmanlar, "antrenman_id"),
            sporcu_id=sporcu_id, tur=tur, sure=sure,
            yogunluk=yogunluk, not_metni=not_metni, tarih=tarih,
        )
        self.antrenmanlar.append(a)
        # Ayrıca bu güne ait Takip kaydındaki yakilan_kalori'yi de güncelle
        sporcu = self.sporcu_bul(sporcu_id)
        if sporcu:
            self._takip_gunluk_yenile(sporcu_id, a.tarih)
        self.kaydet()
        return a

    def antrenman_sil(self, antrenman_id: int):
        a = next((x for x in self.antrenmanlar if x.antrenman_id == antrenman_id), None)
        if not a:
            return
        sporcu_id, tarih = a.sporcu_id, a.tarih
        self.antrenmanlar = [x for x in self.antrenmanlar if x.antrenman_id != antrenman_id]
        self._takip_gunluk_yenile(sporcu_id, tarih)
        self.kaydet()

    def sporcunun_antrenmanlari(self, sporcu_id: int) -> List[Antrenman]:
        return sorted(
            [a for a in self.antrenmanlar if a.sporcu_id == sporcu_id],
            key=lambda x: x.tarih, reverse=True
        )

    # ─── TAKİP ────────────────────────────────────────────
    def _takip_gunluk_yenile(self, sporcu_id: int, tarih: str):
        """O güne ait Takip kaydındaki yakılan kaloriyi antrenmanlardan yeniden hesapla."""
        sporcu = self.sporcu_bul(sporcu_id)
        if not sporcu:
            return
        gunluk_antrenmanlar = [
            a for a in self.antrenmanlar
            if a.sporcu_id == sporcu_id and a.tarih == tarih
        ]
        toplam_yakilan = sum(a.yakilan_kalori(sporcu.kilo) for a in gunluk_antrenmanlar)

        kayit = self._takip_bul(sporcu_id, tarih)
        if kayit:
            kayit.yakilan_kalori = toplam_yakilan
        else:
            yeni = Takip(
                takip_id=self._yeni_id(self.takipler, "takip_id"),
                sporcu_id=sporcu_id, tarih=tarih,
                yakilan_kalori=toplam_yakilan,
            )
            self.takipler.append(yeni)

    def _takip_bul(self, sporcu_id: int, tarih: str) -> Optional[Takip]:
        return next(
            (t for t in self.takipler
             if t.sporcu_id == sporcu_id and t.tarih == tarih),
            None
        )

    def takip_kaydet(self, sporcu_id: int, tarih: str,
                     alinan_kalori: int = 0, adim: int = 0,
                     su_litre: float = 0.0, uyku_saat: float = 0.0,
                     not_metni: str = "", hedef_kalori: int = 0) -> Takip:
        kayit = self._takip_bul(sporcu_id, tarih)
        if not kayit:
            kayit = Takip(
                takip_id=self._yeni_id(self.takipler, "takip_id"),
                sporcu_id=sporcu_id, tarih=tarih,
            )
            self.takipler.append(kayit)
        kayit.alinan_kalori = int(alinan_kalori)
        kayit.adim = int(adim)
        kayit.su_litre = float(su_litre)
        kayit.uyku_saat = float(uyku_saat)
        kayit.not_metni = not_metni
        kayit.kalori = int(hedef_kalori)
        # yakılan kaloriyi yenile
        self._takip_gunluk_yenile(sporcu_id, tarih)
        self.kaydet()
        return kayit

    def sporcunun_takipleri(self, sporcu_id: int) -> List[Takip]:
        return sorted(
            [t for t in self.takipler if t.sporcu_id == sporcu_id],
            key=lambda x: x.tarih, reverse=True
        )

    # ─── ÖLÇÜM (ilerleme_kaydet) ──────────────────────────
    def ilerleme_kaydet(self, sporcu_id: int, yeni_kilo: float,
                        not_metni: str = "") -> Optional[OlcumKaydi]:
        sporcu = self.sporcu_bul(sporcu_id)
        if not sporcu:
            return None
        kayit_dict = sporcu.ilerleme_kaydet(yeni_kilo, not_metni)
        olcum = OlcumKaydi(
            olcum_id=self._yeni_id(self.olcumler, "olcum_id"),
            sporcu_id=sporcu_id,
            tarih=kayit_dict["tarih"],
            olculen_kilo=kayit_dict["olculen_kilo"],
            onceki_kilo=kayit_dict["onceki_kilo"],
            not_metni=not_metni,
        )
        self.olcumler.append(olcum)
        self.kaydet()
        return olcum

    def sporcunun_olcumleri(self, sporcu_id: int) -> List[OlcumKaydi]:
        return sorted(
            [o for o in self.olcumler if o.sporcu_id == sporcu_id],
            key=lambda x: x.tarih
        )

    # ─── İSTATİSTİK ───────────────────────────────────────
    def haftalik_ozet(self, sporcu_id: int) -> dict:
        """Son 7 gündeki antrenman/kalori özeti."""
        bugun = date.today()
        yedi_gun_once = bugun - timedelta(days=6)
        antrenmanlar = [
            a for a in self.antrenmanlar
            if a.sporcu_id == sporcu_id
            and yedi_gun_once.isoformat() <= a.tarih <= bugun.isoformat()
        ]
        sporcu = self.sporcu_bul(sporcu_id)
        kilo = sporcu.kilo if sporcu else 70
        toplam_kalori = sum(a.yakilan_kalori(kilo) for a in antrenmanlar)
        toplam_sure = sum(a.sure for a in antrenmanlar)

        # Günlük kalori dağılımı (grafik için)
        gunluk = {}
        for i in range(7):
            g = (yedi_gun_once + timedelta(days=i)).isoformat()
            gunluk[g] = 0
        for a in antrenmanlar:
            if a.tarih in gunluk:
                gunluk[a.tarih] += a.yakilan_kalori(kilo)

        return {
            "antrenman_sayisi": len(antrenmanlar),
            "toplam_kalori": toplam_kalori,
            "toplam_sure": toplam_sure,
            "gunluk_dagilim": gunluk,
        }
