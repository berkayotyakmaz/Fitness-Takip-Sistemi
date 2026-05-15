"""Modal diyaloglar — sporcu, antrenman, takip, ölçüm formları."""

from datetime import date
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit, QTextEdit,
    QGridLayout, QFormLayout, QWidget, QFrame
)

from .tema import C, F_DISPLAY, F_MONO, F_SANS
from .bilesenler import LimeButton, GhostButton, HBar
from backend.antrenman import MET_TABLOSU


# ═══════════════════════════════════════════════════════════
#  Temel diyalog kabuğu
# ═══════════════════════════════════════════════════════════
class TemelDiyalog(QDialog):
    def __init__(self, kategori: str, baslik: str, parent=None, width: int = 480):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle(baslik)
        self.setMinimumWidth(width)
        self.setStyleSheet(f"""
            QDialog {{ background: {C['bg']}; }}
            QLabel#kategori {{
                color: {C['ink_mute']};
                font-family: '{F_MONO}'; font-size: 10px;
                letter-spacing: 3px;
            }}
            QLabel#baslik {{
                color: {C['ink']};
                font-family: '{F_DISPLAY}';
                font-size: 26px; font-weight: 900;
            }}
            QLabel.formLabel {{
                color: {C['ink_mute']};
                font-family: '{F_MONO}'; font-size: 10px;
                letter-spacing: 2px;
            }}
        """)

        ana = QVBoxLayout(self)
        ana.setContentsMargins(28, 24, 28, 24)
        ana.setSpacing(16)

        # üst başlık
        kat_lbl = QLabel(kategori.upper())
        kat_lbl.setObjectName("kategori")
        ana.addWidget(kat_lbl)
        baslik_lbl = QLabel(baslik)
        baslik_lbl.setObjectName("baslik")
        ana.addWidget(baslik_lbl)
        ana.addWidget(HBar(C['ink'], 2))

        # form alanı
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(12)
        self.form_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.form_layout.setHorizontalSpacing(20)
        ana.addLayout(self.form_layout)

        ana.addStretch()
        ana.addWidget(HBar(C['border_soft'], 1))

        # alt buton barı
        self.alt_bar = QHBoxLayout()
        self.alt_bar.setSpacing(10)
        ana.addLayout(self.alt_bar)
        self.alt_bar.addStretch()

        self.iptal_btn = GhostButton("İptal")
        self.iptal_btn.clicked.connect(self.reject)
        self.alt_bar.addWidget(self.iptal_btn)

    def alan_ekle(self, label: str, widget: QWidget):
        l = QLabel(label.upper())
        l.setProperty("class", "formLabel")
        l.setStyleSheet(
            f"color: {C['ink_mute']}; "
            f"font-family: '{F_MONO}'; font-size: 10px; "
            f"letter-spacing: 2px;"
        )
        self.form_layout.addRow(l, widget)


