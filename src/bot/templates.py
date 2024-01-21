from datetime import datetime
from src.loger import logger


def order_template(order: dict, ) -> str:
    logger.debug(f'Подготовка вида заказа №{order.get("order_number")} с атрибутами: {order}')
    try:

        text = f'<b>🛒 Заказ № {order.get("order_number", "")}</b>\n'

        if order.get('delivery_datetime').get('date'):
            text += f'Дата доставки: {datetime.strptime(order.get("delivery_datetime").get("date"), "%Y-%m-%d").strftime("%d.%m.%Y")}\n'
        else:
            text += f'Дата доставки: <em>Не указано</em> \n'

        if order.get("delivery_datetime").get("time"):
            text += (f'Время доставки: c {order.get("delivery_datetime").get("time").get("from")} '
                     f'до {order.get("delivery_datetime").get("time").get("to")}\n')
        else:
            text += f'Время доставки: <em>Не указано</em> \n'

        address = join_address(order.get('delivery_address', {}))
        text += (
            f'<a href="https://yandex.ru/maps/?text={address.replace(" ", "")}&rtt=auto">{address}</a>\n'
            f'{order.get("phone", "")}\n'
            f'{order.get("customer_full_name", "")}\n\n'
        )

        if order.get("customer_comment"):
            text += f'{"Клиент: " + order.get("customer_comment")}\n'
        if order.get("manager_comment"):
            text += f'{"Оператор: " + order.get("manager_comment")}\n'

        text += 'Состав заказа:\n'
        for product in order.get('products'):
            text += f'➡ {product.get("name")} - {product.get("quantity")}\n'

        text += f'Итоговая сумма: {order.get("total_summ")} ₽'
        logger.debug(f'Подготовка вида заказа №{order.get("order_number")} успешно завершена. {text = }')
        return text
    except Exception as _ex:
        logger.error(f'Не удалось подготовить вид заказа №{order.get("order_number")}. {_ex}', exc_info=True)
        return f'Не удалось отобразить заказ № {order.get("order_number")}'


def join_address(address_dict: dict) -> str:
    address_keys = {'region': '', 'city': '', 'streetType': '', 'street': '', 'building': 'д. ',
                    'flat': 'кв./офиса ', 'floor': 'этаж ', 'block': 'подъезд ', 'house': 'строение ',
                    'housing': 'корпус: ', 'notes': 'Примечания к адресу: '}
    text = ' '.join([v + address_dict.get(k) for k, v in address_keys.items() if address_dict.get(k)])
    return text
