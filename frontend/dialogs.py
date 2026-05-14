"""
dialogs.py
----------
Modal dialoglar:
- KursEkleDialog
- OgrenciEkleDialog
- KayitDialog (kursa öğrenci kaydetme)
- KursDetayDialog
- OgrenciDetayDialog
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QSpinBox, QComboBox,
    QVBoxLayout, QHBoxLayout, QPushButton, QFrame,
    QListWidget, QListWidgetItem, QMessageBox
)

from .styles import COLORS


def _form_label(text):
    lbl = QLabel(text)
    lbl.setObjectName("FormLabel")
    return lbl


class KursEkleDialog(QDialog):
    """Yeni kurs ekleme penceresi"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Kurs")
        self.setMinimumWidth(440)
        self.setModal(True)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(8)

        eyebrow = QLabel("YENİ KAYIT")
        eyebrow.setObjectName("Eyebrow")
        layout.addWidget(eyebrow)

        title = QLabel("Kurs Tanımla")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        sub = QLabel("Eğitmen ve kontenjan bilgilerini doldur.")
        sub.setObjectName("PageSubtitle")
        layout.addWidget(sub)
        layout.addSpacing(20)

        # Kurs adı
        layout.addWidget(_form_label("KURS ADI"))
        self.in_kurs_adi = QLineEdit()
        self.in_kurs_adi.setPlaceholderText("Örn: Modern Web Geliştirme")
        layout.addWidget(self.in_kurs_adi)
        layout.addSpacing(12)

        # Eğitmen
        row = QHBoxLayout()
        row.setSpacing(12)

        col1 = QVBoxLayout()
        col1.setSpacing(6)
        col1.addWidget(_form_label("EĞİTMEN ADI"))
        self.in_egitmen = QLineEdit()
        self.in_egitmen.setPlaceholderText("Ad Soyad")
        col1.addWidget(self.in_egitmen)
        row.addLayout(col1)

        col2 = QVBoxLayout()
        col2.setSpacing(6)
        col2.addWidget(_form_label("UZMANLIK"))
        self.in_uzmanlik = QLineEdit()
        self.in_uzmanlik.setPlaceholderText("Örn: Frontend")
        col2.addWidget(self.in_uzmanlik)
        row.addLayout(col2)

        layout.addLayout(row)
        layout.addSpacing(12)

        # Kontenjan
        layout.addWidget(_form_label("KONTENJAN"))
        self.in_kontenjan = QSpinBox()
        self.in_kontenjan.setRange(1, 1000)
        self.in_kontenjan.setValue(25)
        layout.addWidget(self.in_kontenjan)
        layout.addSpacing(24)

        # Butonlar
        btns = QHBoxLayout()
        btns.setSpacing(10)
        btns.addStretch()
        btn_iptal = QPushButton("İptal")
        btn_iptal.setObjectName("GhostButton")
        btn_iptal.setCursor(Qt.PointingHandCursor)
        btn_iptal.clicked.connect(self.reject)

        btn_kaydet = QPushButton("Kursu Oluştur")
        btn_kaydet.setObjectName("PrimaryButton")
        btn_kaydet.setCursor(Qt.PointingHandCursor)
        btn_kaydet.clicked.connect(self._on_kaydet)

        btns.addWidget(btn_iptal)
        btns.addWidget(btn_kaydet)
        layout.addLayout(btns)

    def _on_kaydet(self):
        if not self.in_kurs_adi.text().strip():
            QMessageBox.warning(self, "Eksik bilgi", "Kurs adı zorunludur.")
            return
        if not self.in_egitmen.text().strip():
            QMessageBox.warning(self, "Eksik bilgi", "Eğitmen adı zorunludur.")
            return
        if not self.in_uzmanlik.text().strip():
            QMessageBox.warning(self, "Eksik bilgi", "Uzmanlık alanı zorunludur.")
            return
        self.accept()

    def values(self):
        return {
            "kurs_adi": self.in_kurs_adi.text().strip(),
            "egitmen_ad": self.in_egitmen.text().strip(),
            "uzmanlik": self.in_uzmanlik.text().strip(),
            "kontenjan": self.in_kontenjan.value(),
        }


