from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QMessageBox

class AddMenuItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить блюдо")

        self.layout = QVBoxLayout(self)

        self.name_label = QLabel("Название блюда:")
        self.layout.addWidget(self.name_label)
        self.name_input = QLineEdit(self)
        self.layout.addWidget(self.name_input)

        self.price_label = QLabel("Цена блюда:")
        self.layout.addWidget(self.price_label)
        self.price_input = QLineEdit(self)
        self.price_input.setPlaceholderText("Введите цену (только цифры)")
        self.layout.addWidget(self.price_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_data(self):
        """Возвращает введенные данные."""
        return {
            "name": self.name_input.text().strip(),
            "price": self.price_input.text().strip(),
        }

    def accept(self):
        """Обрабатывает нажатие кнопки "ОК"."""
        name = self.name_input.text().strip()
        price = self.price_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Название блюда не может быть пустым.")
            return

        if not price.isdigit():
            QMessageBox.warning(self, "Ошибка", "Цена должна быть числом.")
            return

        super().accept()
