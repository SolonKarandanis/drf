from typing import List
from django.db import transaction
from django.conf import settings

from .dtos import CategoriesWithTotals, BrandsWithTotals, SizesWithTotals
from .models import Product
from .product_repository import ProductRepository
from .serializers import PostProductComment, ProductSearchRequestSerializer
from comments.comment_repository import CommentRepository

User = settings.AUTH_USER_MODEL
repo = ProductRepository()
comment_repo = CommentRepository()


class ProductService:

    def find_by_uuid(self, uuid: str) -> Product:
        return repo.find_by_uuid(uuid)

    def find_by_id(self, product_id: int) -> Product:
        return repo.find_by_id(product_id)

    def find_users_product_by_uuid(self, uuid: str, logged_in_user: User) -> Product:
        return repo.find_users_product_by_uuid(uuid, logged_in_user)

    def find_users_product_by_id(self, product_id: int, logged_in_user: User) -> Product:
        return repo.find_users_product_by_id(product_id, logged_in_user)

    def find_all_products(self) -> List[Product]:
        return repo.find_all_products()

    def find_supplier_products(self, logged_in_user: User) -> List[Product]:
        return repo.find_supplier_products(logged_in_user)

    def find_products_by_ids(self, product_ids: List[int]) -> List[Product]:
        return repo.find_products_by_ids(product_ids)

    def update_product_price(self, product_id: int, new_price: float) -> Product:
        product = self.find_by_id(product_id)
        product.price = new_price
        return repo.update_product_price(product)

    def find_public_products(self) -> List[Product]:
        return repo.find_public_products()

    def find_product_skus(self) -> List[str]:
        return repo.find_product_skus()

    @transaction.atomic
    def post_product_comment(self, request: PostProductComment, logged_in_user: User) -> Product:
        serialized_data = request.data
        data_dict = dict(serialized_data)
        product_id = data_dict['product_id']
        comment = data_dict['comment']
        product: Product = self.find_by_id(product_id)
        comment_repo.create_product_comment(comment, product, logged_in_user)
        return repo.find_by_id(product_id)

    def search_products(self, request: ProductSearchRequestSerializer) -> List[Product]:
        serialized_data = request.data
        query = None
        category_id = None
        brand_id = None
        size_id = None
        data_dict = dict(serialized_data)
        if "query" in data_dict:
            query = data_dict['query']
        if "category_id" in data_dict:
            category_id = data_dict['category_id']
        if "brand_id" in data_dict:
            brand_id = data_dict['brand_id']
        if "size_id" in data_dict:
            size_id = data_dict['size_id']
        return repo.search_products(query, None)

    def get_categories_with_totals(self) -> List[CategoriesWithTotals]:
        return repo.get_categories_with_totals()

    def get_brands_with_totals(self) -> List[BrandsWithTotals]:
        return repo.get_brands_with_totals()

    def get_discounts_with_totals(self):
        pass

    def get_sizes_with_totals(self) -> List[SizesWithTotals]:
        return repo.get_sizes_with_totals()
