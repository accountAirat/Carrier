from src.crm.CrmService import CrmService


class Controller:
    def __init__(self, service: CrmService):
        self.service = service

    def orders(self, delivery_date):
        return self.service.orders(delivery_date)

    def order_completed(self, pk: str) -> bool:
        return self.service.order_completed(pk)
