"""
Yeniden kullanılabilir bileşenler.
Aesthetic: kalın siyah çizgiler, lime accent, büyük rakamlar.
"""

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QPen, QColor, QBrush, QPolygonF
from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtWidgets import (
    QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QSizePolicy
)

from .tema import C, F_DISPLAY, F_MONO, F_SANS


# ═══════════════════════════════════════════════════════════
#  Yatay ve dikey ayraç çizgisi
# ═══════════════════════════════════════════════════════════
class HBar(QFrame):
    def __init__(self, color: str = None, height: int = 1, parent=None):
        super().__init__(parent)
        self.setFixedHeight(height)
        self.setStyleSheet(f"background: {color or C['border']};")


class VBar(QFrame):
    def __init__(self, color: str = None, width: int = 1, parent=None):
        super().__init__(parent)
        self.setFixedWidth(width)
        self.setStyleSheet(f"background: {color or C['border']};")


# ═══════════════════════════════════════════════════════════
#  Section başlığı — küçük etiket + büyük başlık
# ═══════════════════════════════════════════════════════════
class SectionHeader(QWidget):
    def __init__(self, kategori: str, baslik: str, sayac: str = "", parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(2)

        # üst etiket — monospace küçük
        et = QLabel(kategori.upper())
        et.setStyleSheet(
            f"color: {C['ink_mute']}; "
            f"font-family: '{F_MONO}'; font-size: 10px; "
            f"letter-spacing: 3px;"
        )
        lay.addWidget(et)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)
        baslik_lbl = QLabel(baslik)
        baslik_lbl.setStyleSheet(
            f"color: {C['ink']}; "
            f"font-family: '{F_DISPLAY}'; "
            f"font-size: 28px; font-weight: 900;"
        )
        row.addWidget(baslik_lbl)
        if sayac:
            sc = QLabel(f"[ {sayac} ]")
            sc.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
            sc.setStyleSheet(
                f"color: {C['ink_mute']}; "
                f"font-family: '{F_MONO}'; font-size: 12px; "
                f"padding-bottom: 4px;"
            )
            row.addWidget(sc)
        row.addStretch()
        lay.addLayout(row)


# ═══════════════════════════════════════════════════════════
#  Büyük metrik — etiket + ÇOK büyük rakam + birim
# ═══════════════════════════════════════════════════════════
class BigMetric(QWidget):
    def __init__(self, etiket: str, deger: str, birim: str = "",
                 vurgu: bool = False, parent=None):
        super().__init__(parent)
        self.deger_lbl: QLabel
        self.birim_lbl: QLabel
        self._build(etiket, deger, birim, vurgu)

    def _build(self, etiket, deger, birim, vurgu):
        renk_deger = C['lime_ink'] if vurgu else C['ink']
        renk_etiket = C['lime_ink'] if vurgu else C['ink_mute']

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        et = QLabel(etiket.upper())
        et.setStyleSheet(
            f"color: {renk_etiket}; "
            f"font-family: '{F_MONO}'; font-size: 10px; "
            f"letter-spacing: 2px;"
        )
        lay.addWidget(et)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        row.setAlignment(Qt.AlignBottom)

        self.deger_lbl = QLabel(str(deger))
        self.deger_lbl.setStyleSheet(
            f"color: {renk_deger}; "
            f"font-family: '{F_DISPLAY}'; "
            f"font-size: 42px; font-weight: 900; "
            f"line-height: 1;"
        )
        row.addWidget(self.deger_lbl)
        if birim:
            self.birim_lbl = QLabel(birim)
            self.birim_lbl.setAlignment(Qt.AlignBottom)
            self.birim_lbl.setStyleSheet(
                f"color: {renk_deger}; "
                f"font-family: '{F_MONO}'; font-size: 12px; "
                f"padding-bottom: 8px; letter-spacing: 1px;"
            )
            row.addWidget(self.birim_lbl)
        else:
            self.birim_lbl = QLabel("")
        row.addStretch()
        lay.addLayout(row)

    def degeri_guncelle(self, yeni_deger: str, yeni_birim: str = None):
        self.deger_lbl.setText(str(yeni_deger))
        if yeni_birim is not None:
            self.birim_lbl.setText(yeni_birim)


