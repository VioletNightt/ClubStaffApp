from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout


class AddComputerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить компьютер")
        self.setFixedSize(300, 150)

        self.name_field = QLineEdit(self)
        self.name_field.setPlaceholderText("Введите название компьютера")

        self.config_field = QLineEdit(self)
        self.config_field.setPlaceholderText("Введите конфигурацию компьютера")

        self.ok_button = QPushButton("ОК", self)
        self.cancel_button = QPushButton("Отмена", self)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.name_field)
        layout.addWidget(QLabel("Конфигурация:"))
        layout.addWidget(self.config_field)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_data(self):
        """Возвращает введённые данные."""
        return {
            "name": self.name_field.text().strip(),
            "configuration": self.config_field.text().strip(),
        }
