"""
styles.py
---------
Uygulamanın görsel kimliği. Koyu, editorial, modern.
Renk paleti: deep navy + warm cream + electric lime aksiyon
"""

# Renk paleti
COLORS = {
    "bg_primary":   "#0E1116",   # Ana arka plan - neredeyse siyah
    "bg_panel":     "#161A22",   # Yan paneller
    "bg_card":      "#1C2129",   # Kartlar
    "bg_card_hover":"#232934",
    "border":       "#2A2F3A",
    "border_soft":  "#1F242E",
    "text_primary": "#F4EFE6",   # Krem beyaz - yumuşak
    "text_muted":   "#7A8290",
    "text_dim":     "#4D5563",
    "accent":       "#C8FF4B",   # Electric lime
    "accent_dim":   "#9BC93C",
    "accent_soft":  "#3B4A1C",   # Lime'ın koyu hafif tonu - badge için
    "danger":       "#FF6B6B",
    "warning":      "#FFB454",
    "success":      "#7DD87B",
}

QSS = f"""
/* ============ GLOBAL ============ */
QWidget {{
    background-color: {COLORS['bg_primary']};
    color: {COLORS['text_primary']};
    font-family: "Segoe UI", "Inter", "Helvetica Neue", sans-serif;
    font-size: 13px;
}}

QMainWindow {{
    background-color: {COLORS['bg_primary']};
}}

/* ============ SIDEBAR ============ */
#Sidebar {{
    background-color: {COLORS['bg_panel']};
    border-right: 1px solid {COLORS['border_soft']};
}}

#BrandLabel {{
    color: {COLORS['text_primary']};
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.5px;
    padding: 0px;
}}

#BrandSubtitle {{
    color: {COLORS['text_muted']};
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 600;
}}

#NavButton {{
    background-color: transparent;
    color: {COLORS['text_muted']};
    border: none;
    border-radius: 10px;
    padding: 11px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
}}
#NavButton:hover {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
}}
#NavButton:checked {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['accent']};
    font-weight: 600;
    border-left: 3px solid {COLORS['accent']};
    padding-left: 13px;
}}

#SidebarSection {{
    color: {COLORS['text_dim']};
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 700;
    padding: 4px 16px;
}}

/* ============ HEADER ============ */
#PageTitle {{
    color: {COLORS['text_primary']};
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -1px;
}}

#PageSubtitle {{
    color: {COLORS['text_muted']};
    font-size: 13px;
    letter-spacing: 0.2px;
}}

#Eyebrow {{
    color: {COLORS['accent']};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
}}

/* ============ STAT KARTI ============ */
#StatCard {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 14px;
}}
QFrame#StatCardHero {{
    background-color: {COLORS['accent']};
    border: 1px solid {COLORS['accent']};
    border-radius: 14px;
}}
QFrame#StatCardHero QLabel {{
    background-color: transparent;
}}

QLabel#StatValue {{
    color: {COLORS['text_primary']};
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -1.5px;
    background-color: transparent;
}}
QLabel#StatValueHero {{
    color: {COLORS['bg_primary']};
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -1.5px;
    background-color: transparent;
}}
QLabel#StatLabel {{
    color: {COLORS['text_muted']};
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    background-color: transparent;
}}
QLabel#StatLabelHero {{
    color: {COLORS['bg_primary']};
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    background-color: transparent;
}}

/* ============ KURS / ÖĞRENCİ KARTI ============ */
#ItemCard {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 14px;
}}
#ItemCard:hover {{
    background-color: {COLORS['bg_card_hover']};
    border: 1px solid {COLORS['accent_dim']};
}}

#CardTitle {{
    color: {COLORS['text_primary']};
    font-size: 16px;
    font-weight: 700;
    letter-spacing: -0.3px;
}}
#CardMeta {{
    color: {COLORS['text_muted']};
    font-size: 12px;
}}

#CardId {{
    color: {COLORS['accent']};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    background-color: {COLORS['accent_soft']};
    border: 1px solid {COLORS['accent_dim']};
    border-radius: 4px;
    padding: 3px 8px;
}}

/* ============ BUTONLAR ============ */
QPushButton {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 9px 16px;
    font-weight: 500;
    font-size: 13px;
    text-align: center;
}}
QPushButton:hover {{
    background-color: {COLORS['bg_card_hover']};
    border: 1px solid {COLORS['text_dim']};
}}
QPushButton:pressed {{
    background-color: {COLORS['border']};
}}

QPushButton#PrimaryButton {{
    background-color: {COLORS['accent']};
    color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['accent']};
    font-weight: 700;
    padding: 10px 20px;
    min-width: 60px;
}}
QPushButton#PrimaryButton:hover {{
    background-color: {COLORS['accent_dim']};
    border: 1px solid {COLORS['accent_dim']};
}}
QPushButton#PrimaryButton:pressed {{
    background-color: {COLORS['accent_dim']};
}}

QPushButton#DangerButton {{
    background-color: transparent;
    color: {COLORS['danger']};
    border: 1px solid {COLORS['border']};
}}
QPushButton#DangerButton:hover {{
    background-color: {COLORS['danger']};
    color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['danger']};
}}

QPushButton#GhostButton {{
    background-color: transparent;
    color: {COLORS['text_muted']};
    border: 1px solid {COLORS['border']};
}}
QPushButton#GhostButton:hover {{
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['text_dim']};
}}

/* ============ INPUTLAR ============ */
QLineEdit, QSpinBox, QComboBox {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    selection-background-color: {COLORS['accent']};
    selection-color: {COLORS['bg_primary']};
}}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border: 1px solid {COLORS['accent']};
    background-color: {COLORS['bg_panel']};
}}
QLineEdit::placeholder {{
    color: {COLORS['text_dim']};
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox::down-arrow {{
    width: 0;
    height: 0;
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_panel']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    selection-background-color: {COLORS['accent_soft']};
    selection-color: {COLORS['accent']};
    padding: 4px;
    outline: 0;
}}

QSpinBox::up-button, QSpinBox::down-button {{
    background-color: {COLORS['border']};
    border: none;
    width: 18px;
    border-radius: 4px;
    margin: 2px;
}}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
    background-color: {COLORS['accent_dim']};
}}
QSpinBox::up-arrow {{ width: 0; height: 0; }}
QSpinBox::down-arrow {{ width: 0; height: 0; }}

/* ============ LABELLAR ============ */
#FormLabel {{
    color: {COLORS['text_muted']};
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}

#SectionTitle {{
    color: {COLORS['text_primary']};
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.5px;
}}

/* ============ PROGRESS / DOLULUK ============ */
QProgressBar {{
    background-color: {COLORS['border_soft']};
    border: none;
    border-radius: 3px;
    height: 6px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    background-color: {COLORS['accent']};
    border-radius: 3px;
}}

/* ============ SCROLLBAR ============ */
QScrollArea {{
    background-color: transparent;
    border: none;
}}
QScrollBar:vertical {{
    background-color: transparent;
    width: 10px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 5px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['text_dim']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background-color: transparent;
    height: 10px;
}}
QScrollBar::handle:horizontal {{
    background-color: {COLORS['border']};
    border-radius: 5px;
}}

/* ============ DIALOG ============ */
QDialog {{
    background-color: {COLORS['bg_panel']};
}}

/* ============ MESAJ KUTUSU ============ */
QMessageBox {{
    background-color: {COLORS['bg_panel']};
}}
QMessageBox QLabel {{
    color: {COLORS['text_primary']};
    font-size: 13px;
}}
QMessageBox QPushButton {{
    min-width: 80px;
}}

/* ============ LIST ============ */
QListWidget {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    padding: 6px;
    outline: 0;
}}
QListWidget::item {{
    background-color: transparent;
    border-radius: 6px;
    padding: 8px 10px;
    margin: 2px 0;
    color: {COLORS['text_primary']};
}}
QListWidget::item:hover {{
    background-color: {COLORS['bg_card_hover']};
}}
QListWidget::item:selected {{
    background-color: {COLORS['accent_soft']};
    color: {COLORS['accent']};
}}

/* ============ TOOLTIP ============ */
QToolTip {{
    background-color: {COLORS['bg_panel']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 6px 10px;
}}
"""