# ═══════════════════════════════════════════════════════════
#  Küçük metrik — ufak alanlar için
# ═══════════════════════════════════════════════════════════
class SmallMetric(QWidget):
    def __init__(self, etiket: str, deger: str, birim: str = "",
                 inverted: bool = False, parent=None):
        super().__init__(parent)
        renk_text = C['ink_inv'] if inverted else C['ink']
        renk_mute = C['ink_inv_mut'] if inverted else C['ink_mute']

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(2)

        et = QLabel(etiket.upper())
        et.setStyleSheet(
            f"color: {renk_mute}; "
            f"font-family: '{F_MONO}'; font-size: 9px; letter-spacing: 2px;"
        )
        lay.addWidget(et)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(4)
        row.setAlignment(Qt.AlignBottom)
        self.deger_lbl = QLabel(str(deger))
        self.deger_lbl.setStyleSheet(
            f"color: {renk_text}; "
            f"font-family: '{F_DISPLAY}'; "
            f"font-size: 22px; font-weight: 900;"
        )
        row.addWidget(self.deger_lbl)
        if birim:
            bl = QLabel(birim)
            bl.setAlignment(Qt.AlignBottom)
            bl.setStyleSheet(
                f"color: {renk_mute}; "
                f"font-family: '{F_MONO}'; font-size: 10px; "
                f"padding-bottom: 4px;"
            )
            row.addWidget(bl)
        row.addStretch()
        lay.addLayout(row)

    def degeri_guncelle(self, yeni_deger: str):
        self.deger_lbl.setText(str(yeni_deger))


# ═══════════════════════════════════════════════════════════
#  Lime Accent Buton — vurgulu CTA butonu
# ═══════════════════════════════════════════════════════════
class LimeButton(QPushButton):
    def __init__(self, text: str, parent=None):
        super().__init__(text.upper(), parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: {C['lime']};
                color: {C['lime_ink']};
                border: 1.5px solid {C['ink']};
                padding: 12px 22px;
                font-size: 12px;
                font-weight: 900;
                letter-spacing: 1.5px;
            }}
            QPushButton:hover {{
                background: {C['ink']};
                color: {C['lime']};
            }}
            QPushButton:pressed {{
                background: {C['ink']};
                color: {C['lime_dark']};
            }}
            QPushButton:disabled {{
                background: {C['bg_alt']};
                color: {C['ink_mute']};
                border-color: {C['border_soft']};
            }}
        """)


class GhostButton(QPushButton):
    """Çerçeveli (transparent) buton."""

    def __init__(self, text: str, danger: bool = False,
                 inverted: bool = False, parent=None):
        super().__init__(text.upper(), parent)
        self.setCursor(Qt.PointingHandCursor)
        if danger:
            border, color = C['danger'], C['danger']
            hover_bg, hover_text = C['danger'], "#FFFFFF"
        elif inverted:
            border, color = C['ink_inv'], C['ink_inv']
            hover_bg, hover_text = C['lime'], C['lime_ink']
        else:
            border, color = C['ink'], C['ink']
            hover_bg, hover_text = C['ink'], C['bg']

        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {color};
                border: 1.5px solid {border};
                padding: 10px 18px;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1.5px;
            }}
            QPushButton:hover {{
                background: {hover_bg};
                color: {hover_text};
            }}
            QPushButton:disabled {{
                color: {C['ink_mute']};
                border-color: {C['border_soft']};
            }}
        """)