# ═══════════════════════════════════════════════════════════
#  Sporcu Ekle / Düzenle
# ═══════════════════════════════════════════════════════════
class SporcuDiyalog(TemelDiyalog):
    def __init__(self, parent=None, sporcu=None):
        kategori = "Sporcu" + (" / Düzenle" if sporcu else " / Yeni")
        baslik = "Sporcu Profili" if sporcu else "Yeni Sporcu Kaydı"
        super().__init__(kategori, baslik, parent, width=500)
        self.sporcu = sporcu
        self.sonuc = None

        # alanlar
        self.ad = QLineEdit()
        self.ad.setPlaceholderText("Ad Soyad")
        self.alan_ekle("Ad Soyad", self.ad)

        # kilo + boy yan yana
        kb = QHBoxLayout()
        self.kilo = QDoubleSpinBox()
        self.kilo.setRange(20, 300)
        self.kilo.setSuffix(" kg")
        self.kilo.setDecimals(1)
        self.kilo.setSingleStep(0.5)
        self.kilo.setValue(70.0)
        self.boy = QSpinBox()
        self.boy.setRange(80, 250)
        self.boy.setSuffix(" cm")
        self.boy.setValue(170)
        kb.addWidget(self.kilo)
        kb.addSpacing(8)
        kb.addWidget(self.boy)
        kb_widget = QWidget(); kb_widget.setLayout(kb)
        kb.setContentsMargins(0, 0, 0, 0)
        self.alan_ekle("Kilo / Boy", kb_widget)

        # doğum yılı + cinsiyet yan yana
        dc = QHBoxLayout()
        self.dogum = QSpinBox()
        self.dogum.setRange(1920, date.today().year - 5)
        self.dogum.setValue(2000)
        self.cinsiyet = QComboBox()
        self.cinsiyet.addItems(["erkek", "kadın"])
        dc.addWidget(self.dogum)
        dc.addSpacing(8)
        dc.addWidget(self.cinsiyet)
        dc_widget = QWidget(); dc_widget.setLayout(dc)
        dc.setContentsMargins(0, 0, 0, 0)
        self.alan_ekle("Doğum Yılı / Cinsiyet", dc_widget)

        # hedef kilo
        self.hedef = QDoubleSpinBox()
        self.hedef.setRange(0, 300)
        self.hedef.setSuffix(" kg")
        self.hedef.setDecimals(1)
        self.hedef.setSpecialValueText("— Hedef belirlenmedi")
        self.alan_ekle("Hedef Kilo", self.hedef)

        # mevcut sporcu ise alanları doldur
        if sporcu:
            self.ad.setText(sporcu.ad)
            self.kilo.setValue(sporcu.kilo)
            self.boy.setValue(int(sporcu.boy))
            self.dogum.setValue(sporcu.dogum_yili)
            self.cinsiyet.setCurrentIndex(0 if sporcu.cinsiyet == "erkek" else 1)
            if sporcu.hedef_kilo:
                self.hedef.setValue(sporcu.hedef_kilo)

        # butonlar
        self.kaydet_btn = LimeButton("Kaydet ⇨")
        self.kaydet_btn.clicked.connect(self._kaydet)
        self.alt_bar.addWidget(self.kaydet_btn)

    def _kaydet(self):
        ad = self.ad.text().strip()
        if not ad:
            self.ad.setFocus()
            return
        cins = "erkek" if self.cinsiyet.currentIndex() == 0 else "kadin"
        self.sonuc = {
            "ad": ad,
            "kilo": self.kilo.value(),
            "boy": self.boy.value(),
            "dogum_yili": self.dogum.value(),
            "cinsiyet": cins,
            "hedef_kilo": self.hedef.value() if self.hedef.value() > 0 else None,
        }
        self.accept()


