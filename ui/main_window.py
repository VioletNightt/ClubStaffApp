from PyQt6.QtWidgets import QMainWindow, QListWidget, QStackedWidget, QHBoxLayout, QWidget, QLabel

from ui.computer_window import ComputerManagementWidget
from ui.menu_window import MenuManagementWidget
from ui.order_window import OrderManagementWidget
from ui.staff_window import StaffWidget
from ui.statictic_computer_window import ComputerUsageStatisticsWidget
from ui.statistic_menu_window import FoodStatisticsWidget


class MainWindow(QMainWindow):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.setWindowTitle("Панель управления")
        self.resize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        self.menu_list = QListWidget()
        self.content_stack = QStackedWidget()

        self.menu_list.addItem("Сотрудники")
        self.menu_list.addItem("Компьютеры")
        self.menu_list.addItem("Заказы")
        self.menu_list.addItem("Меню")
        self.menu_list.addItem("Статистика заказов")
        self.menu_list.addItem("Статистика использования компьютеров")
        self.menu_list.addItem("Выход")
        self.menu_list.setMaximumWidth(300)

        self.menu_list.currentRowChanged.connect(self.switch_view)

        self.staff_widget = StaffWidget(self.business_logic)
        self.computers_widget = ComputerManagementWidget(self.business_logic)
        self.orders_widget = OrderManagementWidget(self.business_logic)
        self.menu_widget = MenuManagementWidget(self.business_logic)
        self.order_stats_widget = FoodStatisticsWidget(self.business_logic)
        self.computer_usage_stats_widget = ComputerUsageStatisticsWidget(self.business_logic)

        self.content_stack.addWidget(self.staff_widget)
        self.content_stack.addWidget(self.computers_widget)
        self.content_stack.addWidget(self.orders_widget)
        self.content_stack.addWidget(self.menu_widget)
        self.content_stack.addWidget(self.order_stats_widget)
        self.content_stack.addWidget(self.computer_usage_stats_widget)

        layout.addWidget(self.menu_list)
        layout.addWidget(self.content_stack)

    def switch_view(self, index):
        if index == 6:
            self.close()
        else:
            self.content_stack.setCurrentIndex(index)
