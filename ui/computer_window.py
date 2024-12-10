from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QDialog, \
    QInputDialog
from datetime import datetime, timedelta

from ui.add_computer_dialog import AddComputerDialog


def calculate_remaining_time(rental_end_time):
    """Вычисляет оставшееся время аренды."""
    end_time = datetime.strptime(rental_end_time, "%Y-%m-%dT%H:%M:%S.%f")
    remaining_time = end_time - datetime.now()
    return max(remaining_time, timedelta(seconds=0))


def format_remaining_time(remaining_time):
    """Форматирует оставшееся время аренды."""
    minutes, seconds = divmod(remaining_time.total_seconds(), 60)
    return f"{int(minutes)} мин {int(seconds)} сек"


class ComputerManagementWidget(QWidget):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.setLayout(QVBoxLayout())

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Конфигурация", "Статус/Действие"])
        self.layout().addWidget(self.table)

        self.add_computer_button = QPushButton("Добавить компьютер")
        self.add_computer_button.clicked.connect(self.add_computer)
        self.layout().addWidget(self.add_computer_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rental_timers)
        self.timer.start(1000)

        self.computers = []

    def showEvent(self, event):
        """Загружается данные при открытии виджета."""
        super().showEvent(event)
        self.load_computers()

    def hideEvent(self, event):
        """Событие скрытия виджета."""
        super().hideEvent(event)
        self.timer.stop()

    def load_computers(self):
        """Загружает список компьютеров через BusinessLogic и обновляет таблицу."""
        try:
            self.computers = self.business_logic.get_computers()
            self.populate_table()
        except Exception as e:
            print(f"Ошибка загрузки компьютеров: {e}")

    def update_rental_timers(self):
        """Обновляет таблицу с компьютерами каждые N секунд."""
        self.load_computers()

    def populate_table(self):
        """Заполняет таблицу компьютеров."""
        self.table.setRowCount(len(self.computers))
        for row, computer in enumerate(self.computers):
            self.table.setItem(row, 0, QTableWidgetItem(str(computer["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(computer["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(computer["configuration"]))

            if computer["status"] == "rented" and computer["rental_end_time"]:
                remaining_time = calculate_remaining_time(computer["rental_end_time"])
                if remaining_time.total_seconds() > 0:
                    countdown_label = QTableWidgetItem(format_remaining_time(remaining_time))
                    self.table.setItem(row, 3, countdown_label)
                    self.start_countdown(row, computer["rental_end_time"])
                else:
                    self.table.setItem(row, 3, QTableWidgetItem("Аренда завершена"))
            else:
                edit_button = QPushButton("Редактировать")
                edit_button.clicked.connect(lambda _, c_id=computer["id"]: self.edit_computer(c_id))
                delete_button = QPushButton("Удалить")
                delete_button.clicked.connect(lambda _, c_id=computer["id"]: self.delete_computer(c_id))

                button_layout = QVBoxLayout()
                button_layout.addWidget(edit_button)
                button_layout.addWidget(delete_button)

                button_widget = QWidget()
                button_widget.setLayout(button_layout)
                self.table.setCellWidget(row, 3, button_widget)

            self.table.setRowHeight(row, 80)

        self.table.resizeColumnsToContents()

    def start_countdown(self, row, rental_end_time):
        """Запускает обратный отсчет для отображения времени аренды."""
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.update_countdown(row, rental_end_time))
        timer.start(1000)

    def update_countdown(self, row, rental_end_time):
        """Обновляет оставшееся время аренды."""
        remaining_time = calculate_remaining_time(rental_end_time)
        if remaining_time.total_seconds() > 0:
            self.table.item(row, 3).setText(format_remaining_time(remaining_time))
        else:
            self.table.item(row, 3).setText("Аренда завершена")

    def add_computer(self):
        """Открывает диалог для добавления компьютера."""
        dialog = AddComputerDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            name = data["name"]
            configuration = data["configuration"]

            if not name or not configuration:
                QMessageBox.warning(self, "Ошибка", "Название и конфигурация компьютера не могут быть пустыми.")
                return

            try:
                self.business_logic.add_computer(name, configuration)
                QMessageBox.information(self, "Успех", "Компьютер успешно добавлен.")
                self.load_computers()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить компьютер: {e}")

    def edit_computer(self, computer_id):
        """Редактирует конфигурацию компьютера."""
        current_computer = next((c for c in self.computers if c["id"] == computer_id), None)
        if not current_computer:
            QMessageBox.critical(self, "Ошибка", "Компьютер не найден.")
            return

        new_configuration, ok = QInputDialog.getText(
            self, "Редактировать компьютер",
            "Введите новую конфигурацию:",
            text=current_computer["configuration"]
        )
        if ok and new_configuration.strip():
            try:
                self.business_logic.update_computer_configuration(computer_id, new_configuration.strip())
                QMessageBox.information(self, "Успех", "Конфигурация компьютера успешно обновлена.")
                self.load_computers()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось обновить конфигурацию: {e}")

    def delete_computer(self, computer_id):
        """Удаляет компьютер."""
        reply = QMessageBox.question(
            self, "Удаление компьютера",
            "Вы уверены, что хотите удалить этот компьютер?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.business_logic.delete_computer(computer_id)
                QMessageBox.information(self, "Успех", "Компьютер успешно удален.")
                self.load_computers()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить компьютер: {e}")
