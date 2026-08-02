from sqlalchemy import select, func, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models import Product


class ProductRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(
        self,
        search: str | None,
        category: str | None,
        status: str | None,
        offset: int,
        limit: int,
    ) -> tuple[list[Product], int]:
        filters = []
        if search:
            search_pattern = f"%{search}%"
            filters.append(
                or_(
                    Product.name.ilike(search_pattern),
                    Product.sku.ilike(search_pattern),
                )
            )
        if category:
            filters.append(Product.category == category)
        if status:
            filters.append(Product.status == status)

        statement = (
            select(Product)
            .where(*filters)
            .order_by(Product.id)
            .offset(offset)
            .limit(limit)
        )
        count_statement = select(func.count()).select_from(Product).where(*filters)
        products = list(self.db_session.scalars(statement).all())
        total = self.db_session.scalar(count_statement) or 0
        return products, total

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db_session.get(Product, product_id)

    def get_by_sku(self, sku: str) -> Product | None:
        statement = select(Product).where(Product.sku == sku)
        return self.db_session.scalar(statement)

    def add(self, product: Product) -> Product:
        try:
            self.db_session.add(product)
            self.db_session.commit()
            self.db_session.refresh(product)
            return product
        except SQLAlchemyError:
            self.db_session.rollback()
            raise

    def save(self, product: Product) -> Product:
        try:
            self.db_session.commit()
            self.db_session.refresh(product)
            return product
        except SQLAlchemyError:
            self.db_sesson.rollback()
            raise

    def delete(self, product: Product) -> None:
        try:
            self.db_session.delete(product)
            self.db_session.commit()
        except SQLAlchemyError:
            self.db_session.rollback()
            raise
