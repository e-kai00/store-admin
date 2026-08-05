import argparse
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session
from app.database import engine
from app.models import Order, OrderItem, Product
from app.seed_data import ORDER_SPECS, PRODUCTS


def create_order_item(
    product: Product,
    quantity: int,
) -> OrderItem:
    line_total = product.price * quantity

    return OrderItem(
        product_id=product.id,
        product_name=product.name,
        quantity=quantity,
        unit_price=product.price,
        line_total=line_total,
    )


def create_order(
    order_number: str,
    customer_name: str,
    customer_email: str,
    status: str,
    items: list[OrderItem],
    days_ago: int,
) -> Order:
    total = sum(
        (item.line_total for item in items),
        start=Decimal("0.00"),
    )
    return Order(
        order_number=order_number,
        customer_name=customer_name,
        customer_email=customer_email,
        status=status,
        total=total,
        created_at=datetime.now(timezone.utc) - timedelta(days=days_ago),
        items=items,
    )


def clear_database() -> None:
    with Session(
        bind=engine,
        expire_on_commit=False,
    ) as session:
        session.execute(delete(OrderItem))
        session.execute(delete(Order))
        session.execute(delete(Product))
        session.commit()


def seed_database(reset: bool = False) -> None:
    if reset:
        clear_database()
    with Session(
        bind=engine,
        expire_on_commit=False,
    ) as session:
        product_count = session.scalar(select(func.count(Product.id)))
        if product_count:
            print("Products already exist. " "Use --reset to replace existing data.")
            return
        products = [Product(**data) for data in PRODUCTS]
        session.add_all(products)
        session.flush()

        products_by_sku = {product.sku: product for product in products}
        orders: list[Order] = []
        for (
            order_number,
            customer_name,
            customer_email,
            order_status,
            days_ago,
            item_specs,
        ) in ORDER_SPECS:
            order_items = [
                create_order_item(
                    products_by_sku[sku],
                    quantity,
                )
                for sku, quantity in item_specs
            ]
            orders.append(
                create_order(
                    order_number=order_number,
                    customer_name=customer_name,
                    customer_email=customer_email,
                    status=order_status,
                    items=order_items,
                    days_ago=days_ago,
                )
            )
        session.add_all(orders)
        session.commit()
        print(f"Seeded {len(products)} products " f"and {len(orders)} orders.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing products and orders before seeding.",
    )
    arguments = parser.parse_args()
    seed_database(reset=arguments.reset)
