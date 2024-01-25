import pytest
from src.crm.handlers.OrderResponseHandler import OrderResponseHandler


@pytest.fixture
def response_handler():
    return OrderResponseHandler()


def test_upload_method(response_handler):
    # Подготовим мок-объект для response
    response_mock = {
        'delivery': {'address': {'date': '2024-01-20', 'time': '12:00'}},
        'phone': '123456789',
        'lastName': 'Doe',
        'firstName': 'John',
        'patronymic': 'Smith',
        'number': 'ORD123',
        'id': '12345',
        'items': [{'offer': {'name': 'Product1'}, 'quantity': 2}],
        'totalSumm': '100.00',
        'customerComment': 'Customer comment',
        'managerComment': 'Manager comment'
    }

    # Вызываем метод upload с мок-ответом
    response_handler.upload(response=response_mock)

    # Проверяем, что методы получения атрибутов вызваны корректно
    assert response_handler.order_number == 'ORD123'
    assert response_handler.id == '12345'
    assert response_handler.delivery_address == {'date': '2024-01-20', 'time': '12:00'}
    assert response_handler.phone == '123456789'
    assert response_handler.customer_full_name == 'Doe John Smith'
    assert response_handler.products == [{'name': 'Product1', 'quantity': 2}]
    assert response_handler.total_summ == '100.00'
    assert response_handler.customer_comment == 'Customer comment'
    assert response_handler.manager_comment == 'Manager comment'


def test_dump_method(response_handler):
    # Подготовим мок-ответ
    response_handler.response = {'key': 'value'}
    response_handler.test = {'key': 'value'}

    # Вызываем метод dump
    result = response_handler.dump()

    # Проверяем, что метод вызван корректно и возвращаемый результат соответствует ожидаемому
    assert result == {'test': {'key': 'value'}}


def test_str_method(response_handler):
    # Подготовим мок-ответ и вызовем метод upload
    response_mock = {'number': 'ORD789', 'delivery': {'address': 'Test Address'}}
    response_handler.upload(response=response_mock)

    # Вызываем метод str и проверяем результат
    result = str(response_handler)
    assert result == 'Заказ № ORD789 по адресу Test Address.  None'

