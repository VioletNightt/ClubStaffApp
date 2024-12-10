from PyQt6.QtWidgets import (
    QLineEdit, QDialog, QFormLayout, QDialogButtonBox
)


class AddStaffDialog(QDialog):
    """Диалоговое окно для добавления нового сотрудника."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить нового сотрудника")

        self.layout = QFormLayout(self)
        self.login_field = QLineEdit(self)
        self.email_field = QLineEdit(self)
        self.phone_field = QLineEdit(self)
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)

        self.layout.addRow("Логин:", self.login_field)
        self.layout.addRow("Email:", self.email_field)
        self.layout.addRow("Телефон:", self.phone_field)
        self.layout.addRow("Пароль:", self.password_field)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        self.layout.addRow(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_data(self):
        """Возвращает данные, введенные в диалоге."""
        return {
            "login": self.login_field.text(),
            "email": self.email_field.text(),
            "phone": self.phone_field.text(),
            "password": self.password_field.text()
        }