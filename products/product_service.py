from typing import List
from django.db import transaction
from django.conf import settings

from images.image_repository import ImageRepository
from images.models import Images
from .dtos import CategoriesWithTotals, BrandsWithTotals, SizesWithTotals, ProductWithPreviewImage
from .models import Product, ProductAttributeValues
from .product_repository import ProductRepository
from .serializers import PostProductComment, ProductSearchRequestSerializer, SimilarProductsRequestSerializer, \
    CreateProductSerializer
from comments.comment_repository import CommentRepository

User = settings.AUTH_USER_MODEL
repo = ProductRepository()
comment_repo = CommentRepository()
image_repo = ImageRepository()


class ProductService:

    def find_by_uuid(self, uuid: str) -> Product:
        return repo.find_by_uuid(uuid)

    @transaction.atomic
    def find_product_images_by_uuid(self, uuid: str) -> List[Images]:
        product = repo.find_by_uuid(uuid, False)
        return image_repo.find_product_images(product.id)

    @transaction.atomic
    def find_similar_products(self, category_ids: List[int], limit: int) -> List[ProductWithPreviewImage]:
        product_results = repo.find_products_by_category_ids(category_ids, limit)
        products_with_preview_images = self.products_to_products_with_preview_images(product_results)
        return products_with_preview_images

    @transaction.atomic
    def find_product_attributes(self, uuid: str) -> List[ProductAttributeValues]:
        product = repo.find_by_uuid(uuid, False)
        return repo.find_product_attributes(product.id)

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

    @transaction.atomic
    def search_products(self, request: ProductSearchRequestSerializer) -> List[ProductWithPreviewImage]:
        serialized_data = request.data
        query = None
        categories = None
        brands = None
        sizes = None
        data_dict = dict(serialized_data)
        if "query" in data_dict:
            query = data_dict['query']
        if "categories" in data_dict:
            categories = data_dict['categories']
        if "brands" in data_dict:
            brands = data_dict['brands']
        if "sizes" in data_dict:
            sizes = data_dict['sizes']
        product_results = repo.search_products(query, categories, brands, sizes, None)
        products_with_preview_images = self.products_to_products_with_preview_images(product_results)
        return products_with_preview_images

    def products_to_products_with_preview_images(self, product_results: List[Product]) -> List[ProductWithPreviewImage]:
        product_ids = [product.id for product in product_results]
        product_preview_images = image_repo.find_product_profile_images(product_ids)
        product_preview_images_dict = {image.object_id: image for image in product_preview_images}
        products_with_preview_images: List[ProductWithPreviewImage] = [
            ProductWithPreviewImage(product=product, preview_image=product_preview_images_dict.get(product.id))
            for product in product_results
        ]
        return products_with_preview_images

    def get_categories_with_totals(self) -> List[CategoriesWithTotals]:
        return repo.get_categories_with_totals()

    def get_brands_with_totals(self) -> List[BrandsWithTotals]:
        return repo.get_brands_with_totals()

    def get_discounts_with_totals(self):
        pass

    def get_sizes_with_totals(self) -> List[SizesWithTotals]:
        return repo.get_sizes_with_totals()

    def create_product(self, request: CreateProductSerializer, logged_in_user: User) -> Product:
        serialized_data = request.data
        data_dict = dict(serialized_data)
        sku = data_dict['sku']
        title = data_dict['title']
        content = data_dict['content']
        price = data_dict['price']
        inventory = data_dict['inventory']
        new_product = Product(sku=sku, user=logged_in_user, title=title, content=content, price=price,
                              inventory=inventory)
