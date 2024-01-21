from src.loger import logger


class OrderResponseHandler:
    def upload(self, response: dict = None):
        if response:
            self.response = response
            self.id = self._get_order_id()
            self.order_number = self._get_order_number()
            self.delivery_datetime = self._get_delivery_datetime()
            self.delivery_address = self._get_delivery()
            self.phone = self._get_phone()
            self.customer_full_name = self._get_customer_full_name()
            self.products = self._get_products()
            self.customer_comment = self._get_customer_comment()
            self.manager_comment = self._get_manager_comment()
            self.total_summ = self._get_total_summ()

    def dump(self):
        attributes = vars(self)
        attributes.pop('response')
        logger.debug(f'{attributes = }')
        return attributes

    def _get_delivery(self) -> dict:
        value_delivery = self.response.get('delivery', {})
        return value_delivery.get('address', {})

    def _get_phone(self) -> str:
        return self.response.get('phone')

    def _get_customer_full_name(self) -> str:
        temp_list = list()
        temp_list.append(self.response.get("lastName"))
        temp_list.append(self.response.get("firstName"))
        temp_list.append(self.response.get("patronymic"))
        self.customer_full_name = ' '.join([i for i in temp_list if i])

        return self.customer_full_name

    def _get_order_number(self) -> str:
        return self.response.get('number')

    def _get_order_id(self) -> str:
        return self.response.get('id')

    def _get_delivery_datetime(self) -> dict:
        return {'date': self.response.get('delivery').get('date'), 'time': self.response.get('delivery').get('time')}

    def _get_products(self) -> list:
        self.products = list()
        if self.response.get('items'):
            for product in self.response.get('items'):
                self.products.append({
                    'name': product.get('offer').get('name'),
                    'quantity': product.get('quantity'),
                })
        return self.products

    def _get_total_summ(self) -> str:
        return self.response.get('totalSumm')

    def _get_customer_comment(self) -> str:
        return self.response.get('customerComment')

    def _get_manager_comment(self) -> str:
        return self.response.get('managerComment')

    def __str__(self) -> str:
        return f'Заказ № {self.order_number} по адресу {self.delivery_address}. {self.customer_full_name} {self.phone}'
