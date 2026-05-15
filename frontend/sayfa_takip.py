"""Takip sayfası — günlük takip kayıtları."""

from datetime import date
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)

from .tema import C, F_DISPLAY, F_MONO, F_SANS
from .bilesenler import (
    SectionHeader, LimeButton, GhostButton, HBar, SmallMetric, Rozet
)


class TakipSayfasi(QWidget):
    takip_eklendi = pyqtSignal()

    def __init__(self, vy, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.sporcu = None
        self._build()

    def _build(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(40, 32, 40, 32)
        ana.setSpacing(24)

        # Başlık
        ust = QHBoxLayout()
        sol = QVBoxLayout(); sol.setSpacing(2)
        kt = QLabel("04 / GÜNLÜK TAKİP")
        kt.setStyleSheet(
            f"color: {C['ink_mute']}; font-family: '{F_MONO}'; "
            f"font-size: 10px; letter-spacing: 3px;"
        )
        sol.addWidget(kt)
        bs = QLabel("DAILY LOG")
        bs.setStyleSheet(
            f"color: {C['ink']}; font-family: '{F_DISPLAY}'; "
            f"font-size: 56px; font-weight: 900; line-height: 1;"
        )
        sol.addWidget(bs)
        ust.addLayout(sol)
        ust.addStretch()
        self.btn_ekle = LimeButton("+ Günü Kaydet")
        self.btn_ekle.clicked.connect(self._ekle)
        ust.addWidget(self.btn_ekle)
        ana.addLayout(ust)
        ana.addWidget(HBar(C['ink'], 2))

        # Özet
        ozet = QFrame()
        ozet.setStyleSheet(
            f"background: {C['panel']}; border: 1.5px solid {C['ink']};"
        )
        ol = QHBoxLayout(ozet)
        ol.setContentsMargins(28, 20, 28, 20)
        ol.setSpacing(40)
        self.met_kayit = SmallMetric("Kayıt Sayısı", "0", "gün")
        ol.addWidget(self.met_kayit)
        ol.addWidget(self._sep())
        self.met_ort_kalori = SmallMetric("Ort. Alınan", "0", "kcal/gün")
        ol.addWidget(self.met_ort_kalori)
        ol.addWidget(self._sep())
        self.met_ort_adim = SmallMetric("Ort. Adım", "0", "adım/gün")
        ol.addWidget(self.met_ort_adim)
        ol.addWidget(self._sep())
        self.met_ort_uyku = SmallMetric("Ort. Uyku", "0", "saat/gece")
        ol.addWidget(self.met_ort_uyku)
        ol.addStretch()
        ana.addWidget(ozet)

        # Tablo
        ana.addWidget(SectionHeader("Günlük Kayıtlar", "Takip Geçmişi"))
        self.tablo = QTableWidget(0, 8)
        self.tablo.setHorizontalHeaderLabels([
            "TARİH", "DURUM", "ALINAN", "YAKILAN", "NET", "ADIM", "SU", "UYKU"
        ])
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tablo.horizontalHeader().setStretchLastSection(True)
        self.tablo.setShowGrid(False)
        self.tablo.setMinimumHeight(360)
        self.tablo.cellDoubleClicked.connect(self._satir_duzenle)
        ana.addWidget(self.tablo, 1)

        ipucu = QLabel("İpucu: Bir satıra çift tıklayarak günü düzenleyebilirsin.")
        ipucu.setStyleSheet(
            f"color: {C['ink_mute']}; font-family: '{F_MONO}'; "
            f"font-size: 10px; letter-spacing: 1.5px; padding-left: 4px;"
        )
        ana.addWidget(ipucu)

    def _sep(self):
        f = QFrame(); f.setFixedWidth(1)
        f.setStyleSheet(f"background: {C['border_soft']};")
        return f

    def sporcu_ayarla(self, sporcu):
        self.sporcu = sporcu
        self.yenile()

    def yenile(self):
        if not self.sporcu:
            self.tablo.setRowCount(0)
            return

        kayitlar = self.vy.sporcunun_takipleri(self.sporcu.sporcu_id)
        # Filtrele: anlamlı kayıt (alınan/adım/su/uyku verisi olan)
        kayitlar = [k for k in kayitlar
                    if k.alinan_kalori or k.adim or k.su_litre or k.uyku_saat]

        # Özet
        n = len(kayitlar)
        self.met_kayit.degeri_guncelle(str(n))
        if n:
            ort_kalori = sum(k.alinan_kalori for k in kayitlar) / n
            ort_adim = sum(k.adim for k in kayitlar) / n
            ort_uyku = sum(k.uyku_saat for k in kayitlar) / n
            self.met_ort_kalori.degeri_guncelle(str(int(round(ort_kalori))))
            self.met_ort_adim.degeri_guncelle(f"{int(round(ort_adim)):,}".replace(",", "."))
            self.met_ort_uyku.degeri_guncelle(f"{ort_uyku:.1f}")
        else:
            self.met_ort_kalori.degeri_guncelle("0")
            self.met_ort_adim.degeri_guncelle("0")
            self.met_ort_uyku.degeri_guncelle("0")

        # Tablo
        self.tablo.setRowCount(n)
        for i, k in enumerate(kayitlar):
            tar = date.fromisoformat(k.tarih).strftime("%d.%m.%Y")
            self.tablo.setItem(i, 0, self._cell(tar, mono=True))

            # Durum
            net = k.net_kalori
            hedef = k.kalori or (self.sporcu.bmr + 300)
            if k.alinan_kalori == 0:
                durum = "BOŞ"; var = "soft"
            elif k.alinan_kalori <= hedef * 1.05:
                durum = "HEDEFTE"; var = "lime"
            else:
                durum = "AŞIM"; var = "warn"
            roz = Rozet(durum, var)
            wrap = QWidget()
            wl = QHBoxLayout(wrap)
            wl.setContentsMargins(8, 4, 8, 4)
            wl.addWidget(roz); wl.addStretch()
            self.tablo.setCellWidget(i, 1, wrap)

            self.tablo.setItem(i, 2, self._cell(f"{k.alinan_kalori}", display=True, align=Qt.AlignRight))
            self.tablo.setItem(i, 3, self._cell(f"{k.yakilan_kalori}", mono=True, align=Qt.AlignRight))
            net_txt = f"{net:+}" if net != 0 else "0"
            self.tablo.setItem(i, 4, self._cell(net_txt, mono=True, align=Qt.AlignRight))
            self.tablo.setItem(i, 5, self._cell(f"{k.adim:,}".replace(",", "."), mono=True, align=Qt.AlignRight))
            self.tablo.setItem(i, 6, self._cell(f"{k.su_litre:.1f} L", mono=True, align=Qt.AlignRight))
            self.tablo.setItem(i, 7, self._cell(f"{k.uyku_saat:.1f} sa", mono=True, align=Qt.AlignRight))
            self.tablo.setRowHeight(i, 48)

    def _cell(self, text, mono=False, display=False, align=Qt.AlignLeft):
        item = QTableWidgetItem(text)
        item.setTextAlignment(align | Qt.AlignVCenter)
        f = item.font()
        if mono:
            f.setFamily(F_MONO)
        elif display:
            f.setFamily(F_DISPLAY)
            f.setBold(True)
            f.setPointSize(13)
        else:
            f.setFamily(F_SANS)
        item.setFont(f)
        return item

    def _ekle(self):
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

    def _satir_duzenle(self, row, _col):
        from .diyaloglar import TakipDiyalog
        if not self.sporcu:
            return
        kayitlar = self.vy.sporcunun_takipleri(self.sporcu.sporcu_id)
        kayitlar = [k for k in kayitlar
                    if k.alinan_kalori or k.adim or k.su_litre or k.uyku_saat]
        if row >= len(kayitlar):
            return
        kayit = kayitlar[row]
        dlg = TakipDiyalog(self, kayit, hedef_kalori=self.sporcu.bmr + 300)
        if dlg.exec_() and dlg.sonuc:
            self.vy.takip_kaydet(self.sporcu.sporcu_id, **dlg.sonuc)
            self.takip_eklendi.emit()
            self.yenile()
