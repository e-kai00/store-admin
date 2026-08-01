from sqlalchemy.exc import IntegrityError
from app.models import Product
from app.repositories.products import ProductRepository
from app.schemas import ProductCreate, ProductUpdate


class ProductAlreadyExistsError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_products(
        self,
        search: str | None,
        category: str | None,
        status: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Product], int]:
        offset = (page - 1) * page_size
        normalize_search = search.strip() if search else None
        return self.repository(
            search=normalize_search,
            category=category,
            status=status,
            offset=offset,
            limit=page_size
        )

    def create_product(self, product_data: ProductCreate) -> Product:
        exisitng_product = self.repository.get_by_sku(product_data.sku)
        if exisitng_product is not None:
            raise ProductAlreadyExistsError
        product = Product(**product_data.model_dump())
        try:
            return self.repository.add(product)
        except IntegrityError as error:
            raise ProductAlreadyExistsError from error

    def get_product(self, product_id: int) -> Product | None:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError
        return product

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError
        update_data = product_data.model_dump(exclude_unset=True)
        new_sku = update_data.get("sku")
        if new_sku is not None and new_sku != product.sku:
            existing_product = self.repository.get_by_id(new_sku)
            if existing_product is not None:
                raise ProductAlreadyExistsError
        # apply only the fields provided in the PATCH request to the existing product.
        for field_name, value in update_data.items():
            setattr(product, field_name, value)
        return self.repository.save(product)

    def delete_product(self, product_id: int) -> None:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError
        self.repository.delete(product)
