import pytest
from unittest.mock import Mock, patch
from src.crm.CrmService import CrmService, STATUS_DELIVERY_KAZAN, STATUS_ORDER_COMPLETE


@pytest.fixture
def crm_service():
    retailcrm_mock = Mock()
    order_handler = Mock()
    crm = CrmService(client=retailcrm_mock, order_handler=order_handler)
    return crm


def test_orders_with_delivery_date(crm_service):
    delivery_date = '2024-01-20'
    expected_filters = {'extendedStatus': STATUS_DELIVERY_KAZAN, 'deliveryDateFrom': delivery_date,
                        'deliveryDateTo': delivery_date}

    with patch.object(crm_service.client, 'orders') as orders_mock:
        crm_service.client.return_value.get_response.return_value = {'success': True,
                                                              'pagination': {'limit': 20, 'totalCount': 0,
                                                                             'currentPage': 1, 'totalPageCount': 0},
                                                              'orders': []}
        result = crm_service.orders(delivery_date=delivery_date)

        crm_service.client.orders.return_value.get_response.assert_called_once()
        crm_service.client.orders.assert_called_once_with(filters=expected_filters)
        assert result == []


def test_order_completed(crm_service):
    pk = '123'
    expected_order_edit = {'id': pk, 'status': STATUS_ORDER_COMPLETE}

    with patch.object(crm_service.client, 'order_edit') as order_edit_mock:
        order_edit_mock.return_value.get_response.return_value = {'success': True}
        result = crm_service.order_completed(pk=pk)

    order_edit_mock.assert_called_once_with(order=expected_order_edit, uid_type='id')
    assert result is True
