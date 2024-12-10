from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QWidget, QMessageBox


class AuthWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Авторизация")
        self.setFixedSize(300, 130)

        self.login_field = QLineEdit(self)
        self.login_field.setPlaceholderText("Логин")

        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Пароль")
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Войти", self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.login_field)
        self.layout.addWidget(self.password_field)
        self.layout.addWidget(self.login_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        """Обрабатывает вход пользователя."""
        login = self.login_field.text()
        password = self.password_field.text()

        if not all([login, password]):
            self.show_error("Заполните все поля.")
            return

        try:
            result = self.controller.business_logic.authenticate_user(login, password)
            if result["success"]:
                self.controller.show_main_window()
            else:
                self.show_error(result.get("error", "Ошибка авторизации."))
        except Exception as e:
            self.show_error(str(e))

    def show_error(self, message):
        """Показывает сообщение об ошибке."""
        QMessageBox.warning(self, "Ошибка", message)
