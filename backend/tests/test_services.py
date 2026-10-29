from decimal import Decimal
from unittest.mock import Mock
import pytest
from app.models import Product
from app.repositories.orders import OrderRepository
from app.repositories.products import ProductRepository
from app.schemas import OrderCreate, ProductCreate, ProductUpdate
from app.services.orders import OrderService, InvalidOrderError
from app.services.products import ProductService, ProductAlreadyExistsError


@pytest.fixture
def product_repository():
    return Mock(spec=ProductRepository)


@pytest.fixture
def order_repository():
    repository = Mock(spec=OrderRepository)
    repository.add.side_effect = lambda order: order
    return repository


@pytest.fixture
def service(order_repository, product_repository):
    return OrderService(
        order_repository,
        product_repository,
    )


@pytest.fixture
def product_service(product_repository):
    return ProductService(product_repository)


def make_order(items):
    return OrderCreate(
        customer_name="Anna", customer_email="anna@example.com", items=items
    )


def test_create_order_calculates_total(service, product_repository, order_repository):
    product = {
        1: Product(id=1, name="Notebook", price=Decimal("12.53")),
        2: Product(id=2, name="Pencil", price=Decimal("0.10")),
    }
    product_repository.get_by_id.side_effect = product.get
    payload = make_order(
        [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 3},
        ]
    )
    order = service.create_order(payload)

    assert [item.line_total for item in order.items] == [
        Decimal("25.06"),
        Decimal("0.30"),
    ]
    assert order.total == Decimal("25.36")
    order_repository.add.assert_called_once_with(order)


def test_new_order_has_pending_status(service, product_repository):
    product_repository.get_by_id.return_value = Product(
        id=1,
        name="Notebook",
        price=Decimal("10.00"),
    )
    payload = make_order(
        [
            {"product_id": 1, "quantity": 1},
        ]
    )
    order = service.create_order(payload)
    assert order.status == "pending"


def test_order_item_copies_product_snapshot(
    service, product_repository, order_repository
):
    product = Product(
        id=1,
        name="Notebook",
        price=Decimal("12.53"),
    )
    product_repository.get_by_id.return_value = product
    payload = make_order(
        [{"product_id": 1, "quantity": 2}],
    )
    order = service.create_order(payload)
    item = order.items[0]

    assert item.product_id == product.id
    assert item.product_name == "Notebook"
    assert item.unit_price == Decimal("12.53")
    assert item.quantity == 2


def test_create_order_rejects_duplicate_products(service, order_repository):
    payload = make_order(
        [
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


def test_create_order_rejects_missing_product(
    service, product_repository, order_repository
):
    product_repository.get_by_id.return_value = None
    payload = make_order(
        [
            {
                "product_id": 999,
                "quantity": 1,
            }
        ],
    )

    with pytest.raises(InvalidOrderError):
        service.create_order(payload)

    order_repository.add.assert_not_called()


def test_update_product_preserves_omitted_fields(product_service, product_repository):
    existing_product = Product(
        id=1,
        name="Notebook",
        sku="NOTE-001",
        category="Stationery",
        price=Decimal("12.50"),
        stock_quantity=20,
        status="active",
        description="Original description",
    )
    product_repository.get_by_id.return_value = existing_product
    product_repository.save.side_effect = lambda product: product
    payload = ProductUpdate(name="Updated Notebook")
    updated_product = product_service.update_product(existing_product.id, payload)

    product_repository.save.assert_called_once_with(existing_product)
    assert updated_product.name == "Updated Notebook"
    assert updated_product.sku == "NOTE-001"
    assert updated_product.category == "Stationery"
    assert updated_product.price == Decimal("12.50")
    assert updated_product.stock_quantity == 20
    assert updated_product.description == "Original description"


def test_create_product_rejects_duplicate_sku(product_service, product_repository):
    existing_product = Product(
        id=1,
        name="Notebook",
        sku="NOTE-001",
        category="Stationery",
        price=Decimal("12.50"),
        stock_quantity=20,
    )
    product_repository.get_by_sku.return_value = existing_product
    payload = ProductCreate(
        name="Another Notebook",
        sku="NOTE-001",
        category="Stationery",
        price=Decimal("15.00"),
    )
    with pytest.raises(ProductAlreadyExistsError):
        product_service.update_product(existing_product.id, payload)
    product_repository.add.assert_not_called()
