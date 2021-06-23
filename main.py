import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from controller.main_window import MainWindow

if __name__ == '__main__':
    current_exit_code = MainWindow.EXIT_CODE_REBOOT
    while current_exit_code == MainWindow.EXIT_CODE_REBOOT:
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        current_exit_code = app.exec_()
        app = None