class OgrenciEkleDialog(QDialog):
    """Yeni öğrenci ekleme penceresi"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Öğrenci")
        self.setMinimumWidth(420)
        self.setModal(True)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(8)

        eyebrow = QLabel("YENİ KAYIT")
        eyebrow.setObjectName("Eyebrow")
        layout.addWidget(eyebrow)

        title = QLabel("Öğrenci Ekle")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        sub = QLabel("Sisteme yeni bir öğrenci ekle.")
        sub.setObjectName("PageSubtitle")
        layout.addWidget(sub)
        layout.addSpacing(20)

        layout.addWidget(_form_label("AD SOYAD"))
        self.in_ad = QLineEdit()
        self.in_ad.setPlaceholderText("Örn: Ahmet Yılmaz")
        layout.addWidget(self.in_ad)
        layout.addSpacing(12)

        layout.addWidget(_form_label("E-POSTA"))
        self.in_email = QLineEdit()
        self.in_email.setPlaceholderText("ornek@mail.com")
        layout.addWidget(self.in_email)
        layout.addSpacing(24)

        btns = QHBoxLayout()
        btns.setSpacing(10)
        btns.addStretch()
        btn_iptal = QPushButton("İptal")
        btn_iptal.setObjectName("GhostButton")
        btn_iptal.setCursor(Qt.PointingHandCursor)
        btn_iptal.clicked.connect(self.reject)

        btn_kaydet = QPushButton("Öğrenciyi Ekle")
        btn_kaydet.setObjectName("PrimaryButton")
        btn_kaydet.setCursor(Qt.PointingHandCursor)
        btn_kaydet.clicked.connect(self._on_kaydet)

        btns.addWidget(btn_iptal)
        btns.addWidget(btn_kaydet)
        layout.addLayout(btns)

    def _on_kaydet(self):
        if not self.in_ad.text().strip():
            QMessageBox.warning(self, "Eksik bilgi", "Ad zorunludur.")
            return
        email = self.in_email.text().strip()
        if not email or "@" not in email:
            QMessageBox.warning(self, "Geçersiz e-posta",
                                "Geçerli bir e-posta adresi gir.")
            return
        self.accept()

    def values(self):
        return {
            "ad": self.in_ad.text().strip(),
            "email": self.in_email.text().strip(),
        }


class KayitDialog(QDialog):
    """Bir kursa öğrenci kaydetme dialogu"""

    def __init__(self, kurs, ogrenciler, parent=None):
        super().__init__(parent)
        self.kurs = kurs
        self.ogrenciler = ogrenciler
        self.secilen_ogrenci_id = None
        self.setWindowTitle("Kursa Kayıt")
        self.setMinimumWidth(460)
        self.setMinimumHeight(500)
        self.setModal(True)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(8)

        eyebrow = QLabel("KURSA KAYIT")
        eyebrow.setObjectName("Eyebrow")
        layout.addWidget(eyebrow)

        title = QLabel(self.kurs.kurs_adi)
        title.setObjectName("PageTitle")
        title.setWordWrap(True)
        layout.addWidget(title)

        bos = self.kurs.bos_kontenjan()
        sub = QLabel(f"{self.kurs.egitmen.ad}  ·  {bos} boş kontenjan")
        sub.setObjectName("PageSubtitle")
        layout.addWidget(sub)
        layout.addSpacing(20)

        layout.addWidget(_form_label("ÖĞRENCİ SEÇ"))

        self.list_ogr = QListWidget()
        for ogr in self.ogrenciler:
            kayitli = ogr.ogrenci_id in self.kurs.kayitli_ogrenciler
            ek = "  ·  Kayıtlı" if kayitli else ""
            item = QListWidgetItem(f"#{ogr.ogrenci_id:03d}   {ogr.ad}   ·   {ogr.email}{ek}")
            item.setData(Qt.UserRole, ogr.ogrenci_id)
            if kayitli:
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            self.list_ogr.addItem(item)
        layout.addWidget(self.list_ogr, 1)

        layout.addSpacing(16)
        btns = QHBoxLayout()
        btns.setSpacing(10)
        btns.addStretch()
        btn_iptal = QPushButton("İptal")
        btn_iptal.setObjectName("GhostButton")
        btn_iptal.setCursor(Qt.PointingHandCursor)
        btn_iptal.clicked.connect(self.reject)

        btn_kaydet = QPushButton("Kaydet")
        btn_kaydet.setObjectName("PrimaryButton")
        btn_kaydet.setCursor(Qt.PointingHandCursor)
        btn_kaydet.clicked.connect(self._on_kaydet)

        btns.addWidget(btn_iptal)
        btns.addWidget(btn_kaydet)
        layout.addLayout(btns)

    def _on_kaydet(self):
        item = self.list_ogr.currentItem()
        if not item:
            QMessageBox.warning(self, "Seçim yok", "Bir öğrenci seç.")
            return
        self.secilen_ogrenci_id = item.data(Qt.UserRole)
        self.accept()


class KursDetayDialog(QDialog):
    """Bir kursun detayını ve kayıtlı öğrencilerini gösterir"""

    def __init__(self, kurs, kayitli_ogrenciler, parent=None):
        super().__init__(parent)
        self.kurs = kurs
        self.kayitli_ogrenciler = kayitli_ogrenciler
        self.setWindowTitle("Kurs Detayı")
        self.setMinimumSize(480, 540)
        self.setModal(True)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(6)

        eyebrow = QLabel(f"KURS / {self.kurs.kurs_id:03d}")
        eyebrow.setObjectName("Eyebrow")
        layout.addWidget(eyebrow)

        title = QLabel(self.kurs.kurs_adi)
        title.setObjectName("PageTitle")
        title.setWordWrap(True)
        layout.addWidget(title)

        sub = QLabel(f"{self.kurs.egitmen.ad}  ·  {self.kurs.egitmen.uzmanlik}")
        sub.setObjectName("PageSubtitle")
        layout.addWidget(sub)
        layout.addSpacing(20)

        # Mini istatistikler
        stat_row = QHBoxLayout()
        stat_row.setSpacing(10)
        stat_row.addWidget(self._mini_stat("KAYITLI",
                                           str(len(self.kurs.kayitli_ogrenciler))))
        stat_row.addWidget(self._mini_stat("KONTENJAN", str(self.kurs.kontenjan)))
        stat_row.addWidget(self._mini_stat("DOLULUK",
                                           f"{int(self.kurs.doluluk_yuzdesi())}%"))
        layout.addLayout(stat_row)
        layout.addSpacing(20)

        layout.addWidget(_form_label("KAYITLI ÖĞRENCİLER"))

        if not self.kayitli_ogrenciler:
            empty = QLabel("Henüz kayıtlı öğrenci yok.")
            empty.setStyleSheet(
                f"color: {COLORS['text_muted']}; padding: 24px; "
                f"background-color: {COLORS['bg_card']}; border-radius: 10px;"
            )
            empty.setAlignment(Qt.AlignCenter)
            layout.addWidget(empty, 1)
        else:
            lst = QListWidget()
            for ogr in self.kayitli_ogrenciler:
                lst.addItem(f"#{ogr.ogrenci_id:03d}   {ogr.ad}   ·   {ogr.email}")
            layout.addWidget(lst, 1)

        layout.addSpacing(16)
        btn_kapat = QPushButton("Kapat")
        btn_kapat.setObjectName("GhostButton")
        btn_kapat.setCursor(Qt.PointingHandCursor)
        btn_kapat.clicked.connect(self.accept)
        layout.addWidget(btn_kapat, alignment=Qt.AlignRight)

    def _mini_stat(self, label, value):
        f = QFrame()
        f.setObjectName("StatCard")
        v = QVBoxLayout(f)
        v.setContentsMargins(16, 12, 16, 12)
        v.setSpacing(2)
        l1 = QLabel(label)
        l1.setObjectName("StatLabel")
        l2 = QLabel(value)
        l2.setStyleSheet(
            f"color: {COLORS['text_primary']}; font-size: 22px; "
            f"font-weight: 700; letter-spacing: -1px;"
        )
        v.addWidget(l1)
        v.addWidget(l2)
        return f


class OgrenciDetayDialog(QDialog):
    """Bir öğrencinin kayıtlı olduğu kursları gösterir"""

    def __init__(self, ogrenci, kayitli_kurslar, parent=None):
        super().__init__(parent)
        self.ogrenci = ogrenci
        self.kayitli_kurslar = kayitli_kurslar
        self.setWindowTitle("Öğrenci Detayı")
        self.setMinimumSize(480, 500)
        self.setModal(True)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(6)

        eyebrow = QLabel(f"ÖĞRENCİ / {self.ogrenci.ogrenci_id:03d}")
        eyebrow.setObjectName("Eyebrow")
        layout.addWidget(eyebrow)

        title = QLabel(self.ogrenci.ad)
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        sub = QLabel(self.ogrenci.email)
        sub.setObjectName("PageSubtitle")
        layout.addWidget(sub)
        layout.addSpacing(24)

        layout.addWidget(_form_label(
            f"KAYITLI KURSLAR  ·  {len(self.kayitli_kurslar)}"
        ))

        if not self.kayitli_kurslar:
            empty = QLabel("Henüz hiçbir kursa kayıt yok.")
            empty.setStyleSheet(
                f"color: {COLORS['text_muted']}; padding: 24px; "
                f"background-color: {COLORS['bg_card']}; border-radius: 10px;"
            )
            empty.setAlignment(Qt.AlignCenter)
            layout.addWidget(empty, 1)
        else:
            lst = QListWidget()
            for k in self.kayitli_kurslar:
                lst.addItem(f"KURS-{k.kurs_id:03d}   ·   {k.kurs_adi}   "
                            f"({k.egitmen.ad})")
            layout.addWidget(lst, 1)

        layout.addSpacing(16)
        btn_kapat = QPushButton("Kapat")
        btn_kapat.setObjectName("GhostButton")
        btn_kapat.setCursor(Qt.PointingHandCursor)
        btn_kapat.clicked.connect(self.accept)
        layout.addWidget(btn_kapat, alignment=Qt.AlignRight)
