"""
Dashboard — sporcunun anlık durumu, haftalık özet, son antrenmanlar.
"""

from datetime import date, datetime, timedelta
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QFrame, QSizePolicy
)

from .tema import C, F_DISPLAY, F_MONO, F_SANS
from .bilesenler import (
    SectionHeader, BigMetric, SmallMetric, LimeButton, GhostButton,
    HBar, Rozet, BarChart, Ilerleme
)


GUN_KISA = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]


class DashboardSayfasi(QWidget):
    antrenman_eklendi = pyqtSignal()
    takip_eklendi = pyqtSignal()
    olcum_eklendi = pyqtSignal()

    def __init__(self, vy, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.sporcu = None
        self._build()

    def _build(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(40, 32, 40, 32)
        ana.setSpacing(28)

        # ─── Üst başlık ────────────────────────────────────
        ust = QHBoxLayout()
        ust.setSpacing(20)

        sol = QVBoxLayout()
        sol.setSpacing(2)
        kategori = QLabel("01 / DASHBOARD")
        kategori.setStyleSheet(
            f"color: {C['ink_mute']}; "
            f"font-family: '{F_MONO}'; font-size: 10px; "
            f"letter-spacing: 3px;"
        )
        sol.addWidget(kategori)
        self.baslik = QLabel("BUGÜN")
        self.baslik.setStyleSheet(
            f"color: {C['ink']}; "
            f"font-family: '{F_DISPLAY}'; "
            f"font-size: 56px; font-weight: 900; line-height: 1;"
        )
        sol.addWidget(self.baslik)
        self.alt_baslik = QLabel("")
        self.alt_baslik.setStyleSheet(
            f"color: {C['ink_mute']}; "
            f"font-family: '{F_MONO}'; font-size: 11px; "
            f"letter-spacing: 2px;"
        )
        sol.addWidget(self.alt_baslik)

        ust.addLayout(sol)
        ust.addStretch()

        # CTA butonları
        sag_btn = QVBoxLayout()
        sag_btn.setSpacing(8)
        self.btn_antrenman = LimeButton("+ Antrenman Ekle")
        self.btn_antrenman.clicked.connect(self._antrenman_ekle)
        sag_btn.addWidget(self.btn_antrenman)

        alt_btn = QHBoxLayout()
        alt_btn.setSpacing(8)
        self.btn_takip = GhostButton("Günü Kaydet")
        self.btn_takip.clicked.connect(self._takip_ekle)
        alt_btn.addWidget(self.btn_takip)
        self.btn_olcum = GhostButton("Tartım")
        self.btn_olcum.clicked.connect(self._olcum_ekle)
        alt_btn.addWidget(self.btn_olcum)
        sag_btn.addLayout(alt_btn)

        ust.addLayout(sag_btn)
        ana.addLayout(ust)
        ana.addWidget(HBar(C['ink'], 2))

        # ─── Üç büyük metrik ───────────────────────────────
        metrikler = QHBoxLayout()
        metrikler.setSpacing(0)

        self.metrik_kalori = self._buyuk_metrik_kart(
            "Yakılan", "0", "kcal bugün"
        )
        metrikler.addWidget(self.metrik_kalori)

        metrikler.addWidget(self._dikey_ayrac())

        self.metrik_sure = self._buyuk_metrik_kart(
            "Süre", "0", "dakika bugün"
        )
        metrikler.addWidget(self.metrik_sure)

        metrikler.addWidget(self._dikey_ayrac())

        self.metrik_antrenman = self._buyuk_metrik_kart(
            "Antrenman", "0", "kayıt bugün", vurgu=True
        )
        metrikler.addWidget(self.metrik_antrenman)

        cerceve = QFrame()
        cerceve.setLayout(metrikler)
        cerceve.setStyleSheet(f"""
            QFrame {{
                background: {C['panel']};
                border: 1.5px solid {C['ink']};
            }}
        """)
        ana.addWidget(cerceve)

        # ─── Alt grid: haftalık grafik + günlük takip + son antrenmanlar ──
        alt_grid = QGridLayout()
        alt_grid.setSpacing(20)
        alt_grid.setColumnStretch(0, 3)
        alt_grid.setColumnStretch(1, 2)

        # SOL ÜST: Haftalık kalori grafiği
        graf_panel = QFrame()
        graf_panel.setStyleSheet(f"""
            QFrame {{
                background: {C['panel']};
                border: 1.5px solid {C['ink']};
            }}
        """)
        graf_lay = QVBoxLayout(graf_panel)
        graf_lay.setContentsMargins(20, 18, 20, 18)
        graf_lay.setSpacing(12)
        graf_lay.addWidget(SectionHeader("Aktivite", "Son 7 Gün", "kcal"))
        self.haftalik_chart = BarChart()
        self.haftalik_chart.setMinimumHeight(180)
        graf_lay.addWidget(self.haftalik_chart)
        alt_grid.addWidget(graf_panel, 0, 0)

        # SAĞ ÜST: bugünün takipi
        takip_panel = QFrame()
        takip_panel.setStyleSheet(f"""
            QFrame {{
                background: {C['ink']};
                border: 1.5px solid {C['ink']};
            }}
        """)
        takip_lay = QVBoxLayout(takip_panel)
        takip_lay.setContentsMargins(20, 18, 20, 18)
        takip_lay.setSpacing(14)

        # başlık (inverted)
        kat = QLabel("BUGÜNÜN HEDEFLERİ")
        kat.setStyleSheet(
            f"color: {C['ink_inv_mut']}; "
            f"font-family: '{F_MONO}'; font-size: 10px; "
            f"letter-spacing: 3px;"
        )
        takip_lay.addWidget(kat)
        bsl = QLabel("PROGRESS")
        bsl.setStyleSheet(
            f"color: {C['lime']}; "
            f"font-family: '{F_DISPLAY}'; "
            f"font-size: 28px; font-weight: 900;"
        )
        takip_lay.addWidget(bsl)
        ayrac = QFrame()
        ayrac.setFixedHeight(1)
        ayrac.setStyleSheet(f"background: {C['ink_inv_mut']};")
        takip_lay.addWidget(ayrac)

        self.ilerleme_kalori = Ilerleme("Kalori", 0, 2000, " kcal", inverted=True)
        takip_lay.addWidget(self.ilerleme_kalori)
        self.ilerleme_adim = Ilerleme("Adım", 0, 10000, "", inverted=True)
        takip_lay.addWidget(self.ilerleme_adim)
        self.ilerleme_su = Ilerleme("Su", 0, 25, " dL", inverted=True)
        takip_lay.addWidget(self.ilerleme_su)
        takip_lay.addStretch()
        alt_grid.addWidget(takip_panel, 0, 1)

        # ALT (genişlik tüm grid): son antrenmanlar
        liste_panel = QFrame()
        liste_panel.setStyleSheet(f"""
            QFrame {{
                background: {C['panel']};
                border: 1.5px solid {C['ink']};
            }}
        """)
        liste_lay = QVBoxLayout(liste_panel)
        liste_lay.setContentsMargins(20, 18, 20, 18)
        liste_lay.setSpacing(8)
        liste_lay.addWidget(SectionHeader("Son Aktivite", "Yakın Antrenmanlar", ""))
        self.antrenman_liste = QVBoxLayout()
        self.antrenman_liste.setSpacing(0)
        liste_lay.addLayout(self.antrenman_liste)
        liste_lay.addStretch()
        alt_grid.addWidget(liste_panel, 1, 0, 1, 2)

        ana.addLayout(alt_grid)
        ana.addStretch()

    def _buyuk_metrik_kart(self, etiket, deger, birim, vurgu=False):
        kart = QFrame()
        if vurgu:
            kart.setStyleSheet(f"background: {C['lime']}; border: 0;")
        else:
            kart.setStyleSheet(f"background: {C['panel']}; border: 0;")
        l = QVBoxLayout(kart)
        l.setContentsMargins(28, 24, 28, 24)
        l.setSpacing(0)
        m = BigMetric(etiket, deger, birim, vurgu=vurgu)
        l.addWidget(m)
        kart.metric = m
        return kart

    def _dikey_ayrac(self):
        f = QFrame()
        f.setFixedWidth(1)
        f.setStyleSheet(f"background: {C['ink']};")
        return f

    # ─── Sporcu yüklendiğinde / değiştiğinde ──────────────
    def sporcu_ayarla(self, sporcu):
        self.sporcu = sporcu
        self.yenile()

    def yenile(self):
        if not self.sporcu:
            return
        bugun = date.today()
        bugun_iso = bugun.isoformat()
        AY_TR = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                 "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        GUN_TR = ["Pazartesi", "Salı", "Çarşamba", "Perşembe",
                  "Cuma", "Cumartesi", "Pazar"]
        self.alt_baslik.setText(
            f"{GUN_TR[bugun.weekday()]}, "
            f"{bugun.day} {AY_TR[bugun.month]} {bugun.year}"
            f"  ·  {self.sporcu.ad.upper()}"
        )

        # bugünün antrenmanları
        bugun_a = [a for a in self.vy.antrenmanlar
                   if a.sporcu_id == self.sporcu.sporcu_id and a.tarih == bugun_iso]
        toplam_kalori = sum(a.yakilan_kalori(self.sporcu.kilo) for a in bugun_a)
        toplam_sure = sum(a.sure for a in bugun_a)
        self.metrik_kalori.metric.degeri_guncelle(str(toplam_kalori))
        self.metrik_sure.metric.degeri_guncelle(str(toplam_sure))
        self.metrik_antrenman.metric.degeri_guncelle(str(len(bugun_a)))

        # haftalık grafik
        ozet = self.vy.haftalik_ozet(self.sporcu.sporcu_id)
        veri = []
        for tarih_iso, kcal in sorted(ozet["gunluk_dagilim"].items()):
            d = date.fromisoformat(tarih_iso)
            veri.append((GUN_KISA[d.weekday()], kcal))
        self.haftalik_chart.veri_ayarla(veri)

        # bugünün takip kaydı
        takip = self.vy._takip_bul(self.sporcu.sporcu_id, bugun_iso)
        if takip:
            hedef_k = takip.kalori or self.sporcu.bmr + 300
            self.ilerleme_kalori.guncelle(takip.alinan_kalori, hedef_k)
            self.ilerleme_adim.guncelle(takip.adim, 10000)
            # su: dL olarak gösterelim, hedef 25 dL = 2.5 L
            self.ilerleme_su.guncelle(int(takip.su_litre * 10), 25)
        else:
            self.ilerleme_kalori.guncelle(0, self.sporcu.bmr + 300)
            self.ilerleme_adim.guncelle(0, 10000)
            self.ilerleme_su.guncelle(0, 25)

        # son antrenmanlar listesi
        self._antrenman_liste_yenile()

    def _antrenman_liste_yenile(self):
        # eski itemleri temizle
        while self.antrenman_liste.count():
            item = self.antrenman_liste.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        antrenmanlar = self.vy.sporcunun_antrenmanlari(self.sporcu.sporcu_id)[:6]
        if not antrenmanlar:
            bos = QLabel("Henüz antrenman kaydı yok.\nİlk antrenmanını eklemek için yukarıdaki butonu kullan.")
            bos.setStyleSheet(
                f"color: {C['ink_mute']}; "
                f"font-family: '{F_MONO}'; font-size: 11px; "
                f"padding: 24px; letter-spacing: 1px; line-height: 1.5;"
            )
            bos.setAlignment(Qt.AlignCenter)
            self.antrenman_liste.addWidget(bos)
            return

        for i, a in enumerate(antrenmanlar):
            self.antrenman_liste.addWidget(self._antrenman_satiri(a, i == 0))

    def _antrenman_satiri(self, antrenman, ilk: bool):
        sat = QFrame()
        sat.setStyleSheet(f"""
            QFrame {{
                background: transparent;
                border: 0;
                border-bottom: 1px solid {C['border_soft']};
            }}
        """)
        l = QHBoxLayout(sat)
        l.setContentsMargins(0, 12, 0, 12)
        l.setSpacing(20)

        # tarih
        tar = date.fromisoformat(antrenman.tarih)
        tar_lbl = QLabel(tar.strftime("%d.%m"))
        tar_lbl.setFixedWidth(60)
        tar_lbl.setStyleSheet(
            f"color: {C['ink']}; "
            f"font-family: '{F_DISPLAY}'; "
            f"font-size: 18px; font-weight: 900;"
        )
        l.addWidget(tar_lbl)

        # tür
        tur_lbl = QLabel(antrenman.tur.upper())
        tur_lbl.setMinimumWidth(120)
        tur_lbl.setStyleSheet(
            f"color: {C['ink']}; font-family: '{F_SANS}'; "
            f"font-size: 13px; font-weight: bold; letter-spacing: 1px;"
        )
        l.addWidget(tur_lbl)

        # yoğunluk rozeti
        yog_var = {"dusuk": "soft", "orta": "outline", "yuksek": "lime"}
        l.addWidget(Rozet(antrenman.yogunluk_etiket, yog_var[antrenman.yogunluk]))

        l.addStretch()

        # süre
        sure_lbl = QLabel(f"{antrenman.sure} dk")
        sure_lbl.setStyleSheet(
            f"color: {C['ink_mute']}; "
            f"font-family: '{F_MONO}'; font-size: 12px;"
        )
        l.addWidget(sure_lbl)

        # kalori
        kcal = antrenman.yakilan_kalori(self.sporcu.kilo)
        kal_lbl = QLabel(f"{kcal} kcal")
        kal_lbl.setStyleSheet(
            f"color: {C['ink']}; "
            f"font-family: '{F_DISPLAY}'; "
            f"font-size: 16px; font-weight: 900;"
        )
        kal_lbl.setMinimumWidth(80)
        kal_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l.addWidget(kal_lbl)

        return sat

    # ─── Aksiyonlar ───────────────────────────────────────
    def _antrenman_ekle(self):
        from .diyaloglar import AntrenmanDiyalog
        if not self.sporcu:
            return
        dlg = AntrenmanDiyalog(self, self.sporcu.kilo)
        if dlg.exec_() and dlg.sonuc:
            self.vy.antrenman_ekle(self.sporcu.sporcu_id, **dlg.sonuc)
            self.antrenman_eklendi.emit()
            self.yenile()

    def _takip_ekle(self):
        from .diyaloglar import TakipDiyalog
        if not self.sporcu:
            return
        bugun = date.today().isoformat()
        mevcut = self.vy._takip_bul(self.sporcu.sporcu_id, bugun)
        dlg = TakipDiyalog(self, mevcut, hedef_kalori=self.sporcu.bmr + 300)
        if dlg.exec_() and dlg.sonuc:
            self.vy.takip_kaydet(self.sporcu.sporcu_id, **dlg.sonuc)
            self.takip_eklendi.emit()
            self.yenile()

    def _olcum_ekle(self):
        from .diyaloglar import IlerlemeDiyalog
        if not self.sporcu:
            return
        dlg = IlerlemeDiyalog(self, self.sporcu.kilo)
        if dlg.exec_() and dlg.sonuc:
            self.vy.ilerleme_kaydet(
                self.sporcu.sporcu_id,
                dlg.sonuc["yeni_kilo"],
                dlg.sonuc["not_metni"],
            )
            self.olcum_eklendi.emit()
            self.yenile()
