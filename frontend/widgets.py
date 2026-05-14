"""
widgets.py
----------
Yeniden kullanılabilir özel widgetlar:
- StatCard: dashboard istatistik kartı
- KursCard: kurs listesi kartı
- OgrenciCard: öğrenci listesi kartı
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QProgressBar, QSizePolicy, QGraphicsDropShadowEffect
)

from .styles import COLORS


def _shadow(widget, blur=24, y=4, alpha=80):
    eff = QGraphicsDropShadowEffect(widget)
    eff.setBlurRadius(blur)
    eff.setOffset(0, y)
    eff.setColor(QColor(0, 0, 0, alpha))
    widget.setGraphicsEffect(eff)


class StatCard(QFrame):
    """Dashboard'da gösterilen istatistik kartı"""

    def __init__(self, label: str, value: str, hero: bool = False, parent=None):
        super().__init__(parent)
        self._hero = hero
        self.setObjectName("StatCardHero" if hero else "StatCard")
        self.setMinimumHeight(130)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Hero için inline stil de ver - QSS kaçabiliyor bazen
        if hero:
            self.setStyleSheet(f"""
                QFrame#StatCardHero {{
                    background-color: {COLORS['accent']};
                    border: 1px solid {COLORS['accent']};
                    border-radius: 14px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QFrame#StatCard {{
                    background-color: {COLORS['bg_card']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 14px;
                }}
            """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(0)

        self.lbl_label = QLabel(label)
        self.lbl_value = QLabel(value)

        if hero:
            self.lbl_label.setStyleSheet(f"""
                color: {COLORS['bg_primary']};
                background-color: transparent;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1.5px;
            """)
            self.lbl_value.setStyleSheet(f"""
                color: {COLORS['bg_primary']};
                background-color: transparent;
                font-size: 32px;
                font-weight: 700;
                letter-spacing: -1.5px;
            """)
        else:
            self.lbl_label.setStyleSheet(f"""
                color: {COLORS['text_muted']};
                background-color: transparent;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1.5px;
            """)
            self.lbl_value.setStyleSheet(f"""
                color: {COLORS['text_primary']};
                background-color: transparent;
                font-size: 32px;
                font-weight: 700;
                letter-spacing: -1.5px;
            """)

        layout.addWidget(self.lbl_label)
        layout.addStretch()
        layout.addWidget(self.lbl_value)

        if not hero:
            _shadow(self, blur=20, y=2, alpha=60)

    def setValue(self, value: str):
        self.lbl_value.setText(value)


class DotIndicator(QWidget):
    """Yan tarafa konan renkli nokta - her kart için kategori vurgusu"""
    def __init__(self, color: str, parent=None):
        super().__init__(parent)
        self._color = color
        self.setFixedSize(8, 8)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(self._color))
        p.drawEllipse(0, 0, 8, 8)


