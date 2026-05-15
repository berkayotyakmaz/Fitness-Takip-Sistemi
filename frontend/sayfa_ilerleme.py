"""İlerleme sayfası — kilo grafiği + ölçüm geçmişi."""

from datetime import date
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)

from .tema import C, F_DISPLAY, F_MONO, F_SANS
from .bilesenler import (
    SectionHeader, LimeButton, HBar, SmallMetric, SparkLine
)


class IlerlemeSayfasi(QWidget):
    olcum_eklendi = pyqtSignal()

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
        sol = QVBoxLayout()
        sol.setSpacing(2)
        kt = QLabel("03 / İLERLEME")
        kt.setStyleSheet(
            f"color: {C['ink_mute']}; font-family: '{F_MONO}'; "
            f"font-size: 10px; letter-spacing: 3px;"
        )
        sol.addWidget(kt)
        bs = QLabel("PROGRESS")
        bs.setStyleSheet(
            f"color: {C['ink']}; font-family: '{F_DISPLAY}'; "
            f"font-size: 56px; font-weight: 900; line-height: 1;"
        )
        sol.addWidget(bs)
        ust.addLayout(sol)
        ust.addStretch()
        self.btn_olcum = LimeButton("+ Yeni Tartım")
        self.btn_olcum.clicked.connect(self._olcum_ekle)
        ust.addWidget(self.btn_olcum)
        ana.addLayout(ust)
        ana.addWidget(HBar(C['ink'], 2))

        # ─── Üst panel: Kilo özeti + grafik ──────────────
        ust_panel = QHBoxLayout()
        ust_panel.setSpacing(20)

        # Sol: kilo metrikleri
        sol_panel = QFrame()
        sol_panel.setFixedWidth(280)
        sol_panel.setStyleSheet(
            f"background: {C['ink']}; border: 1.5px solid {C['ink']};"
        )
        sl = QVBoxLayout(sol_panel)
        sl.setContentsMargins(24, 22, 24, 22)
        sl.setSpacing(16)

        kt2 = QLabel("KİLO")
        kt2.setStyleSheet(
            f"color: {C['ink_inv_mut']}; font-family: '{F_MONO}'; "
            f"font-size: 10px; letter-spacing: 3px;"
        )
        sl.addWidget(kt2)

        self.lbl_kilo = QLabel("—")
        self.lbl_kilo.setStyleSheet(
            f"color: {C['lime']}; font-family: '{F_DISPLAY}'; "
            f"font-size: 64px; font-weight: 900; line-height: 1;"
        )
        sl.addWidget(self.lbl_kilo)
        self.lbl_kilo_alt = QLabel("kg · şu anki")
        self.lbl_kilo_alt.setStyleSheet(
            f"color: {C['ink_inv_mut']}; font-family: '{F_MONO}'; "
            f"font-size: 11px; letter-spacing: 2px;"
        )
        sl.addWidget(self.lbl_kilo_alt)

        ay = QFrame(); ay.setFixedHeight(1); ay.setStyleSheet(f"background: {C['ink_inv_mut']};")
        sl.addWidget(ay)

        # alt metrikler
        self.met_hedef = SmallMetric("Hedef", "—", "kg", inverted=True)
        sl.addWidget(self.met_hedef)
        self.met_fark = SmallMetric("Hedefe Kalan", "—", "kg", inverted=True)
        sl.addWidget(self.met_fark)
        self.met_ilk = SmallMetric("İlk Ölçüm", "—", "kg", inverted=True)
        sl.addWidget(self.met_ilk)
        sl.addStretch()
        ust_panel.addWidget(sol_panel)

        # Sağ: spark line grafik
        graf_panel = QFrame()
        graf_panel.setStyleSheet(
            f"background: {C['panel']}; border: 1.5px solid {C['ink']};"
        )
        gl = QVBoxLayout(graf_panel)
        gl.setContentsMargins(20, 18, 20, 18)
        gl.setSpacing(12)
        gl.addWidget(SectionHeader("Trend", "Kilo Değişimi"))
        self.spark = SparkLine()
        self.spark.setMinimumHeight(180)
        gl.addWidget(self.spark, 1)

        # alt: VKİ + BMR
        alt_satir = QHBoxLayout()
        alt_satir.setSpacing(40)
        self.met_vki = SmallMetric("VKİ", "—", "")
        alt_satir.addWidget(self.met_vki)
        self.met_kategori = SmallMetric("Kategori", "—", "")
        alt_satir.addWidget(self.met_kategori)
        self.met_bmr = SmallMetric("BMR", "—", "kcal/gün")
        alt_satir.addWidget(self.met_bmr)
        alt_satir.addStretch()
        gl.addLayout(alt_satir)
        ust_panel.addWidget(graf_panel, 1)

        ana.addLayout(ust_panel)

        # ─── Ölçüm tablosu ───────────────────────────────
        ana.addWidget(SectionHeader("Geçmiş Ölçümler", "Tartım Kayıtları"))
        self.tablo = QTableWidget(0, 4)
        self.tablo.setHorizontalHeaderLabels(["TARİH", "ÖLÇÜM", "FARK", "NOT"])
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablo.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tablo.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tablo.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tablo.setShowGrid(False)
        self.tablo.setMinimumHeight(220)
        ana.addWidget(self.tablo, 1)

    def sporcu_ayarla(self, sporcu):
        self.sporcu = sporcu
        self.yenile()

    def yenile(self):
        if not self.sporcu:
            return
        s = self.sporcu
        self.lbl_kilo.setText(f"{s.kilo:g}")

        if s.hedef_kilo:
            self.met_hedef.degeri_guncelle(f"{s.hedef_kilo:g}")
            fark = round(s.kilo - s.hedef_kilo, 1)
            self.met_fark.degeri_guncelle(f"{fark:+g}")
        else:
            self.met_hedef.degeri_guncelle("—")
            self.met_fark.degeri_guncelle("—")

        # ilk ölçüm
        olcumler = self.vy.sporcunun_olcumleri(s.sporcu_id)
        if olcumler:
            ilk = olcumler[0]
            self.met_ilk.degeri_guncelle(f"{ilk.onceki_kilo:g}")
        else:
            self.met_ilk.degeri_guncelle(f"{s.kilo:g}")

        # VKİ + BMR
        self.met_vki.degeri_guncelle(f"{s.vki:g}")
        self.met_kategori.degeri_guncelle(s.vki_kategori)
        self.met_bmr.degeri_guncelle(str(s.bmr))

        # spark line: ölçümlerin olculen_kilo'su + güncel kilo (sonuncu)
        if olcumler:
            # zincir: ilk ölçümün onceki_kilo, ardından her ölçümün olculen_kilo
            kilolar = [olcumler[0].onceki_kilo] + [o.olculen_kilo for o in olcumler]
        else:
            kilolar = [s.kilo]
        self.spark.veri_ayarla(kilolar)

        # ölçüm tablosu
        self.tablo.setRowCount(len(olcumler))
        for i, o in enumerate(reversed(olcumler)):  # en yeni üstte
            tar = date.fromisoformat(o.tarih).strftime("%d.%m.%Y")
            self.tablo.setItem(i, 0, self._cell(tar, mono=True))
            self.tablo.setItem(i, 1, self._cell(f"{o.olculen_kilo:g} kg", display=True))
            fark = o.fark
            fark_txt = f"{fark:+g} kg"
            it = self._cell(fark_txt, mono=True, align=Qt.AlignCenter)
            if fark < 0:
                it.setForeground(Qt.black)
                it.setBackground(Qt.GlobalColor.transparent)
            self.tablo.setItem(i, 2, it)
            self.tablo.setItem(i, 3, self._cell(o.not_metni or "—"))
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
