"""
Frontend tema ve stil paleti
─────────────────────────────────────────────────────────
Aesthetic: "Athletic Performance Lab"
- Krem/kağıt zemin
- Mürekkep siyahı text
- Lime/electric green accent
- Düz köşeler, kalın tipografi
"""

# ═══════════════════════════════════════════════════════════
#  RENKLER
# ═══════════════════════════════════════════════════════════
C = {
    # zemin
    "bg":          "#F5F4EE",   # krem kağıt
    "bg_alt":      "#EDECE5",   # biraz koyu
    "panel":       "#FFFFFF",   # beyaz panel
    "panel_alt":   "#0A0A0A",   # siyah panel (sol profil)

    # text
    "ink":         "#0A0A0A",   # mürekkep siyah
    "ink_soft":    "#3A3A38",
    "ink_mute":    "#7C7B73",
    "ink_inv":     "#F5F4EE",   # ters (siyah panel üstünde)
    "ink_inv_mut": "#A8A6A0",

    # accent
    "lime":        "#C6FF3D",   # ana vurgu — electric green
    "lime_dark":   "#9FD12E",
    "lime_ink":    "#1A2A00",   # lime üstüne yazı

    # state
    "ok":          "#1F8A4C",
    "warn":        "#D4811C",
    "danger":      "#C0392B",

    # grafik / data
    "data_1":      "#0A0A0A",
    "data_2":      "#C6FF3D",
    "data_3":      "#7C7B73",

    # çizgi
    "border":      "#1A1A1A",
    "border_soft": "#D8D6CD",
    "grid":        "#E8E6DD",
}


# ═══════════════════════════════════════════════════════════
#  FONT — JetBrains Mono + Inter alternatifi yok, sistem fontuna düşeriz
#  Qt'da tarayıcı gibi font dosyası yüklemek mümkün ama bağımlılığı azaltıyorum.
#  Tasarım: Display = ağır weight + condensed, Body = sans, Mono = stat'lar.
# ═══════════════════════════════════════════════════════════
F_DISPLAY = "Arial Black"          # tüm sistemlerde var, Bold weight'i agresif
F_SANS    = "Helvetica"            # mac+linux+win'de mevcut
F_MONO    = "Courier New"          # bütün sistemlerde var


# ═══════════════════════════════════════════════════════════
#  GLOBAL STYLESHEET
# ═══════════════════════════════════════════════════════════
def app_qss() -> str:
    return f"""
    * {{
        font-family: "{F_SANS}", "Segoe UI", sans-serif;
        font-size: 13px;
        color: {C['ink']};
        outline: 0;
    }}

    QMainWindow, QWidget#Root {{
        background: {C['bg']};
    }}

    /* ── Tooltips ── */
    QToolTip {{
        background: {C['ink']};
        color: {C['bg']};
        border: 1px solid {C['ink']};
        padding: 6px 9px;
        font-size: 11px;
    }}

    /* ── ScrollBar — minimal, ince ── */
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {C['ink_mute']};
        min-height: 30px;
        border-radius: 0;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {C['ink']};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 8px;
    }}
    QScrollBar::handle:horizontal {{
        background: {C['ink_mute']};
        min-width: 30px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {C['ink']};
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
    }}

    /* ── Inputs ── */
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit, QTextEdit {{
        background: {C['panel']};
        border: 1.5px solid {C['border']};
        padding: 9px 11px;
        font-size: 13px;
        color: {C['ink']};
        selection-background-color: {C['lime']};
        selection-color: {C['lime_ink']};
    }}
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
    QComboBox:focus, QDateEdit:focus, QTextEdit:focus {{
        border: 2px solid {C['ink']};
    }}
    QLineEdit:disabled, QSpinBox:disabled {{
        background: {C['bg_alt']};
        color: {C['ink_mute']};
    }}

    QSpinBox::up-button, QSpinBox::down-button,
    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
        width: 0; height: 0; border: 0;
    }}

    QComboBox::drop-down {{
        border: 0;
        width: 24px;
    }}
    QComboBox::down-arrow {{
        image: none;
        width: 0; height: 0;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid {C['ink']};
        margin-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background: {C['panel']};
        border: 1.5px solid {C['border']};
        selection-background-color: {C['lime']};
        selection-color: {C['lime_ink']};
        padding: 4px;
    }}

    QDateEdit::drop-down {{ border: 0; width: 0; }}

    /* ── Tablo ── */
    QTableWidget {{
        background: {C['panel']};
        border: 1.5px solid {C['border']};
        gridline-color: {C['border_soft']};
        font-size: 12px;
    }}
    QTableWidget::item {{
        padding: 10px 12px;
        border-bottom: 1px solid {C['border_soft']};
        color: {C['ink']};
    }}
    QTableWidget::item:selected {{
        background: {C['lime']};
        color: {C['lime_ink']};
    }}
    QHeaderView::section {{
        background: {C['ink']};
        color: {C['bg']};
        padding: 9px 12px;
        border: 0;
        font-size: 10px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    QTableWidget QTableCornerButton::section {{
        background: {C['ink']};
        border: 0;
    }}

    /* ── Mesaj kutuları ── */
    QMessageBox {{
        background: {C['panel']};
    }}
    QMessageBox QLabel {{
        color: {C['ink']};
        font-size: 13px;
    }}

    /* ── Genel buton (default) ── */
    QPushButton {{
        background: {C['ink']};
        color: {C['bg']};
        border: 1.5px solid {C['ink']};
        padding: 10px 18px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    QPushButton:hover {{
        background: {C['lime']};
        color: {C['lime_ink']};
        border-color: {C['ink']};
    }}
    QPushButton:pressed {{
        background: {C['lime_dark']};
    }}
    QPushButton:disabled {{
        background: {C['bg_alt']};
        color: {C['ink_mute']};
        border-color: {C['border_soft']};
    }}
    """
