from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QDialog, QInputDialog
)
from PyQt6.QtCore import QTimer

from ui.add_menu_dialog import AddMenuItemDialog


class MenuManagementWidget(QWidget):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.setLayout(QVBoxLayout())

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Цена", "Действие"])
        self.layout().addWidget(self.table)

        self.add_dish_button = QPushButton("Добавить блюдо")
        self.add_dish_button.clicked.connect(self.add_menu_item)
        self.layout().addWidget(self.add_dish_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_menu)
        self.timer.start(10000)

        self.menu_items = []

    def showEvent(self, event):
        """Событие, вызываемое при открытии виджета."""
        super().showEvent(event)
        self.load_menu()

    def hideEvent(self, event):
        """Событие, вызываемое при закрытии виджета."""
        super().hideEvent(event)
        self.timer.stop()

    def load_menu(self):
        """Загружает меню через BusinessLogic и обновляет таблицу."""
        try:
            self.menu_items = self.business_logic.get_menu()
            self.populate_table(self.menu_items)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки меню: {e}")

    def populate_table(self, menu_items):
        """Заполняет таблицу меню."""
        self.table.setRowCount(len(menu_items))
        for row, item in enumerate(menu_items):
            self.table.setItem(row, 0, QTableWidgetItem(str(item["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(f'{item["price"]:.2f} руб.'))

            edit_button = QPushButton("Изменить цену")
            edit_button.clicked.connect(lambda _, i_id=item["id"]: self.edit_price(i_id))

            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(lambda _, i_id=item["id"]: self.delete_dish(i_id))

            button_layout = QVBoxLayout()
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)

            button_widget = QWidget()
            button_widget.setLayout(button_layout)
            self.table.setCellWidget(row, 3, button_widget)

            self.table.setRowHeight(row, 80)

        self.table.resizeColumnsToContents()

    def edit_price(self, item_id):
        """Изменяет цену блюда."""
        current_price = next((item["price"] for item in self.menu_items if item["id"] == item_id), 0)
        new_price, ok = QInputDialog.getDouble(
            self, "Изменить цену", "Введите новую цену:",
            value=current_price, min=0.0, decimals=2
        )
        if not ok or new_price == current_price:
            return

        try:
            self.business_logic.update_menu_price(item_id, new_price)
            QMessageBox.information(self, "Успех", "Цена успешно обновлена.")
            self.load_menu()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить цену: {e}")

    def delete_dish(self, item_id):
        """Удаляет блюдо из меню."""
        reply = QMessageBox.question(
            self, "Удаление блюда", "Вы уверены, что хотите удалить это блюдо?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.business_logic.delete_menu_item(item_id)
                QMessageBox.information(self, "Успех", "Блюдо успешно удалено.")
                self.load_menu()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить блюдо: {e}")

    def add_menu_item(self):
        """Открывает диалог для добавления нового блюда."""
        dialog = AddMenuItemDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            name = data["name"]
            price = data["price"]

            try:
                self.business_logic.add_menu_item(name, float(price))
                QMessageBox.information(self, "Успех", "Блюдо успешно добавлено.")
                self.load_menu()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить блюдо: {e}")
