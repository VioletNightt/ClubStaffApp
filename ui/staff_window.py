from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QInputDialog
)

from functools import partial

from ui.add_staff_dialog import AddStaffDialog


class StaffWidget(QWidget):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.setLayout(QVBoxLayout())

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Email", "Телефон", "Действие"])
        self.layout().addWidget(self.table)

        self.add_button = QPushButton("Добавить сотрудника", self)
        self.add_button.clicked.connect(self.open_add_staff_dialog)
        self.layout().addWidget(self.add_button)

    def showEvent(self, event):
        """Событие, вызываемое при отображении виджета."""
        super().showEvent(event)
        self.load_staffs()

    def load_staffs(self):
        """Загружает список сотрудников через BusinessLogic и обновляет таблицу."""
        try:
            staffs = self.business_logic.get_staffs()
            self.populate_table(staffs)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки списка сотрудников: {e}")

    def populate_table(self, staffs):
        """Заполняет таблицу данными сотрудников."""
        self.table.setRowCount(len(staffs))
        for row, staff in enumerate(staffs):
            self.table.setItem(row, 0, QTableWidgetItem(str(staff["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(staff["login"]))
            self.table.setItem(row, 2, QTableWidgetItem(staff["email"]))
            self.table.setItem(row, 3, QTableWidgetItem(staff["phone"]))

            if self.business_logic.is_my_login(staff["login"]):
                button = QPushButton("Сменить пароль", self)
                button.clicked.connect(partial(self.change_password, staff["id"]))
            else:
                button = QPushButton("Удалить", self)
                button.clicked.connect(partial(self.delete_staff, staff["id"]))
            self.table.setCellWidget(row, 4, button)

        self.table.resizeColumnsToContents()

    def open_add_staff_dialog(self):
        """Открывает диалог для добавления нового сотрудника."""
        dialog = AddStaffDialog()
        if dialog.exec():
            data = dialog.get_data()
            try:
                result = self.business_logic.add_staff(data)
                if result["success"]:
                    QMessageBox.information(self, "Успех", result["message"])
                    self.load_staffs()
                else:
                    QMessageBox.critical(self, "Ошибка", result["error"])
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении сотрудника: {e}")

    def delete_staff(self, staff_id):
        """Удаляет сотрудника."""
        confirm = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить сотрудника?")
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                result = self.business_logic.delete_staff(staff_id)
                if result["success"]:
                    QMessageBox.information(self, "Успех", result["message"])
                    self.load_staffs()
                else:
                    QMessageBox.critical(self, "Ошибка", result["error"])
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении сотрудника: {e}")

    def change_password(self, staff_id):
        """Изменяет пароль для текущего пользователя."""
        new_password, ok = QInputDialog.getText(self, "Смена пароля", "Введите новый пароль:", QLineEdit.EchoMode.Password)
        if ok and new_password:
            try:
                result = self.business_logic.change_password(staff_id, new_password)
                if result["success"]:
                    QMessageBox.information(self, "Успех", "Пароль успешно изменен.")
                else:
                    QMessageBox.critical(self, "Ошибка", result["error"])
            except Exception as e:
                print(e)
                QMessageBox.critical(self, "Ошибка", f"Ошибка при смене пароля: {e}")