from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer, Qt


def get_next_status(current_status):
    """Возвращает следующий статус заказа."""
    status_transitions = {
        "paid": "preparing",
        "preparing": "ready",
        "ready": "delivered",
    }
    return status_transitions.get(current_status)


class OrderManagementWidget(QWidget):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.setLayout(QVBoxLayout())

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Клиент", "Состав", "Статус", "Действие"])
        self.layout().addWidget(self.table)

        self.orders = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_orders)

    def showEvent(self, event):
        """Событие, вызываемое при открытии виджета."""
        super().showEvent(event)
        self.load_orders()
        self.timer.start(10000)

    def hideEvent(self, event):
        """Событие, вызываемое при закрытии виджета."""
        super().hideEvent(event)
        self.timer.stop()

    def load_orders(self):
        """Загружает список заказов через BusinessLogic и обновляет таблицу."""
        try:
            self.orders = self.business_logic.get_pending_orders()
            self.populate_table(self.orders)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки заказов: {e}")

    def populate_table(self, orders):
        """Заполняет таблицу заказов."""
        self.table.setRowCount(len(orders))
        for row, order in enumerate(orders):
            self.table.setItem(row, 0, QTableWidgetItem(str(order["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(order["user_id"])))

            items = "\n".join([f"{item['name']} - {item['quantity']} шт." for item in order["items"]])
            self.table.setItem(row, 2, QTableWidgetItem(items))

            status_item = QTableWidgetItem(order["status"])
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, status_item)

            next_status = get_next_status(order["status"])
            if next_status:
                change_status_button = QPushButton(f"Перевести в {next_status}")
                change_status_button.clicked.connect(lambda _, o_id=order["id"], ns=next_status: self.change_order_status(o_id, ns))
                self.table.setCellWidget(row, 4, change_status_button)
            else:
                self.table.setItem(row, 4, QTableWidgetItem(""))

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def change_order_status(self, order_id, new_status):
        """Изменяет статус заказа."""
        try:
            self.business_logic.update_order_status(order_id, new_status)
            QMessageBox.information(self, "Успех", f"Статус заказа #{order_id} обновлен до '{new_status}'.")
            self.load_orders()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить статус заказа: {e}")