# ═══════════════════════════════════════════════════════════
#  Antrenman Ekle
# ═══════════════════════════════════════════════════════════
class AntrenmanDiyalog(TemelDiyalog):
    def __init__(self, parent=None, sporcu_kilo: float = 70):
        super().__init__("Yeni Antrenman", "Antrenman Kaydı", parent, width=520)
        self.sonuc = None
        self.sporcu_kilo = sporcu_kilo

        self.tur = QComboBox()
        self.tur.addItems(sorted(MET_TABLOSU.keys()))
        self.tur.currentIndexChanged.connect(self._kalori_yenile)
        self.alan_ekle("Antrenman Türü", self.tur)

        self.sure = QSpinBox()
        self.sure.setRange(1, 480)
        self.sure.setSuffix(" dakika")
        self.sure.setValue(30)
        self.sure.valueChanged.connect(self._kalori_yenile)
        self.alan_ekle("Süre", self.sure)

        self.yogunluk = QComboBox()
        self.yogunluk.addItem("Düşük yoğunluk", "dusuk")
        self.yogunluk.addItem("Orta yoğunluk", "orta")
        self.yogunluk.addItem("Yüksek yoğunluk", "yuksek")
        self.yogunluk.setCurrentIndex(1)
        self.yogunluk.currentIndexChanged.connect(self._kalori_yenile)
        self.alan_ekle("Yoğunluk", self.yogunluk)

        self.tarih = QDateEdit()
        self.tarih.setCalendarPopup(True)
        self.tarih.setDate(QDate.currentDate())
        self.tarih.setMaximumDate(QDate.currentDate())
        self.tarih.setDisplayFormat("dd.MM.yyyy")
        self.alan_ekle("Tarih", self.tarih)

        self.notu = QLineEdit()
        self.notu.setPlaceholderText("İsteğe bağlı not")
        self.alan_ekle("Not", self.notu)

        # tahmini kalori önizleme
        self.tahmin_lbl = QLabel()
        self.tahmin_lbl.setStyleSheet(f"""
            background: {C['lime']};
            color: {C['lime_ink']};
            border: 1.5px solid {C['ink']};
            padding: 16px;
            font-family: '{F_DISPLAY}';
            font-size: 18px;
            font-weight: 900;
            letter-spacing: 1px;
        """)
        self.tahmin_lbl.setAlignment(Qt.AlignCenter)
        self.form_layout.addRow(self.tahmin_lbl)
        self._kalori_yenile()

        self.kaydet_btn = LimeButton("Antrenmanı Kaydet ⇨")
        self.kaydet_btn.clicked.connect(self._kaydet)
        self.alt_bar.addWidget(self.kaydet_btn)

    def _kalori_yenile(self):
        from backend.antrenman import MET_TABLOSU, YOGUNLUK_CARPAN
        tur = self.tur.currentText()
        sure = self.sure.value()
        yog = self.yogunluk.currentData()
        met = MET_TABLOSU.get(tur, 6.0)
        carp = YOGUNLUK_CARPAN[yog]
        kcal = int(round(met * carp * 3.5 * self.sporcu_kilo / 200.0 * sure))
        self.tahmin_lbl.setText(f"~ {kcal} KCAL TAHMİNİ")

    def _kaydet(self):
        self.sonuc = {
            "tur": self.tur.currentText(),
            "sure": self.sure.value(),
            "yogunluk": self.yogunluk.currentData(),
            "tarih": self.tarih.date().toString("yyyy-MM-dd"),
            "not_metni": self.notu.text().strip(),
        }
        self.accept()


# ═══════════════════════════════════════════════════════════
#  İlerleme Kaydet — kilo ölçümü
# ═══════════════════════════════════════════════════════════
class IlerlemeDiyalog(TemelDiyalog):
    def __init__(self, parent=None, mevcut_kilo: float = 70):
        super().__init__("İlerleme", "Yeni Tartım Kaydet", parent, width=440)
        self.sonuc = None

        # mevcut kilo gösterimi
        bilgi = QLabel(f"Mevcut: {mevcut_kilo} kg")
        bilgi.setStyleSheet(
            f"color: {C['ink_mute']}; "
            f"font-family: '{F_MONO}'; font-size: 11px; "
            f"letter-spacing: 1.5px;"
        )
        self.form_layout.addRow(bilgi)

        self.yeni_kilo = QDoubleSpinBox()
        self.yeni_kilo.setRange(20, 300)
        self.yeni_kilo.setSuffix(" kg")
        self.yeni_kilo.setDecimals(1)
        self.yeni_kilo.setSingleStep(0.1)
        self.yeni_kilo.setValue(mevcut_kilo)
        self.alan_ekle("Yeni Ölçüm", self.yeni_kilo)

        self.notu = QLineEdit()
        self.notu.setPlaceholderText("Örn: sabah aç karna")
        self.alan_ekle("Not", self.notu)

        self.kaydet_btn = LimeButton("Tartımı Kaydet ⇨")
        self.kaydet_btn.clicked.connect(self._kaydet)
        self.alt_bar.addWidget(self.kaydet_btn)

    def _kaydet(self):
        self.sonuc = {
            "yeni_kilo": self.yeni_kilo.value(),
            "not_metni": self.notu.text().strip(),
        }
        self.accept()


