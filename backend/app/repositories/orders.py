from sqlalchemy import func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload
from app.models import Order


class OrderRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(
        self, search: str | None, status: str | None, offset: int, limit: int
    ) -> tuple[list[Order], int]:
        filters = []
        if search:
            search_pattern = f"%{search}%"
            filters.append(
                or_(
                    Order.order_number.ilike(search_pattern),
                    Order.customer_name.ilike(search_pattern),
                    Order.customer_email.ilike(search_pattern),
                )
            )
        if status:
            filters.append(Order.status == status)

        statement = (
            select(Order)
            .options(selectinload(Order.items))
            .where(*filters)
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        count_statement = select(func.count(Order.id)).where(*filters)

        orders = list(self.db_session.scalars(statement).all())
        total = self.db_session.scalar(count_statement) or 0
        return orders, total

    def get_by_id(self, order_id: int) -> Order | None:
        return self.db_session.get(Order, order_id, options=[selectinload(Order.items)])

    def add(self, order: Order) -> Order:
        try:
            self.db_session.add(order)
            self.db_session.commit()
            self.db_session.refresh(order)
            return order
        except SQLAlchemyError:
            self.db_session.rollback()
            raise

    def save(self, order: Order) -> Order:
        try:
            self.db_session.commit()
            self.db_session.refresh(order)
            return order
        except SQLAlchemyError:
            self.db_session.rollback()
            raise