# ═══════════════════════════════════════════════════════════
#  Nav Item — sol panel için seçilebilir nav
# ═══════════════════════════════════════════════════════════
class NavItem(QPushButton):
    def __init__(self, num: str, label: str, parent=None):
        super().__init__(parent)
        self.num = num
        self.label = label
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(f"  {num}    {label.upper()}")
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {C['ink_inv_mut']};
                border: 0;
                border-left: 3px solid transparent;
                padding: 14px 16px;
                font-family: '{F_SANS}';
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 2px;
                text-align: left;
            }}
            QPushButton:hover {{
                color: {C['ink_inv']};
                border-left: 3px solid {C['ink_inv_mut']};
            }}
            QPushButton:checked {{
                color: {C['lime']};
                border-left: 3px solid {C['lime']};
                background: rgba(198, 255, 61, 0.06);
            }}
        """)


# ═══════════════════════════════════════════════════════════
#  Renkli rozet (chip) — yoğunluk, kategori vs
# ═══════════════════════════════════════════════════════════
class Rozet(QLabel):
    PRESETS = {
        "lime":   (C['lime'],     C['lime_ink']),
        "ink":    (C['ink'],      C['bg']),
        "soft":   (C['bg_alt'],   C['ink']),
        "ok":     (C['ok'],       "#FFFFFF"),
        "warn":   (C['warn'],     "#FFFFFF"),
        "danger": (C['danger'],   "#FFFFFF"),
        "outline":("transparent", C['ink']),
    }

    def __init__(self, text: str, varyant: str = "ink", parent=None):
        super().__init__(text.upper(), parent)
        bg, fg = self.PRESETS.get(varyant, self.PRESETS["ink"])
        border = C['ink'] if varyant == "outline" else bg
        self.setStyleSheet(
            f"background: {bg}; color: {fg}; "
            f"border: 1px solid {border}; "
            f"padding: 3px 8px; "
            f"font-family: '{F_MONO}'; font-size: 9px; "
            f"font-weight: bold; letter-spacing: 1.5px;"
        )
        self.setAlignment(Qt.AlignCenter)


# ═══════════════════════════════════════════════════════════
#  Bar Grafik — haftalık kalori dağılımı için
# ═══════════════════════════════════════════════════════════
class BarChart(QWidget):
    """Basit bar chart — Qt paint ile çizilir."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.veri = []  # list[(label, value)]
        self.maks = 0
        self.setMinimumHeight(160)

    def veri_ayarla(self, veri: list):
        self.veri = veri
        self.maks = max([v for _, v in veri], default=0) or 1
        self.update()

    def paintEvent(self, ev):
        if not self.veri:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, False)

        w = self.width()
        h = self.height()
        n = len(self.veri)
        margin = 8
        bar_alani_h = h - 30  # alt etiket alanı için

        bar_genislik = (w - margin * 2) / n - 6
        bar_genislik = max(bar_genislik, 8)

        for i, (lbl, v) in enumerate(self.veri):
            x = margin + i * ((w - margin * 2) / n) + 3
            bar_h = (v / self.maks) * (bar_alani_h - 10) if self.maks else 0
            y = bar_alani_h - bar_h

            # bar
            renk = QColor(C['lime']) if v == self.maks else QColor(C['ink'])
            p.fillRect(QRectF(x, y, bar_genislik, bar_h), renk)

            # değer üstte (eğer yer varsa)
            if v > 0:
                p.setPen(QPen(QColor(C['ink']), 1))
                f = QFont(F_MONO, 8, QFont.Bold)
                p.setFont(f)
                p.drawText(
                    QRectF(x - 4, y - 16, bar_genislik + 8, 14),
                    Qt.AlignCenter, str(v)
                )

            # etiket altta
            p.setPen(QPen(QColor(C['ink_mute']), 1))
            p.setFont(QFont(F_MONO, 8))
            p.drawText(
                QRectF(x - 4, bar_alani_h + 4, bar_genislik + 8, 18),
                Qt.AlignCenter, lbl
            )

        # alt çizgi
        p.setPen(QPen(QColor(C['ink']), 1.5))
        p.drawLine(margin, bar_alani_h, w - margin, bar_alani_h)


