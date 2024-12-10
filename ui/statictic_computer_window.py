from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QTableWidget, QMessageBox, QTableWidgetItem


class ComputerUsageStatisticsWidget(QWidget):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.setLayout(QVBoxLayout())

        self.period_filter = QComboBox()
        self.period_filter.addItems(["За текущий день", "За текущий месяц", "За текущий год"])
        self.layout().addWidget(self.period_filter)

        self.load_button = QPushButton("Загрузить")
        self.load_button.clicked.connect(self.load_statistics)
        self.layout().addWidget(self.load_button)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Компьютер", "Количество аренд", "Общее время аренды (часов)"])
        self.layout().addWidget(self.table)

    def load_statistics(self):
        """Загружает статистику использования компьютеров."""
        period_map = {"За текущий день": "day", "За текущий месяц": "month", "За текущий год": "year"}
        selected_period = self.period_filter.currentText()
        period = period_map[selected_period]

        try:
            stats = self.business_logic.get_computer_usage_statistics(period)
            self.populate_table(stats)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить статистику: {e}")

    def populate_table(self, stats):
        """Заполняет таблицу статистики."""
        self.table.setRowCount(len(stats))
        for row, stat in enumerate(stats):
            self.table.setItem(row, 0, QTableWidgetItem(stat["computer_name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(stat["rental_count"])))
            self.table.setItem(row, 2, QTableWidgetItem(f"{stat['total_rental_hours']:.2f}"))
        self.table.resizeColumnsToContents()