import pytest
from billing import Bill


@pytest.fixture
def bill():
    return Bill()


def test_valid_id_TC01(bill):
    assert bill.verify_id(1) is True


def test_invalid_id_TC02(bill):
    assert bill.verify_id(0) is False
    assert bill.verify_id(-1) is False
    assert bill.verify_id('1') is False


def test_valid_month_TC03(bill):
    assert bill.verify_month('2026-10') is True


def test_invalid_month_TC04(bill):
    assert bill.verify_month('2026-13') is False
    assert bill.verify_month('October') is False
    assert bill.verify_month('') is False


def test_create_bill_TC05(bill):
    deliveries = [
        {'customer_id': 1, 'date': '2026-10-01', 'price': 3.00, 'quantity': 1, 'delivered': True},
        {'customer_id': 1, 'date': '2026-10-02', 'price': 2.50, 'quantity': 2, 'delivered': True},
    ]

    assert bill.create_bill(1, 1, '2026-10', deliveries) is True
    assert bill.getBillId() == 1
    assert bill.getCustomerId() == 1
    assert bill.getMonth() == '2026-10'
    assert bill.getTotal() == 8.00


def test_invalid_bill_TC06(bill):
    assert bill.create_bill(0, 1, '2026-10', []) is False
    assert bill.create_bill(1, 0, '2026-10', []) is False
    assert bill.create_bill(1, 1, '2026-13', []) is False
    assert bill.getBillId() is None


def test_undelivered_items_not_charged_TC07(bill):
    deliveries = [
        {'customer_id': 1, 'date': '2026-10-01', 'price': 3.00, 'quantity': 1, 'delivered': True},
        {'customer_id': 1, 'date': '2026-10-02', 'price': 3.00, 'quantity': 1, 'delivered': False},
    ]

    assert bill.create_bill(1, 1, '2026-10', deliveries) is True
    assert bill.getTotal() == 3.00


def test_other_customers_and_months_TC08(bill):
    deliveries = [
        {'customer_id': 1, 'date': '2026-10-01', 'price': 3.00, 'quantity': 1, 'delivered': True},
        {'customer_id': 2, 'date': '2026-10-01', 'price': 4.00, 'quantity': 1, 'delivered': True},
        {'customer_id': 1, 'date': '2026-09-30', 'price': 5.00, 'quantity': 1, 'delivered': True},
    ]

    assert bill.create_bill(1, 1, '2026-10', deliveries) is True
    assert bill.getTotal() == 3.00


def test_no_deliveries_TC09(bill):
    assert bill.create_bill(1, 1, '2026-10', []) is True
    assert bill.getTotal() == 0
