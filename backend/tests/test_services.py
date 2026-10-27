from decimal import Decimal
from unittest.mock import Mock
import pytest
from app.models import Product
from app.repositories.orders import OrderRepository
from app.repositories.products import ProductRepository
from app.schemas import OrderCreate
from app.services.orders import OrderService, InvalidOrderError


def test_create_order_calculates_total():
    product_repository = Mock(spec=ProductRepository)
    order_repository = Mock(spec=OrderRepository)

    product = {
        1: Product(id=1, name="Notebook", price=Decimal("12.53")),
        2: Product(id=2, name="Pencil", price=Decimal("0.10")),
    }

    product_repository.get_by_id.side_effect = product.get
    order_repository.add.side_effect = lambda order: order

    service = OrderService(
        order_repository,
        product_repository,
    )
    payload = OrderCreate(
        customer_name="Anna",
        customer_email="anna@example.com",
        items=[
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 3},
        ],
    )
    order = service.create_order(payload)

    assert [item.line_total for item in order.items] == [
        Decimal("25.06"),
        Decimal("0.30"),
    ]
    assert order.total == Decimal("25.36")
    order_repository.add.assert_called_once_with(order)


def test_new_order_has_pending_status():
    product_repository = Mock(spec=ProductRepository)
    order_repository = Mock(spec=OrderRepository)

    product_repository.get_by_id.return_value = Product(
        id=1,
        name="Notebook",
        price=Decimal("10.00"),
    )

    order_repository.add.side_effect = lambda order: order

    service = OrderService(
        order_repository,
        product_repository,
    )

    payload = OrderCreate(
        customer_name="Anna",
        customer_email="anna@example.com",
        items=[
            {
                "product_id": 1,
                "quantity": 1,
            }
        ],
    )

    order = service.create_order(payload)
    assert order.status == "pending"


def test_order_item_copies_product_snapshot():
    product_repository = Mock(spec=ProductRepository)
    order_repository = Mock(spec=OrderRepository)

    product = Product(
        id=1,
        name="Notebook",
        price=Decimal("12.53"),
    )

    product_repository.get_by_id.return_value = product
    order_repository.add.side_effect = lambda order: order

    service = OrderService(
        order_repository,
        product_repository,
    )

    payload = OrderCreate(
        customer_name="Anna",
        customer_email="anna@example.com",
        items=[{"product_id": 1, "quantity": 2}],
    )

    order = service.create_order(payload)
    item = order.items[0]

    assert item.product_id == product.id
    assert item.product_name == "Notebook"
    assert item.unit_price == Decimal("12.53")
    assert item.quantity == 2


def test_create_order_rejects_duplicate_products():
    product_repository = Mock(spec=ProductRepository)
    order_repository = Mock(spec=OrderRepository)

    service = OrderService(
        order_repository,
        product_repository,
    )
    payload = OrderCreate(
        customer_name="Anna",
        customer_email="anna@example.com",
        items=[
            {
                "product_id": 1,
                "quantity": 1,
            },
            {
                "product_id": 1,
                "quantity": 2,
            },
        ],
    )
    with pytest.raises(InvalidOrderError):
        service.create_order(payload)

    order_repository.add.assert_not_called()


def test_create_order_rejects_missing_product():
    product_repository = Mock(spec=ProductRepository)
    order_repository = Mock(spec=OrderRepository)

    product_repository.get_by_id.return_value = None

    service = OrderService(
        order_repository,
        product_repository,
    )

    payload = OrderCreate(
        customer_name="Anna",
        customer_email="anna@example.com",
        items=[
            {
                "product_id": 999,
                "quantity": 1,
            }
        ],
    )

    with pytest.raises(InvalidOrderError):
        service.create_order(payload)

    order_repository.add.assert_not_called()