class KursCard(QFrame):
    """Tek bir kursu temsil eden kart"""
    kayit_istendi = pyqtSignal(int)   # kurs_id
    sil_istendi = pyqtSignal(int)
    detay_istendi = pyqtSignal(int)

    # Vurgu rengi - kurs id'sine göre rotate
    AKSAN_RENKLERI = ["#C8FF4B", "#FF9B6B", "#7CC8FF", "#E26BFF", "#FFD66B"]

    def __init__(self, kurs, parent=None):
        super().__init__(parent)
        self.kurs = kurs
        self.setObjectName("ItemCard")
        self.setMinimumHeight(180)
        self.setMaximumHeight(200)
        self.setMinimumWidth(0)
        self._build()

    def _build(self):
        kurs = self.kurs
        aksan = self.AKSAN_RENKLERI[(kurs.kurs_id - 1) % len(self.AKSAN_RENKLERI)]

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 18, 20, 18)
        outer.setSpacing(0)

        # ---- Üst satır: ID badge + dot ----
        top = QHBoxLayout()
        top.setSpacing(8)
        dot = DotIndicator(aksan)
        id_lbl = QLabel(f"KURS / {kurs.kurs_id:03d}")
        id_lbl.setObjectName("CardId")
        top.addWidget(dot)
        top.addWidget(id_lbl)
        top.addStretch()

        # Doluluk yüzdesi sağda küçük yazı
        doluluk_pct = int(kurs.doluluk_yuzdesi())
        pct_lbl = QLabel(f"{doluluk_pct}%")
        pct_font = QFont()
        pct_font.setPointSize(10)
        pct_font.setBold(True)
        pct_lbl.setFont(pct_font)
        pct_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; letter-spacing: 1px;")
        top.addWidget(pct_lbl)

        outer.addLayout(top)
        outer.addSpacing(12)

        # ---- Başlık ----
        title = QLabel(kurs.kurs_adi)
        title.setObjectName("CardTitle")
        title.setWordWrap(True)
        outer.addWidget(title)

        # ---- Eğitmen ----
        meta = QLabel(f"{kurs.egitmen.ad}  ·  {kurs.egitmen.uzmanlik}")
        meta.setObjectName("CardMeta")
        outer.addWidget(meta)

        outer.addStretch()

        # ---- Doluluk barı ----
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(doluluk_pct)
        bar.setFixedHeight(4)
        bar.setStyleSheet(f"""
            QProgressBar {{ background-color: {COLORS['border_soft']};
                            border: none; border-radius: 2px; }}
            QProgressBar::chunk {{ background-color: {aksan}; border-radius: 2px; }}
        """)
        outer.addWidget(bar)
        outer.addSpacing(10)

        # ---- Alt satır: kayıtlı sayısı + butonlar ----
        bottom = QHBoxLayout()
        bottom.setSpacing(8)

        kayit_lbl = QLabel(
            f"{len(kurs.kayitli_ogrenciler)}/{kurs.kontenjan} kayıtlı"
        )
        kayit_lbl.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 600;"
        )
        bottom.addWidget(kayit_lbl)
        bottom.addStretch()

        btn_kayit = QPushButton("Kayıt")
        btn_kayit.setObjectName("PrimaryButton")
        btn_kayit.setCursor(Qt.PointingHandCursor)
        btn_kayit.setFixedHeight(32)
        btn_kayit.setMinimumWidth(70)
        btn_kayit.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: {COLORS['bg_primary']};
                border: 1px solid {COLORS['accent']};
                border-radius: 8px;
                padding: 6px 14px;
                font-weight: 700;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_dim']};
                border: 1px solid {COLORS['accent_dim']};
            }}
        """)
        btn_kayit.clicked.connect(lambda: self.kayit_istendi.emit(kurs.kurs_id))

        btn_detay = QPushButton("Detay")
        btn_detay.setObjectName("GhostButton")
        btn_detay.setCursor(Qt.PointingHandCursor)
        btn_detay.setFixedHeight(32)
        btn_detay.clicked.connect(lambda: self.detay_istendi.emit(kurs.kurs_id))

        btn_sil = QPushButton("✕")
        btn_sil.setObjectName("DangerButton")
        btn_sil.setCursor(Qt.PointingHandCursor)
        btn_sil.setFixedSize(32, 32)
        btn_sil.setToolTip("Kursu sil")
        btn_sil.clicked.connect(lambda: self.sil_istendi.emit(kurs.kurs_id))

        bottom.addWidget(btn_detay)
        bottom.addWidget(btn_kayit)
        bottom.addWidget(btn_sil)
        outer.addLayout(bottom)


class OgrenciCard(QFrame):
    """Tek bir öğrenciyi temsil eden kart"""
    sil_istendi = pyqtSignal(int)
    detay_istendi = pyqtSignal(int)

    def __init__(self, ogrenci, kurs_sayisi: int, parent=None):
        super().__init__(parent)
        self.ogrenci = ogrenci
        self.kurs_sayisi = kurs_sayisi
        self.setObjectName("ItemCard")
        self.setMinimumHeight(110)
        self.setMaximumHeight(120)
        self._build()

    def _build(self):
        ogr = self.ogrenci
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)

        # Avatar - baş harfler
        initials = "".join([p[0].upper() for p in ogr.ad.split()[:2]])
        avatar = QLabel(initials)
        avatar.setFixedSize(48, 48)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(f"""
            background-color: {COLORS['accent_soft']};
            color: {COLORS['accent']};
            border: 1px solid {COLORS['accent_dim']};
            border-radius: 24px;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 0.5px;
        """)
        layout.addWidget(avatar)

        # İsim + email
        info = QVBoxLayout()
        info.setSpacing(2)

        # ID küçük
        id_lbl = QLabel(f"#{ogr.ogrenci_id:03d}")
        id_lbl.setStyleSheet(f"""
            color: {COLORS['text_dim']}; font-size: 10px;
            font-weight: 700; letter-spacing: 2px;
        """)
        info.addWidget(id_lbl)

        ad = QLabel(ogr.ad)
        ad.setObjectName("CardTitle")
        info.addWidget(ad)

        email = QLabel(ogr.email)
        email.setObjectName("CardMeta")
        info.addWidget(email)

        layout.addLayout(info)
        layout.addStretch()

        # Kayıtlı kurs sayısı
        kurs_box = QVBoxLayout()
        kurs_box.setSpacing(0)
        kurs_box.setAlignment(Qt.AlignCenter)
        sayi = QLabel(str(self.kurs_sayisi))
        sayi.setAlignment(Qt.AlignCenter)
        sayi.setStyleSheet(f"""
            color: {COLORS['accent']}; font-size: 22px; font-weight: 700;
            letter-spacing: -1px;
        """)
        etk = QLabel("KURS")
        etk.setAlignment(Qt.AlignCenter)
        etk.setStyleSheet(f"""
            color: {COLORS['text_muted']}; font-size: 9px;
            font-weight: 700; letter-spacing: 2px;
        """)
        kurs_box.addWidget(sayi)
        kurs_box.addWidget(etk)
        layout.addLayout(kurs_box)

        # Butonlar
        btn_detay = QPushButton("Detay")
        btn_detay.setObjectName("GhostButton")
        btn_detay.setCursor(Qt.PointingHandCursor)
        btn_detay.setFixedHeight(32)
        btn_detay.clicked.connect(lambda: self.detay_istendi.emit(ogr.ogrenci_id))

        btn_sil = QPushButton("✕")
        btn_sil.setObjectName("DangerButton")
        btn_sil.setCursor(Qt.PointingHandCursor)
        btn_sil.setFixedSize(32, 32)
        btn_sil.setToolTip("Öğrenciyi sil")
        btn_sil.clicked.connect(lambda: self.sil_istendi.emit(ogr.ogrenci_id))

        layout.addWidget(btn_detay)
        layout.addWidget(btn_sil)