# ═══════════════════════════════════════════════════════════
#  Spark Line — kilo değişim çizgisi
# ═══════════════════════════════════════════════════════════
class SparkLine(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.values = []  # list[float]
        self.labels = []
        self.setMinimumHeight(120)

    def veri_ayarla(self, values: list, labels: list = None):
        self.values = values
        self.labels = labels or [""] * len(values)
        self.update()

    def paintEvent(self, ev):
        if len(self.values) < 1:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        w, h = self.width(), self.height()
        margin = 18
        plot_w = w - margin * 2
        plot_h = h - margin * 2

        if len(self.values) == 1:
            # tek nokta
            x = margin + plot_w / 2
            y = margin + plot_h / 2
            p.setBrush(QBrush(QColor(C['ink'])))
            p.setPen(Qt.NoPen)
            p.drawEllipse(QPointF(x, y), 5, 5)
            return

        mn = min(self.values)
        mx = max(self.values)
        rng = (mx - mn) or 1.0

        pts = []
        for i, v in enumerate(self.values):
            x = margin + (i / (len(self.values) - 1)) * plot_w
            y = margin + (1 - (v - mn) / rng) * plot_h
            pts.append(QPointF(x, y))

        # zemin lime dolgu
        poly = QPolygonF(pts)
        poly.append(QPointF(pts[-1].x(), margin + plot_h))
        poly.append(QPointF(pts[0].x(), margin + plot_h))
        p.setBrush(QBrush(QColor(198, 255, 61, 60)))
        p.setPen(Qt.NoPen)
        p.drawPolygon(poly)

        # çizgi
        p.setPen(QPen(QColor(C['ink']), 2))
        for i in range(len(pts) - 1):
            p.drawLine(pts[i], pts[i + 1])

        # noktalar
        for pt in pts:
            p.setBrush(QBrush(QColor(C['lime'])))
            p.setPen(QPen(QColor(C['ink']), 1.5))
            p.drawEllipse(pt, 4, 4)

        # min/max label
        p.setPen(QPen(QColor(C['ink_mute']), 1))
        p.setFont(QFont(F_MONO, 8))
        p.drawText(QRectF(0, 2, w, 12), Qt.AlignRight, f"max {mx}")
        p.drawText(QRectF(0, h - 14, w, 12), Qt.AlignRight, f"min {mn}")


# ═══════════════════════════════════════════════════════════
#  Yatay ilerleme çubuğu
# ═══════════════════════════════════════════════════════════
class Ilerleme(QWidget):
    def __init__(self, etiket: str, deger: int, hedef: int,
                 birim: str = "", inverted: bool = False, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.etiket = etiket
        self.deger = deger
        self.hedef = hedef
        self.birim = birim
        self.inverted = inverted

    def guncelle(self, deger: int, hedef: int):
        self.deger = deger
        self.hedef = hedef
        self.update()

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, False)
        w, h = self.width(), self.height()

        text_color = QColor(C['ink_inv'] if self.inverted else C['ink'])
        mute_color = QColor(C['ink_inv_mut'] if self.inverted else C['ink_mute'])
        track_color = QColor("#2A2A2A" if self.inverted else C['border_soft'])
        fill_color = QColor(C['lime'])

        # etiket
        p.setPen(QPen(mute_color))
        p.setFont(QFont(F_MONO, 9, QFont.Bold))
        p.drawText(QRectF(0, 0, w, 14), Qt.AlignLeft, self.etiket.upper())

        # değer
        deger_txt = f"{self.deger}{self.birim} / {self.hedef}{self.birim}"
        p.setPen(QPen(text_color))
        p.drawText(QRectF(0, 0, w, 14), Qt.AlignRight, deger_txt)

        # bar track
        bar_y = 22
        bar_h = 8
        p.fillRect(QRectF(0, bar_y, w, bar_h), track_color)

        # bar fill
        oran = min(self.deger / self.hedef, 1.0) if self.hedef else 0
        p.fillRect(QRectF(0, bar_y, w * oran, bar_h), fill_color)

        # yüzde
        yuzde = int(oran * 100)
        p.setPen(QPen(mute_color))
        p.setFont(QFont(F_MONO, 8))
        p.drawText(QRectF(0, bar_y + bar_h + 2, w, 14),
                   Qt.AlignLeft, f"{yuzde}% TAMAMLANDI")