# ═══════════════════════════════════════════════════════════
#  Günlük Takip Kaydı
# ═══════════════════════════════════════════════════════════
class TakipDiyalog(TemelDiyalog):
    def __init__(self, parent=None, mevcut_kayit=None, hedef_kalori: int = 2000):
        super().__init__("Günlük Takip", "Günü Kaydet", parent, width=560)
        self.sonuc = None

        self.tarih = QDateEdit()
        self.tarih.setCalendarPopup(True)
        self.tarih.setDate(QDate.currentDate())
        self.tarih.setMaximumDate(QDate.currentDate())
        self.tarih.setDisplayFormat("dd.MM.yyyy")
        self.alan_ekle("Tarih", self.tarih)

        self.hedef_kalori = QSpinBox()
        self.hedef_kalori.setRange(0, 10000)
        self.hedef_kalori.setSuffix(" kcal")
        self.hedef_kalori.setValue(hedef_kalori)
        self.alan_ekle("Hedef Kalori", self.hedef_kalori)

        self.alinan = QSpinBox()
        self.alinan.setRange(0, 10000)
        self.alinan.setSuffix(" kcal")
        self.alan_ekle("Alınan Kalori", self.alinan)

        self.adim = QSpinBox()
        self.adim.setRange(0, 100000)
        self.adim.setSuffix(" adım")
        self.alan_ekle("Adım Sayısı", self.adim)

        # su + uyku yan yana
        su_uyku = QHBoxLayout()
        self.su = QDoubleSpinBox()
        self.su.setRange(0, 10)
        self.su.setSuffix(" L")
        self.su.setDecimals(1)
        self.su.setSingleStep(0.1)
        self.uyku = QDoubleSpinBox()
        self.uyku.setRange(0, 24)
        self.uyku.setSuffix(" sa")
        self.uyku.setDecimals(1)
        self.uyku.setSingleStep(0.5)
        su_uyku.addWidget(self.su)
        su_uyku.addSpacing(8)
        su_uyku.addWidget(self.uyku)
        wrap = QWidget(); wrap.setLayout(su_uyku)
        su_uyku.setContentsMargins(0, 0, 0, 0)
        self.alan_ekle("Su / Uyku", wrap)

        self.notu = QLineEdit()
        self.notu.setPlaceholderText("Bugünkü genel hisler, gözlemler…")
        self.alan_ekle("Not", self.notu)

        if mevcut_kayit:
            self.tarih.setDate(QDate.fromString(mevcut_kayit.tarih, "yyyy-MM-dd"))
            self.hedef_kalori.setValue(mevcut_kayit.kalori or hedef_kalori)
            self.alinan.setValue(mevcut_kayit.alinan_kalori)
            self.adim.setValue(mevcut_kayit.adim)
            self.su.setValue(mevcut_kayit.su_litre)
            self.uyku.setValue(mevcut_kayit.uyku_saat)
            self.notu.setText(mevcut_kayit.not_metni)

        self.kaydet_btn = LimeButton("Günü Kaydet ⇨")
        self.kaydet_btn.clicked.connect(self._kaydet)
        self.alt_bar.addWidget(self.kaydet_btn)

    def _kaydet(self):
        self.sonuc = {
            "tarih": self.tarih.date().toString("yyyy-MM-dd"),
            "hedef_kalori": self.hedef_kalori.value(),
            "alinan_kalori": self.alinan.value(),
            "adim": self.adim.value(),
            "su_litre": self.su.value(),
            "uyku_saat": self.uyku.value(),
            "not_metni": self.notu.text().strip(),
        }
        self.accept()
