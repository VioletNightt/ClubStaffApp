from datetime import datetime, timedelta


class BusinessLogic:
    def __init__(self, network_layer):
        self.network_layer = network_layer
        self.token = None
        self.user_role = None
        self.token_expiry = None
        self.login = None
        self.password = None

    def authenticate_user(self, login, password):
        if not self.login or not self.password:
            self.login = login
            self.password = password
        response = self.network_layer.post(
            "/auth/login",
            json={"login_or_email": login, "password": password}
        )
        if response["status"] == 200:
            self.token = response["data"]["access_token"]
            self.token_expiry = datetime.now() + timedelta(minutes=30)
            self.user_role = response["data"]["role"]
            self.network_layer.set_token(self.token)
            return {"success": True}
        return {"success": False, "error": response["detail"]}

    def refresh_token(self):
        """Перезапрашивает токен, используя сохраненные учетные данные."""
        if not self.login or not self.password:
            raise Exception("Необходим повторный вход: учетные данные отсутствуют.")

        if self.is_token_expired:
            self.authenticate_user(self.login, self.password)

    def is_token_expired(self):
        """Проверяет, истек ли токен."""
        return self.token_expiry is None or datetime.now() > self.token_expiry - timedelta(seconds=60)

    def is_my_login(self, login):
        return self.login == login

    def get_staffs(self):
        """Получает список сотрудников."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.get("/users/staffs", headers=headers)
        if response["status"] == 200:
            return response["data"]
        else:
            raise Exception(response["detail"])

    def add_staff(self, data):
        """Добавляет нового сотрудника."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.post("/users/register", headers=headers, json=data)
        if response["status"] == 200:
            return {"success": True, "message": "Сотрудник успешно добавлен."}
        else:
            return {"success": False, "error": response["detail"]}

    def delete_staff(self, staff_id):
        """Удаляет сотрудника."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.delete(f"/users/{staff_id}", headers=headers)
        if response["status"] == 200:
            return {"success": True, "message": "Сотрудник успешно удален."}
        else:
            return {"success": False, "error": response["detail"]}

    def change_password(self, staff_id, new_password):
        """Меняет пароль для текущего пользователя."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.put(f"/users/{staff_id}/password", headers=headers,
                                          json={"password": new_password})
        if response["status"] == 200:
            self.password = new_password
            return {"success": True}
        else:
            return {"success": False, "error": response["detail"]}

    def get_computers(self):
        """Получает список компьютеров."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.get("/computers", headers=headers)
        if response["status"] == 200:
            return response["data"]
        else:
            raise Exception(response["detail"])

    def add_computer(self, name, configuration):
        """Добавляет новый компьютер"""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.post("/computers", headers=headers,
                                           json={"name": name, "configuration": configuration})
        if response["status"] != 200:
            raise Exception(response["detail"])

    def delete_computer(self, computer_id):
        """Удаляет компьютер"""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.delete(f"/computers/{computer_id}", headers=headers)
        if response["status"] != 200:
            raise Exception(response["detail"])

    def update_computer_configuration(self, computer_id, configuration):
        """Изменяет конфигурацию компьютера"""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.put(f"/computers/{computer_id}", headers=headers,
                                          json={"configuration": configuration})
        if response["status"] != 200:
            raise Exception(response["detail"])

    def get_pending_orders(self):
        """Получает список незавершенных заказов."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.get("/orders/pending", headers=headers)
        print(response)
        if response["status"] == 200:
            return response["data"]
        raise Exception(response["detail"])

    def update_order_status(self, order_id, new_status):
        """Обновляет статус заказа."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.put(f"/orders/{order_id}/status", headers=headers,
                                          params={"new_status": new_status})
        if response["status"] != 200:
            raise Exception(response["detail"])

    def get_menu(self):
        """Получает список всех блюд в меню."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.get("/menu", headers=headers)
        if response["status"] == 200:
            return response["data"]
        else:
            raise Exception(response["detail"])

    def add_menu_item(self, name, price):
        """Добавляет новое блюдо в меню."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.post("/menu", headers=headers, json={"name": name, "price": price})
        if response["status"] != 200:
            raise Exception(response["detail"])

    def update_menu_price(self, item_id, new_price):
        """Обновляет цену существующего блюда."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.put(
            f"/menu/{item_id}/price", headers=headers, params={"new_price": new_price}
        )
        if response["status"] != 200:
            raise Exception(response["detail"])

    def delete_menu_item(self, item_id):
        """Удаляет блюдо из меню."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.delete(f"/menu/{item_id}", headers=headers)
        if response["status"] != 200:
            raise Exception(response["detail"])

    def get_computer_usage_statistics(self, period):
        """Получает статистику использования компьютеров."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.get(f"/statistics/computer_usage", headers=headers, params={"period": period})
        if response["status"] == 200:
            return response["data"]
        else:
            raise Exception(response["detail"])

    def get_food_statistics(self, period):
        """Получает статистику заказов еды."""
        self.refresh_token()
        headers = self.network_layer.get_headers()
        response = self.network_layer.get(f"/statistics/food_statistics", headers=headers, params={"period": period})
        if response["status"] == 200:
            return response["data"]
        else:
            raise Exception(response["detail"])