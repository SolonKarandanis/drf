import logging
from typing import List
from django.db import transaction
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from images.image_repository import ImageRepository
from images.models import Images
from .dtos import CategoriesWithTotals, BrandsWithTotals, SizesWithTotals, ProductWithPreviewImage, ProductAttributes, \
    AllAttributeOptions
from .models import Product, ProductAttributeValues, Category, Brand, AttributeOptions
from .product_repository import ProductRepository
from .serializers import PostProductComment, ProductSearchRequestSerializer, SimilarProductsRequestSerializer, \
    SaveProductSerializer
from comments.comment_repository import CommentRepository

logger = logging.getLogger('django')
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

    def initialize_product_from_serializer(self, data_dict: dict[str, object]) -> Product:
        sku = data_dict['sku']
        title = data_dict['title']
        price = data_dict['price']
        inventory = data_dict['inventory']
        publish_status = data_dict['publishStatus']
        availability_status = data_dict['availabilityStatus']
        published_date = data_dict['publishedDate']

        new_product = Product(sku=sku, title=title, price=price, inventory=inventory,
                              publish_status=publish_status, availability_status=availability_status,
                              published_date=published_date)
        if "content" in data_dict:
            content = data_dict['content']
            new_product.content = content
        if "fabricDetails" in data_dict:
            fabric_details = data_dict['fabricDetails']
            new_product.fabric_details = fabric_details
        if "careInstructions" in data_dict:
            care_instructions = data_dict['careInstructions']
            new_product.care_instructions = care_instructions

        return new_product

    @transaction.atomic
    def create_product(self, request: SaveProductSerializer, images: List[InMemoryUploadedFile],
                       logged_in_user: User) -> Product:
        serialized_data = request.data
        data_dict = dict(serialized_data)
        logger.info(f'---> ProductService ---> create_product ---> data_dict: {data_dict}')
        new_product = self.initialize_product_from_serializer(data_dict)
        new_product.user = logged_in_user
        repo.save_product(new_product)

        category_ids = data_dict['categories']
        logger.info(f'---> ProductService ---> create_product ---> category_ids: {category_ids}')
        brand_ids = data_dict['brand']
        logger.info(f'---> ProductService ---> create_product ---> brand_ids: {brand_ids}')
        size_ids = data_dict['sizes']
        logger.info(f'---> ProductService ---> create_product ---> size_ids: {size_ids}')
        gender_ids = data_dict['gender']
        logger.info(f'---> ProductService ---> create_product ---> gender_ids: {gender_ids}')
        color_ids = data_dict['colors']
        logger.info(f'---> ProductService ---> create_product ---> color_ids: {color_ids}')

        categories = repo.find_categories_by_ids(category_ids)
        if len(categories) == 0:
            raise serializers.ValidationError({'categories': "Supplied Categories don't exist"})
        brands = repo.find_brands_by_ids(brand_ids)
        if len(brands) == 0:
            raise serializers.ValidationError({'brands': "Supplied Brands don't exist"})
        sizes = repo.find_sizes_by_ids(size_ids)
        if len(sizes) == 0:
            raise serializers.ValidationError({'sizes': "Supplied Sizes don't exist"})
        genders = repo.find_genders_by_ids(gender_ids)
        if len(genders) == 0:
            raise serializers.ValidationError({'genders': "Supplied Genders don't exist"})
        colors = repo.find_colors_by_ids(color_ids)
        if len(colors) == 0:
            raise serializers.ValidationError({'colors': "Supplied Colors don't exist"})

        new_product.category.add(categories)
        new_product.attributes.add(sizes)
        new_product.attributes.add(genders)
        new_product.attributes.add(colors)
        new_product.brand = brands[0]

        if "images" in data_dict:
            images = data_dict['images']
            logger.info(f'---> ProductService ---> create_product ---> images: {images}')

        return new_product

    def find_product_categories(self, product_uuid: str) -> List[Category]:
        return repo.find_product_categories(product_uuid)

    @transaction.atomic
    def find_product_attributes(self, product_uuid: str) -> ProductAttributes:
        colors = repo.find_product_colors(product_uuid)
        sizes = repo.find_product_sizes(product_uuid)
        genders = repo.find_product_genders(product_uuid)
        product_attributes = ProductAttributes(colors=colors, sizes=sizes, genders=genders)
        return product_attributes

    def find_all_categories(self) -> List[Category]:
        return repo.find_all_categories()

    def find_all_brands(self) -> List[Brand]:
        return repo.find_all_brands()

    @transaction.atomic
    def find_all_attributes(self) -> AllAttributeOptions:
        colors = self.find_all_colours()
        sizes = self.find_all_sizes()
        genders = self.find_all_genders()
        attribute_options = AllAttributeOptions(colors=colors, sizes=sizes, genders=genders)
        return attribute_options

    def find_all_sizes(self) -> List[AttributeOptions]:
        return repo.find_all_sizes()

    def find_all_colours(self) -> List[AttributeOptions]:
        return repo.find_all_colours()

    def find_all_genders(self) -> List[AttributeOptions]:
        return repo.find_all_genders()
