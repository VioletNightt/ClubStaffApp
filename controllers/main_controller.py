from PyQt6.QtWidgets import QApplication
from ui.auth_window import AuthWindow
from ui.main_window import MainWindow
from logic.business_logic import BusinessLogic
from logic.network_layer import NetworkLayer
import sys


class MainController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.network_layer = NetworkLayer()
        self.business_logic = BusinessLogic(self.network_layer)
        self.auth_window = AuthWindow(self)
        self.main_window = MainWindow(self.business_logic)

    def show_auth_window(self):
        """Показывает окно авторизации."""
        self.main_window.hide()
        self.auth_window.show()

    def show_main_window(self):
        """Показывает главное окно после успешного входа."""
        self.auth_window.hide()
        self.main_window.show()

    def run(self):
        """Запуск приложения."""
        self.auth_window.show()
        sys.exit(self.app.exec())
