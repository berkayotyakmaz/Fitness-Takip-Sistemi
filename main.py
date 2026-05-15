"""
Fitness Takip Sistemi
=====================
Proje 7 - PyQt5 ile sporcu, antrenman ve takip yönetimi.

Çalıştırmak için:
    python main.py

Demo veri yüklenmesi için:
    python main.py --seed
"""
import sys
from pathlib import Path

# Paket yolu
sys.path.insert(0, str(Path(__file__).parent))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from backend.veri_yoneticisi import VeriYoneticisi
from backend.seed import seed
from frontend.ana_pencere import AnaPencere
from frontend.tema import app_qss, F_SANS


def main() -> int:
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    uygulama = QApplication(sys.argv)
    uygulama.setApplicationName("PULSE - Fitness Takip Sistemi")
    uygulama.setFont(QFont(F_SANS, 10))
    uygulama.setStyleSheet(app_qss())

    # Veri yöneticisi
    veri_dizini = Path(__file__).parent / "data"
    veri_dizini.mkdir(exist_ok=True)
    yonetici = VeriYoneticisi(str(veri_dizini))

    # İlk çalıştırmada veya --seed parametresiyle demo veri yükle
    seed_iste = "--seed" in sys.argv
    if seed_iste or not yonetici.sporcular:
        seed(yonetici)

    pencere = AnaPencere(yonetici)
    pencere.show()

    return uygulama.exec_()


if __name__ == "__main__":
    sys.exit(main())
