"""
Ana Pencere — sol siyah profil panel + sağ içerik alanı.
"""

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QStackedWidget, QPushButton, QComboBox, QMessageBox,
    QSpacerItem, QSizePolicy, QButtonGroup
)

from .tema import C, F_DISPLAY, F_MONO, F_SANS, app_qss
from .bilesenler import (
    NavItem, LimeButton, GhostButton, HBar, SmallMetric, Rozet
)
from .sayfa_dashboard import DashboardSayfasi
from .sayfa_antrenmanlar import AntrenmanlarSayfasi
from .sayfa_ilerleme import IlerlemeSayfasi
from .sayfa_takip import TakipSayfasi
from .diyaloglar import SporcuDiyalog


class AnaPencere(QMainWindow):
    def __init__(self, vy):
        super().__init__()
        self.vy = vy
        self.aktif_sporcu = None

        self.setWindowTitle("PULSE — Fitness Takip Sistemi")
        self.resize(1320, 820)
        self.setMinimumSize(1180, 720)
        self.setStyleSheet(app_qss())

        self._build()
        self._sporcular_yukle()

    def _build(self):
        kok = QWidget()
        kok.setObjectName("Root")
        self.setCentralWidget(kok)
        ana = QHBoxLayout(kok)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        # ─── SOL PANEL (siyah, sabit) ─────────────────────
        self._sol_panel_kur(ana)

        # ─── SAĞ İÇERİK ───────────────────────────────────
        self.icerik = QStackedWidget()
        self.icerik.setStyleSheet(f"background: {C['bg']};")
        ana.addWidget(self.icerik, 1)

        # sayfalar
        self.s_dashboard = DashboardSayfasi(self.vy)
        self.s_antrenmanlar = AntrenmanlarSayfasi(self.vy)
        self.s_ilerleme = IlerlemeSayfasi(self.vy)
        self.s_takip = TakipSayfasi(self.vy)

        for s in (self.s_dashboard, self.s_antrenmanlar,
                  self.s_ilerleme, self.s_takip):
            self.icerik.addWidget(s)

        # signal'lar — herhangi bir sayfada veri değişince diğerleri yenilenmeli
        for s in (self.s_dashboard, self.s_antrenmanlar,
                  self.s_ilerleme, self.s_takip):
            for sig_name in ("antrenman_eklendi", "antrenman_silindi",
                             "takip_eklendi", "olcum_eklendi"):
                sig = getattr(s, sig_name, None)
                if sig is not None:
                    sig.connect(self._tum_sayfalari_yenile)

        # nav default → dashboard
        self._sayfa_degistir(0)

    # ═══════════════════════════════════════════════════════
    #  SOL SİYAH PANEL
    # ═══════════════════════════════════════════════════════
    def _sol_panel_kur(self, parent_layout):
        panel = QFrame()
        panel.setFixedWidth(300)
        panel.setStyleSheet(f"""
            QFrame {{
                background: {C['ink']};
                border: 0;
                border-right: 1.5px solid {C['ink']};
            }}
            QLabel {{ color: {C['ink_inv']}; }}
        """)
        l = QVBoxLayout(panel)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(0)

        # ─── Üst: Logo + sporcu seçici ────────────────────
        ust = QWidget()
        ul = QVBoxLayout(ust)
        ul.setContentsMargins(24, 24, 24, 18)
        ul.setSpacing(14)

        # Logo: PULSE — kalın, lime accent çentik
        logo_row = QHBoxLayout()
        logo_row.setSpacing(0)
        logo_lbl = QLabel("PULSE")
        logo_lbl.setStyleSheet(
            f"color: {C['ink_inv']}; font-family: '{F_DISPLAY}'; "
            f"font-size: 32px; font-weight: 900; letter-spacing: -1px;"
        )
        logo_row.addWidget(logo_lbl)
        accent_dot = QLabel(".")
        accent_dot.setStyleSheet(
            f"color: {C['lime']}; font-family: '{F_DISPLAY}'; "
            f"font-size: 32px; font-weight: 900;"
        )
        logo_row.addWidget(accent_dot)
        logo_row.addStretch()
        ul.addLayout(logo_row)

        alt = QLabel("FITNESS · PERFORMANCE LAB")
        alt.setStyleSheet(
            f"color: {C['ink_inv_mut']}; font-family: '{F_MONO}'; "
            f"font-size: 9px; letter-spacing: 3px;"
        )
        ul.addWidget(alt)

        # ayrac
        ay = QFrame()
        ay.setFixedHeight(1)
        ay.setStyleSheet(f"background: {C['ink_inv_mut']};")
        ul.addWidget(ay)

        # Aktif sporcu seçici
        sec_lbl = QLabel("AKTİF SPORCU")
        sec_lbl.setStyleSheet(
            f"color: {C['ink_inv_mut']}; font-family: '{F_MONO}'; "
            f"font-size: 9px; letter-spacing: 2px;"
        )
        ul.addWidget(sec_lbl)

        self.sporcu_combo = QComboBox()
        self.sporcu_combo.setStyleSheet(f"""
            QComboBox {{
                background: transparent;
                color: {C['lime']};
                border: 0;
                border-bottom: 1.5px solid {C['ink_inv_mut']};
                padding: 6px 0;
                font-family: '{F_DISPLAY}';
                font-size: 18px;
                font-weight: 900;
            }}
            QComboBox:hover {{
                border-bottom: 1.5px solid {C['lime']};
            }}
            QComboBox::drop-down {{
                border: 0; width: 24px;
            }}
            QComboBox::down-arrow {{
                image: none;
                width: 0; height: 0;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid {C['lime']};
            }}
            QComboBox QAbstractItemView {{
                background: {C['ink']};
                color: {C['ink_inv']};
                border: 1px solid {C['ink_inv_mut']};
                selection-background-color: {C['lime']};
                selection-color: {C['lime_ink']};
                padding: 4px;
            }}
        """)
        self.sporcu_combo.currentIndexChanged.connect(self._sporcu_secim_degisti)
        ul.addWidget(self.sporcu_combo)

        l.addWidget(ust)

        # ─── Profil özet — büyük rakamlar ─────────────────
        self.profil_alan = QFrame()
        self.profil_alan.setStyleSheet("background: transparent; border: 0;")
        pl = QVBoxLayout(self.profil_alan)
        pl.setContentsMargins(24, 18, 24, 18)
        pl.setSpacing(14)

        # Yatay: VKİ + BMR
        ust_metrik = QHBoxLayout()
        ust_metrik.setSpacing(20)
        self.met_vki = SmallMetric("VKİ", "—", "", inverted=True)
        ust_metrik.addWidget(self.met_vki)
        self.met_bmr = SmallMetric("BMR", "—", "kcal", inverted=True)
        ust_metrik.addWidget(self.met_bmr)
        ust_metrik.addStretch()
        pl.addLayout(ust_metrik)

        # Yatay: kilo + boy
        alt_metrik = QHBoxLayout()
        alt_metrik.setSpacing(20)
        self.met_kilo = SmallMetric("Kilo", "—", "kg", inverted=True)
        alt_metrik.addWidget(self.met_kilo)
        self.met_boy = SmallMetric("Boy", "—", "cm", inverted=True)
        alt_metrik.addWidget(self.met_boy)
        alt_metrik.addStretch()
        pl.addLayout(alt_metrik)

        # Kategori rozeti
        self.kategori_rozet = Rozet("—", "outline")
        self.kategori_rozet.setStyleSheet(
            f"background: transparent; color: {C['lime']}; "
            f"border: 1px solid {C['lime']}; "
            f"padding: 4px 9px; "
            f"font-family: '{F_MONO}'; font-size: 9px; "
            f"font-weight: bold; letter-spacing: 1.5px;"
        )
        roz_row = QHBoxLayout()
        roz_row.addWidget(self.kategori_rozet)
        roz_row.addStretch()
        pl.addLayout(roz_row)

        l.addWidget(self.profil_alan)

        # Ayrac
        ay2 = QFrame()
        ay2.setFixedHeight(1)
        ay2.setStyleSheet(f"background: {C['ink_inv_mut']};")
        ay2_kapsayici = QWidget()
        ay2_l = QHBoxLayout(ay2_kapsayici)
        ay2_l.setContentsMargins(24, 0, 24, 0)
        ay2_l.addWidget(ay2)
        l.addWidget(ay2_kapsayici)

        # ─── NAV ─────────────────────────────────────────
        nav = QWidget()
        nl = QVBoxLayout(nav)
        nl.setContentsMargins(0, 16, 0, 16)
        nl.setSpacing(2)

        self.nav_grup = QButtonGroup(self)
        self.nav_grup.setExclusive(True)

        self.nav_dashboard = NavItem("01", "Dashboard")
        self.nav_dashboard.clicked.connect(lambda: self._sayfa_degistir(0))
        nl.addWidget(self.nav_dashboard)
        self.nav_grup.addButton(self.nav_dashboard, 0)

        self.nav_antrenman = NavItem("02", "Antrenmanlar")
        self.nav_antrenman.clicked.connect(lambda: self._sayfa_degistir(1))
        nl.addWidget(self.nav_antrenman)
        self.nav_grup.addButton(self.nav_antrenman, 1)

        self.nav_ilerleme = NavItem("03", "İlerleme")
        self.nav_ilerleme.clicked.connect(lambda: self._sayfa_degistir(2))
        nl.addWidget(self.nav_ilerleme)
        self.nav_grup.addButton(self.nav_ilerleme, 2)

        self.nav_takip = NavItem("04", "Günlük Takip")
        self.nav_takip.clicked.connect(lambda: self._sayfa_degistir(3))
        nl.addWidget(self.nav_takip)
        self.nav_grup.addButton(self.nav_takip, 3)

        l.addWidget(nav)
        l.addStretch()

        # ─── Alt: profil yönetim butonları ────────────────
        alt = QWidget()
        al = QVBoxLayout(alt)
        al.setContentsMargins(24, 12, 24, 24)
        al.setSpacing(10)

        ay3 = QFrame(); ay3.setFixedHeight(1)
        ay3.setStyleSheet(f"background: {C['ink_inv_mut']};")
        al.addWidget(ay3)

        btn_yeni = GhostButton("+ Yeni Sporcu", inverted=True)
        btn_yeni.clicked.connect(self._yeni_sporcu)
        al.addWidget(btn_yeni)

        btn_satir = QHBoxLayout()
        btn_satir.setSpacing(6)
        btn_duzenle = GhostButton("Düzenle", inverted=True)
        btn_duzenle.clicked.connect(self._duzenle_sporcu)
        btn_satir.addWidget(btn_duzenle)
        btn_sil = GhostButton("Sil", danger=True)
        btn_sil.clicked.connect(self._sil_sporcu)
        btn_satir.addWidget(btn_sil)
        al.addLayout(btn_satir)

        # küçük statü
        self.statu_lbl = QLabel("")
        self.statu_lbl.setStyleSheet(
            f"color: {C['ink_inv_mut']}; font-family: '{F_MONO}'; "
            f"font-size: 9px; letter-spacing: 1.5px; padding-top: 6px;"
        )
        self.statu_lbl.setAlignment(Qt.AlignCenter)
        al.addWidget(self.statu_lbl)

        l.addWidget(alt)

        parent_layout.addWidget(panel)

    # ═══════════════════════════════════════════════════════
    #  Sporcu yönetimi
    # ═══════════════════════════════════════════════════════
    def _sporcular_yukle(self, secilecek_id=None):
        self.sporcu_combo.blockSignals(True)
        self.sporcu_combo.clear()
        for s in self.vy.sporcular:
            self.sporcu_combo.addItem(s.ad, s.sporcu_id)

        if secilecek_id is not None:
            idx = self.sporcu_combo.findData(secilecek_id)
            if idx >= 0:
                self.sporcu_combo.setCurrentIndex(idx)
        self.sporcu_combo.blockSignals(False)

        if self.vy.sporcular:
            self._sporcu_secim_degisti()
        else:
            self._aktif_sporcu_temizle()

    def _sporcu_secim_degisti(self):
        sid = self.sporcu_combo.currentData()
        if sid is None:
            return
        s = self.vy.sporcu_bul(sid)
        if s is None:
            return
        self.aktif_sporcu = s
        self._profil_yenile()
        # tüm sayfalara dağıt
        for sayfa in (self.s_dashboard, self.s_antrenmanlar,
                      self.s_ilerleme, self.s_takip):
            sayfa.sporcu_ayarla(s)

    def _profil_yenile(self):
        s = self.aktif_sporcu
        if not s:
            self._aktif_sporcu_temizle()
            return
        self.met_vki.degeri_guncelle(f"{s.vki:g}")
        self.met_bmr.degeri_guncelle(str(s.bmr))
        self.met_kilo.degeri_guncelle(f"{s.kilo:g}")
        self.met_boy.degeri_guncelle(f"{s.boy:g}")
        self.kategori_rozet.setText(s.vki_kategori.upper())
        self.statu_lbl.setText(f"YAŞ {s.yas} · {s.cinsiyet.upper()}")

    def _aktif_sporcu_temizle(self):
        self.aktif_sporcu = None
        self.met_vki.degeri_guncelle("—")
        self.met_bmr.degeri_guncelle("—")
        self.met_kilo.degeri_guncelle("—")
        self.met_boy.degeri_guncelle("—")
        self.kategori_rozet.setText("—")
        self.statu_lbl.setText("SPORCU YOK")
        for sayfa in (self.s_dashboard, self.s_antrenmanlar,
                      self.s_ilerleme, self.s_takip):
            sayfa.sporcu_ayarla(None)

    # ═══════════════════════════════════════════════════════
    #  Aksiyonlar
    # ═══════════════════════════════════════════════════════
    def _yeni_sporcu(self):
        dlg = SporcuDiyalog(self)
        if dlg.exec_() and dlg.sonuc:
            yeni = self.vy.sporcu_ekle(**dlg.sonuc)
            self._sporcular_yukle(yeni.sporcu_id)

    def _duzenle_sporcu(self):
        if not self.aktif_sporcu:
            return
        dlg = SporcuDiyalog(self, self.aktif_sporcu)
        if dlg.exec_() and dlg.sonuc:
            self.vy.sporcu_guncelle(self.aktif_sporcu.sporcu_id, **dlg.sonuc)
            self._sporcular_yukle(self.aktif_sporcu.sporcu_id)

    def _sil_sporcu(self):
        if not self.aktif_sporcu:
            return
        ad = self.aktif_sporcu.ad
        cevap = QMessageBox.question(
            self, "Sporcu sil",
            f"{ad} ve buna bağlı tüm antrenman, takip ve ölçüm "
            f"kayıtları silinsin mi?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if cevap == QMessageBox.Yes:
            self.vy.sporcu_sil(self.aktif_sporcu.sporcu_id)
            self._sporcular_yukle()

    def _sayfa_degistir(self, idx: int):
        self.icerik.setCurrentIndex(idx)
        if idx == 0: self.nav_dashboard.setChecked(True)
        elif idx == 1: self.nav_antrenman.setChecked(True)
        elif idx == 2: self.nav_ilerleme.setChecked(True)
        elif idx == 3: self.nav_takip.setChecked(True)

    def _tum_sayfalari_yenile(self):
        # aktif sporcu güncellenmiş olabilir (özellikle ilerleme_kaydet sonrası kilo)
        if self.aktif_sporcu:
            self.aktif_sporcu = self.vy.sporcu_bul(self.aktif_sporcu.sporcu_id)
            self._profil_yenile()
            for sayfa in (self.s_dashboard, self.s_antrenmanlar,
                          self.s_ilerleme, self.s_takip):
                sayfa.sporcu = self.aktif_sporcu
                sayfa.yenile()
