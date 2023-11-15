from crm.handlers.OrderResponseHandler import OrderResponseHandler
from retailcrm import v5 as retailcrm
from pprint import pprint
from settings import STATUS_ORDER_COMPLETE

from settings import STATUS_DELIVERY_KAZAN, CRM_URL, CRM_TOKEN
from loger import loger


class CrmService:
    def __init__(self, client: retailcrm):
        self.client = client

    def orders(self, delivery_date):
        filters = {'extendedStatus': STATUS_DELIVERY_KAZAN}
        if delivery_date:
            filters.update({'deliveryDateFrom': delivery_date, 'deliveryDateTo': delivery_date})
        loger.debug(f"Отправляем запрос: client.orders({filters=})")
        response = self.client.orders(filters=filters).get_response()
        loger.debug(f'Получили ответ {response = }')

        orders = response.get('orders')
        list_orders = list()
        for item in orders:
            order = OrderResponseHandler(item)
            list_orders.append(order.dump())
        loger.debug(f'Список заказов готов: {list_orders = }')
        return list_orders

    def order_completed(self, pk: str) -> bool:
        response = self.client.order_edit(order={'id': pk, 'status': STATUS_ORDER_COMPLETE}, uid_type='id')
        return response.get_response().get('success')


if __name__ == '__main__':
    cl = retailcrm(crm_url=CRM_URL, api_key=CRM_TOKEN)
    service = CrmService(cl)
    pprint(service.orders())
