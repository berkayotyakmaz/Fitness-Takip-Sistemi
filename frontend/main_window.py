"""
main_window.py
--------------
Ana pencere. Sol sidebar + sayfa stack:
    - Dashboard (özet)
    - Kurslar (grid)
    - Öğrenciler (list)
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QFrame, QScrollArea, QGridLayout,
    QLineEdit, QMessageBox, QButtonGroup, QSizePolicy
)

from backend import PlatformService
from .styles import QSS, COLORS
from .widgets import StatCard, KursCard, OgrenciCard
from .dialogs import (
    KursEkleDialog, OgrenciEkleDialog, KayitDialog,
    KursDetayDialog, OgrenciDetayDialog
)


class MainWindow(QMainWindow):
    """Ana uygulama penceresi"""

    def __init__(self, service: PlatformService):
        super().__init__()
        self.service = service
        self.setWindowTitle("Lumen — Online Kurs Platformu")
        self.setMinimumSize(1180, 760)
        self.resize(1280, 820)
        self.setStyleSheet(QSS)

        self._build_ui()
        self._refresh_all()

    # ============================================================
    # YAPILANDIRMA
    # ============================================================
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ---- SIDEBAR ----
        root.addWidget(self._build_sidebar())

        # ---- İÇERİK ALANI ----
        content_wrap = QWidget()
        content_wrap.setStyleSheet(f"background-color: {COLORS['bg_primary']};")
        content = QVBoxLayout(content_wrap)
        content.setContentsMargins(40, 32, 40, 32)
        content.setSpacing(0)

        self.stack = QStackedWidget()
        self.page_dashboard = self._build_dashboard_page()
        self.page_kurslar = self._build_kurslar_page()
        self.page_ogrenciler = self._build_ogrenciler_page()
        self.stack.addWidget(self.page_dashboard)
        self.stack.addWidget(self.page_kurslar)
        self.stack.addWidget(self.page_ogrenciler)

        content.addWidget(self.stack, 1)
        root.addWidget(content_wrap, 1)

    # ------------------------------------------------------------
    # SIDEBAR
    # ------------------------------------------------------------
    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(248)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 28, 20, 24)
        layout.setSpacing(0)

        # Brand
        brand_box = QHBoxLayout()
        brand_box.setSpacing(10)

        # Logo bloğu - lime kare ile minimal mark
        logo = QLabel()
        logo.setFixedSize(34, 34)
        logo.setStyleSheet(f"""
            background-color: {COLORS['accent']};
            border-radius: 8px;
        """)

        brand_text = QVBoxLayout()
        brand_text.setSpacing(0)
        brand_text.setContentsMargins(0, 0, 0, 0)
        sub = QLabel("PLATFORM")
        sub.setObjectName("BrandSubtitle")
        name = QLabel("Lumen")
        name.setObjectName("BrandLabel")
        brand_text.addWidget(sub)
        brand_text.addWidget(name)

        brand_box.addWidget(logo)
        brand_box.addLayout(brand_text)
        brand_box.addStretch()

        layout.addLayout(brand_box)
        layout.addSpacing(36)

        # Section header
        sec = QLabel("MENÜ")
        sec.setObjectName("SidebarSection")
        layout.addWidget(sec)
        layout.addSpacing(6)

        # Nav butonları
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        self.btn_dashboard = self._nav_button("◐  Dashboard", 0)
        self.btn_kurslar = self._nav_button("▣  Kurslar", 1)
        self.btn_ogrenciler = self._nav_button("◉  Öğrenciler", 2)
        self.btn_dashboard.setChecked(True)

        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_kurslar)
        layout.addWidget(self.btn_ogrenciler)

        layout.addStretch()

        # Alt: küçük durum kutusu
        durum = QFrame()
        durum.setObjectName("ItemCard")
        d_layout = QVBoxLayout(durum)
        d_layout.setContentsMargins(16, 14, 16, 14)
        d_layout.setSpacing(2)
        eyebrow = QLabel("v1.0  ·  LIVE")
        eyebrow.setStyleSheet(
            f"color: {COLORS['accent']}; font-size: 10px; "
            f"font-weight: 700; letter-spacing: 2px;"
        )
        info = QLabel("Tüm değişiklikler otomatik kaydediliyor.")
        info.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        info.setWordWrap(True)
        d_layout.addWidget(eyebrow)
        d_layout.addWidget(info)
        layout.addWidget(durum)

        return sidebar

    def _nav_button(self, text: str, page_idx: int) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("NavButton")
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.clicked.connect(lambda: self._switch_page(page_idx))
        self.nav_group.addButton(btn)
        return btn

    def _switch_page(self, idx: int):
        self.stack.setCurrentIndex(idx)
        # İlgili nav butonunu check et
        btns = [self.btn_dashboard, self.btn_kurslar, self.btn_ogrenciler]
        for i, b in enumerate(btns):
            b.setChecked(i == idx)
        if idx == 0:
            self._refresh_dashboard()
        elif idx == 1:
            self._refresh_kurslar()
        elif idx == 2:
            self._refresh_ogrenciler()

    # ------------------------------------------------------------
    # DASHBOARD SAYFASI
    # ------------------------------------------------------------
    def _build_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = self._page_header(
            eyebrow="GENEL BAKIŞ",
            title="Dashboard",
            subtitle="Platform sağlığı ve hızlı işlemler.",
        )
        layout.addLayout(header)
        layout.addSpacing(28)

        # Stat kartları
        stats = QHBoxLayout()
        stats.setSpacing(14)

        self.stat_kurslar = StatCard("TOPLAM KURS", "0")
        self.stat_ogrenci = StatCard("TOPLAM ÖĞRENCİ", "0")
        self.stat_kayit = StatCard("AKTİF KAYIT", "0", hero=True)
        self.stat_doluluk = StatCard("ORT. DOLULUK", "0%")

        stats.addWidget(self.stat_kurslar)
        stats.addWidget(self.stat_ogrenci)
        stats.addWidget(self.stat_kayit)
        stats.addWidget(self.stat_doluluk)

        layout.addLayout(stats)
        layout.addSpacing(36)

        # Hızlı işlemler
        layout.addLayout(self._sub_header("HIZLI İŞLEMLER", "Yaygın görevler"))
        layout.addSpacing(14)

        actions = QHBoxLayout()
        actions.setSpacing(12)

        a1 = self._action_tile("Yeni Kurs", "Eğitmen ata, kontenjan belirle", True,
                                self._yeni_kurs)
        a2 = self._action_tile("Yeni Öğrenci", "Sisteme öğrenci ekle", False,
                                self._yeni_ogrenci)
        a3 = self._action_tile("Kayıt Al", "Bir kursa öğrenci kaydet", False,
                                self._dashboard_kayit_al)

        actions.addWidget(a1)
        actions.addWidget(a2)
        actions.addWidget(a3)
        layout.addLayout(actions)

        layout.addStretch()
        return page

    def _action_tile(self, title, sub, primary, on_click):
        f = QFrame()
        f.setObjectName("ItemCard")
        f.setMinimumHeight(110)
        f.setCursor(Qt.PointingHandCursor)

        v = QVBoxLayout(f)
        v.setContentsMargins(20, 18, 20, 18)
        v.setSpacing(2)

        eyebrow = QLabel("→")
        eyebrow.setStyleSheet(
            f"color: {COLORS['accent'] if primary else COLORS['text_muted']}; "
            f"font-size: 16px; font-weight: 700;"
        )
        v.addWidget(eyebrow)
        v.addStretch()

        t = QLabel(title)
        t.setStyleSheet(
            f"color: {COLORS['text_primary']}; font-size: 16px; "
            f"font-weight: 700; letter-spacing: -0.3px;"
        )
        v.addWidget(t)
        s = QLabel(sub)
        s.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        v.addWidget(s)

        f.mousePressEvent = lambda _e: on_click()
        return f

    # ------------------------------------------------------------
    # KURSLAR SAYFASI
    # ------------------------------------------------------------
    def _build_kurslar_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header + buton
        header_row = QHBoxLayout()
        header_layout = self._page_header(
            eyebrow="KATALOG",
            title="Kurslar",
            subtitle="Tüm aktif kursları yönet, yeni kurs aç.",
        )
        header_row.addLayout(header_layout, 1)

        btn_yeni = QPushButton("+ Yeni Kurs")
        btn_yeni.setObjectName("PrimaryButton")
        btn_yeni.setCursor(Qt.PointingHandCursor)
        btn_yeni.setFixedHeight(42)
        btn_yeni.setMinimumWidth(140)
        btn_yeni.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: {COLORS['bg_primary']};
                border: 1px solid {COLORS['accent']};
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: 700;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_dim']};
                border: 1px solid {COLORS['accent_dim']};
            }}
        """)
        btn_yeni.clicked.connect(self._yeni_kurs)
        header_row.addWidget(btn_yeni, alignment=Qt.AlignBottom)

        layout.addLayout(header_row)
        layout.addSpacing(20)

        # Arama
        self.kurs_search = QLineEdit()
        self.kurs_search.setPlaceholderText("Kurs adı veya eğitmen ara...")
        self.kurs_search.textChanged.connect(self._refresh_kurslar)
        self.kurs_search.setMaximumWidth(380)
        layout.addWidget(self.kurs_search)
        layout.addSpacing(20)

        # Grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.kurslar_container = QWidget()
        self.kurslar_grid = QGridLayout(self.kurslar_container)
        self.kurslar_grid.setContentsMargins(0, 0, 6, 0)
        self.kurslar_grid.setSpacing(14)

        scroll.setWidget(self.kurslar_container)
        layout.addWidget(scroll, 1)

        return page

    # ------------------------------------------------------------
    # ÖĞRENCİLER SAYFASI
    # ------------------------------------------------------------
    def _build_ogrenciler_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header_row = QHBoxLayout()
        header_layout = self._page_header(
            eyebrow="DİZİN",
            title="Öğrenciler",
            subtitle="Sisteme kayıtlı tüm öğrenciler.",
        )
        header_row.addLayout(header_layout, 1)

        btn_yeni = QPushButton("+ Yeni Öğrenci")
        btn_yeni.setObjectName("PrimaryButton")
        btn_yeni.setCursor(Qt.PointingHandCursor)
        btn_yeni.setFixedHeight(42)
        btn_yeni.setMinimumWidth(160)
        btn_yeni.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: {COLORS['bg_primary']};
                border: 1px solid {COLORS['accent']};
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: 700;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_dim']};
                border: 1px solid {COLORS['accent_dim']};
            }}
        """)
        btn_yeni.clicked.connect(self._yeni_ogrenci)
        header_row.addWidget(btn_yeni, alignment=Qt.AlignBottom)

        layout.addLayout(header_row)
        layout.addSpacing(20)

        self.ogr_search = QLineEdit()
        self.ogr_search.setPlaceholderText("İsim veya e-posta ara...")
        self.ogr_search.textChanged.connect(self._refresh_ogrenciler)
        self.ogr_search.setMaximumWidth(380)
        layout.addWidget(self.ogr_search)
        layout.addSpacing(20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.ogrenciler_container = QWidget()
        self.ogrenciler_layout = QVBoxLayout(self.ogrenciler_container)
        self.ogrenciler_layout.setContentsMargins(0, 0, 6, 0)
        self.ogrenciler_layout.setSpacing(10)
        self.ogrenciler_layout.addStretch()

        scroll.setWidget(self.ogrenciler_container)
        layout.addWidget(scroll, 1)

        return page

    # ------------------------------------------------------------
    # ORTAK YARDIMCILAR
    # ------------------------------------------------------------
    def _page_header(self, eyebrow, title, subtitle):
        v = QVBoxLayout()
        v.setSpacing(4)
        e = QLabel(eyebrow)
        e.setObjectName("Eyebrow")
        v.addWidget(e)
        t = QLabel(title)
        t.setObjectName("PageTitle")
        v.addWidget(t)
        s = QLabel(subtitle)
        s.setObjectName("PageSubtitle")
        v.addWidget(s)
        return v

    def _sub_header(self, eyebrow, title):
        v = QVBoxLayout()
        v.setSpacing(2)
        e = QLabel(eyebrow)
        e.setObjectName("Eyebrow")
        v.addWidget(e)
        t = QLabel(title)
        t.setObjectName("SectionTitle")
        v.addWidget(t)
        return v

    # ============================================================
    # REFRESH
    # ============================================================
    def _refresh_all(self):
        self._refresh_dashboard()
        self._refresh_kurslar()
        self._refresh_ogrenciler()

    def _refresh_dashboard(self):
        self.stat_kurslar.setValue(str(len(self.service.kurslar)))
        self.stat_ogrenci.setValue(str(len(self.service.ogrenciler)))
        self.stat_kayit.setValue(str(self.service.toplam_kayit_sayisi()))
        self.stat_doluluk.setValue(f"{int(self.service.ortalama_doluluk())}%")

    def _refresh_kurslar(self):
        # Eski kartları temizle
        while self.kurslar_grid.count():
            it = self.kurslar_grid.takeAt(0)
            w = it.widget()
            if w:
                w.deleteLater()

        q = self.kurs_search.text().strip().lower()
        kurslar = self.service.kurslar
        if q:
            kurslar = [k for k in kurslar if q in k.kurs_adi.lower()
                       or q in k.egitmen.ad.lower()
                       or q in k.egitmen.uzmanlik.lower()]

        if not kurslar:
            empty = self._empty_state(
                "Kurs bulunamadı" if q else "Henüz kurs yok",
                "Yeni bir kurs ekleyerek başla."
            )
            self.kurslar_grid.addWidget(empty, 0, 0, 1, 3)
            return

        # 2 sütunlu grid (responsive ve okunaklı)
        cols = 2
        for i, kurs in enumerate(kurslar):
            card = KursCard(kurs)
            card.kayit_istendi.connect(self._kursa_kayit)
            card.sil_istendi.connect(self._kurs_sil)
            card.detay_istendi.connect(self._kurs_detay)
            row, col = divmod(i, cols)
            self.kurslar_grid.addWidget(card, row, col)

        # Sütunları eşit dağıt
        for c in range(cols):
            self.kurslar_grid.setColumnStretch(c, 1)
        # Boş alt satırları yiyen satır
        last_row = (len(kurslar) - 1) // cols + 1
        self.kurslar_grid.setRowStretch(last_row, 1)

    def _refresh_ogrenciler(self):
        # Stretch hariç hepsini temizle
        while self.ogrenciler_layout.count() > 1:
            it = self.ogrenciler_layout.takeAt(0)
            w = it.widget()
            if w:
                w.deleteLater()

        q = self.ogr_search.text().strip().lower()
        ogrenciler = self.service.ogrenciler
        if q:
            ogrenciler = [o for o in ogrenciler
                          if q in o.ad.lower() or q in o.email.lower()]

        if not ogrenciler:
            empty = self._empty_state(
                "Öğrenci bulunamadı" if q else "Henüz öğrenci yok",
                "Yeni bir öğrenci ekleyerek başla."
            )
            self.ogrenciler_layout.insertWidget(0, empty)
            return

        for ogr in ogrenciler:
            card = OgrenciCard(ogr, len(ogr.kayitli_kurslar))
            card.sil_istendi.connect(self._ogrenci_sil)
            card.detay_istendi.connect(self._ogrenci_detay)
            self.ogrenciler_layout.insertWidget(
                self.ogrenciler_layout.count() - 1, card
            )

    def _empty_state(self, title, sub):
        f = QFrame()
        f.setObjectName("ItemCard")
        f.setMinimumHeight(180)
        v = QVBoxLayout(f)
        v.setAlignment(Qt.AlignCenter)
        t = QLabel(title)
        t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet(
            f"color: {COLORS['text_primary']}; font-size: 16px; "
            f"font-weight: 700;"
        )
        s = QLabel(sub)
        s.setAlignment(Qt.AlignCenter)
        s.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        v.addWidget(t)
        v.addWidget(s)
        return f

    # ============================================================
    # AKSİYON HANDLERLARI
    # ============================================================
    def _yeni_kurs(self):
        dlg = KursEkleDialog(self)
        if dlg.exec_() == dlg.Accepted:
            v = dlg.values()
            self.service.kurs_ekle(
                v["kurs_adi"], v["egitmen_ad"], v["uzmanlik"], v["kontenjan"]
            )
            self._refresh_all()
            self._toast("Kurs oluşturuldu.")

    def _yeni_ogrenci(self):
        dlg = OgrenciEkleDialog(self)
        if dlg.exec_() == dlg.Accepted:
            v = dlg.values()
            self.service.ogrenci_ekle(v["ad"], v["email"])
            self._refresh_all()
            self._toast("Öğrenci eklendi.")

    def _kursa_kayit(self, kurs_id: int):
        kurs = self.service.kurs_bul(kurs_id)
        if not kurs:
            return
        if not self.service.ogrenciler:
            QMessageBox.information(
                self, "Öğrenci yok",
                "Önce bir öğrenci ekle, sonra kayıt al."
            )
            return
        dlg = KayitDialog(kurs, self.service.ogrenciler, self)
        if dlg.exec_() == dlg.Accepted and dlg.secilen_ogrenci_id is not None:
            ok, msg = self.service.kursa_kayit(kurs_id, dlg.secilen_ogrenci_id)
            if ok:
                self._refresh_all()
                self._toast(msg)
            else:
                QMessageBox.warning(self, "Kayıt başarısız", msg)

    def _dashboard_kayit_al(self):
        if not self.service.kurslar:
            QMessageBox.information(self, "Kurs yok",
                                    "Önce bir kurs oluştur.")
            return
        # Dashboard'dan: ilk kursu seç ya da kurslar sayfasına git
        self._switch_page(1)
        self.btn_kurslar.setChecked(True)

    def _kurs_sil(self, kurs_id: int):
        kurs = self.service.kurs_bul(kurs_id)
        if not kurs:
            return
        ans = QMessageBox.question(
            self, "Kursu sil",
            f"\"{kurs.kurs_adi}\" silinsin mi?\n"
            f"Bu kursa kayıtlı {len(kurs.kayitli_ogrenciler)} öğrencinin "
            f"kaydı da iptal edilecek.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ans == QMessageBox.Yes:
            self.service.kurs_sil(kurs_id)
            self._refresh_all()
            self._toast("Kurs silindi.")

    def _ogrenci_sil(self, ogrenci_id: int):
        ogr = self.service.ogrenci_bul(ogrenci_id)
        if not ogr:
            return
        ans = QMessageBox.question(
            self, "Öğrenciyi sil",
            f"\"{ogr.ad}\" silinsin mi?\n"
            f"Tüm kurs kayıtları da iptal edilecek.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ans == QMessageBox.Yes:
            self.service.ogrenci_sil(ogrenci_id)
            self._refresh_all()
            self._toast("Öğrenci silindi.")

    def _kurs_detay(self, kurs_id: int):
        kurs = self.service.kurs_bul(kurs_id)
        if not kurs:
            return
        kayitli = [self.service.ogrenci_bul(oid)
                   for oid in kurs.kayitli_ogrenciler]
        kayitli = [o for o in kayitli if o is not None]
        dlg = KursDetayDialog(kurs, kayitli, self)
        dlg.exec_()

    def _ogrenci_detay(self, ogrenci_id: int):
        ogr = self.service.ogrenci_bul(ogrenci_id)
        if not ogr:
            return
        kurslar = ogr.kurs_listesi(self.service.kurslar)
        dlg = OgrenciDetayDialog(ogr, kurslar, self)
        dlg.exec_()

    def _toast(self, msg: str):
        """Kısa durum mesajı - status bar tarzı"""
        self.statusBar().setStyleSheet(
            f"background-color: {COLORS['bg_panel']}; "
            f"color: {COLORS['accent']}; font-weight: 600; padding: 4px 16px;"
        )
        self.statusBar().showMessage(f"  ✓  {msg}", 2500)
