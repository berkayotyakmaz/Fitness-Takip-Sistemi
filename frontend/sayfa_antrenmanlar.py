"""Antrenmanlar sayfası — tüm geçmiş, filtreleme, silme."""

from datetime import date
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QAbstractItemView, QMessageBox, QGridLayout
)

from .tema import C, F_DISPLAY, F_MONO, F_SANS
from .bilesenler import (
    SectionHeader, LimeButton, GhostButton, HBar, Rozet, SmallMetric
)


class AntrenmanlarSayfasi(QWidget):
    antrenman_eklendi = pyqtSignal()
    antrenman_silindi = pyqtSignal()

    def __init__(self, vy, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.sporcu = None
        self._build()

    def _build(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(40, 32, 40, 32)
        ana.setSpacing(24)

        # ─── Başlık ──────────────────────────────────────
        ust = QHBoxLayout()
        sol = QVBoxLayout()
        sol.setSpacing(2)
        kt = QLabel("02 / ANTRENMANLAR")
        kt.setStyleSheet(
            f"color: {C['ink_mute']}; "
            f"font-family: '{F_MONO}'; font-size: 10px; letter-spacing: 3px;"
        )
        sol.addWidget(kt)
        bs = QLabel("WORKOUTS")
        bs.setStyleSheet(
            f"color: {C['ink']}; font-family: '{F_DISPLAY}'; "
            f"font-size: 56px; font-weight: 900; line-height: 1;"
        )
        sol.addWidget(bs)
        ust.addLayout(sol)
        ust.addStretch()
        self.btn_ekle = LimeButton("+ Antrenman Ekle")
        self.btn_ekle.clicked.connect(self._ekle)
        ust.addWidget(self.btn_ekle)
        ana.addLayout(ust)
        ana.addWidget(HBar(C['ink'], 2))

        # ─── Özet metrikler ──────────────────────────────
        ozet_panel = QFrame()
        ozet_panel.setStyleSheet(
            f"background: {C['panel']}; border: 1.5px solid {C['ink']};"
        )
        oz_lay = QHBoxLayout(ozet_panel)
        oz_lay.setContentsMargins(28, 20, 28, 20)
        oz_lay.setSpacing(40)

        self.ozet_toplam = SmallMetric("Toplam", "0", "kayıt")
        oz_lay.addWidget(self.ozet_toplam)
        oz_lay.addWidget(self._sep())
        self.ozet_sure = SmallMetric("Süre", "0", "dakika")
        oz_lay.addWidget(self.ozet_sure)
        oz_lay.addWidget(self._sep())
        self.ozet_kalori = SmallMetric("Kalori", "0", "kcal")
        oz_lay.addWidget(self.ozet_kalori)
        oz_lay.addWidget(self._sep())
        self.ozet_favori = SmallMetric("Favori", "—", "tür")
        oz_lay.addWidget(self.ozet_favori)
        oz_lay.addStretch()

        # filtre
        f_lay = QVBoxLayout()
        f_lay.setSpacing(2)
        f_lbl = QLabel("FİLTRE")
        f_lbl.setStyleSheet(
            f"color: {C['ink_mute']}; font-family: '{F_MONO}'; "
            f"font-size: 9px; letter-spacing: 2px;"
        )
        f_lay.addWidget(f_lbl)
        self.filtre = QComboBox()
        self.filtre.setFixedWidth(180)
        self.filtre.addItem("Tüm türler", "")
        self.filtre.currentIndexChanged.connect(self._tablo_yenile)
        f_lay.addWidget(self.filtre)
        oz_lay.addLayout(f_lay)
        ana.addWidget(ozet_panel)

        # ─── Tablo ───────────────────────────────────────
        ana.addWidget(SectionHeader("Geçmiş", "Tüm Kayıtlar"))
        self.tablo = QTableWidget(0, 6)
        self.tablo.setHorizontalHeaderLabels([
            "TARİH", "TÜR", "YOĞUNLUK", "SÜRE", "KALORİ", ""
        ])
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tablo.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tablo.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tablo.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tablo.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.tablo.setShowGrid(False)
        self.tablo.setMinimumHeight(360)
        ana.addWidget(self.tablo, 1)

    def _sep(self):
        f = QFrame(); f.setFixedWidth(1)
        f.setStyleSheet(f"background: {C['border_soft']};")
        return f

    def sporcu_ayarla(self, sporcu):
        self.sporcu = sporcu
        # filtre seçeneklerini güncelle
        self.filtre.blockSignals(True)
        mevcut = self.filtre.currentData()
        self.filtre.clear()
        self.filtre.addItem("Tüm türler", "")
        if sporcu:
            turler = sorted(set(
                a.tur for a in self.vy.antrenmanlar
                if a.sporcu_id == sporcu.sporcu_id
            ))
            for t in turler:
                self.filtre.addItem(t, t)
        idx = self.filtre.findData(mevcut)
        if idx >= 0:
            self.filtre.setCurrentIndex(idx)
        self.filtre.blockSignals(False)
        self.yenile()

    def yenile(self):
        self._tablo_yenile()
        self._ozet_yenile()

    def _ozet_yenile(self):
        if not self.sporcu:
            return
        antrenmanlar = self.vy.sporcunun_antrenmanlari(self.sporcu.sporcu_id)
        self.ozet_toplam.degeri_guncelle(str(len(antrenmanlar)))
        toplam_sure = sum(a.sure for a in antrenmanlar)
        self.ozet_sure.degeri_guncelle(str(toplam_sure))
        toplam_kalori = sum(a.yakilan_kalori(self.sporcu.kilo) for a in antrenmanlar)
        self.ozet_kalori.degeri_guncelle(str(toplam_kalori))

        # en sık tür
        if antrenmanlar:
            from collections import Counter
            sayac = Counter(a.tur for a in antrenmanlar)
            favori = sayac.most_common(1)[0][0]
            self.ozet_favori.degeri_guncelle(favori)
        else:
            self.ozet_favori.degeri_guncelle("—")

    def _tablo_yenile(self):
        if not self.sporcu:
            self.tablo.setRowCount(0)
            return
        f = self.filtre.currentData() or ""
        antrenmanlar = self.vy.sporcunun_antrenmanlari(self.sporcu.sporcu_id)
        if f:
            antrenmanlar = [a for a in antrenmanlar if a.tur == f]

        self.tablo.setRowCount(len(antrenmanlar))
        for i, a in enumerate(antrenmanlar):
            tar = date.fromisoformat(a.tarih).strftime("%d.%m.%Y")
            self.tablo.setItem(i, 0, self._cell(tar, mono=True))
            self.tablo.setItem(i, 1, self._cell(a.tur, bold=True))

            # yoğunluk rozeti
            yog_var = {"dusuk": "soft", "orta": "outline", "yuksek": "lime"}
            roz = Rozet(a.yogunluk_etiket, yog_var[a.yogunluk])
            kapsayici = QWidget()
            kl = QHBoxLayout(kapsayici)
            kl.setContentsMargins(8, 4, 8, 4)
            kl.addWidget(roz)
            kl.addStretch()
            self.tablo.setCellWidget(i, 2, kapsayici)

            self.tablo.setItem(i, 3, self._cell(f"{a.sure} dk", mono=True, align=Qt.AlignRight))
            kcal = a.yakilan_kalori(self.sporcu.kilo)
            self.tablo.setItem(i, 4, self._cell(f"{kcal} kcal", display=True, align=Qt.AlignRight))

            # sil butonu
            sil_btn = GhostButton("Sil", danger=True)
            sil_btn.setFixedWidth(70)
            sil_btn.clicked.connect(lambda _, aid=a.antrenman_id: self._sil(aid))
            kapsayici_btn = QWidget()
            kbl = QHBoxLayout(kapsayici_btn)
            kbl.setContentsMargins(8, 4, 8, 4)
            kbl.addWidget(sil_btn)
            self.tablo.setCellWidget(i, 5, kapsayici_btn)

            self.tablo.setRowHeight(i, 52)

    def _cell(self, text, mono=False, bold=False, display=False, align=Qt.AlignLeft):
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
        if bold:
            f.setBold(True)
        item.setFont(f)
        return item

    def _ekle(self):
        from .diyaloglar import AntrenmanDiyalog
        if not self.sporcu:
            return
        dlg = AntrenmanDiyalog(self, self.sporcu.kilo)
        if dlg.exec_() and dlg.sonuc:
            self.vy.antrenman_ekle(self.sporcu.sporcu_id, **dlg.sonuc)
            self.antrenman_eklendi.emit()
            self.sporcu_ayarla(self.sporcu)

    def _sil(self, antrenman_id):
        cevap = QMessageBox.question(
            self, "Antrenmanı sil",
            "Bu antrenman kaydı silinsin mi?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if cevap == QMessageBox.Yes:
            self.vy.antrenman_sil(antrenman_id)
            self.antrenman_silindi.emit()
            self.sporcu_ayarla(self.sporcu)
