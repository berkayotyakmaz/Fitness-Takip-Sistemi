"""
main.py
-------
Online Kurs Platformu - giriş noktası.

Çalıştırma:
    pip install PyQt5
    cd kurs_platformu
    python main.py
"""

import os
import sys

# Bu dosyanın bulunduğu klasörü import path'ine ekle.
# Böylece nereden çalıştırılırsa çalıştırılsın `backend` ve `frontend`
# paketleri bulunur.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from backend import PlatformService
from frontend import MainWindow


def main():
    # Yüksek DPI desteği
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))

    # data klasörünü proje kökünde garantile (cwd ne olursa olsun)
    data_dir = os.path.join(PROJECT_ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    data_path = os.path.join(data_dir, "platform.json")

    service = PlatformService(data_path=data_path)
    window = MainWindow(service)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
