import logging
from typing import List
from django.db import transaction
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from images.image_service import ImageService
from images.models import Images
from .dtos import CategoriesWithTotals, BrandsWithTotals, SizesWithTotals, ProductWithPreviewImage, ProductAttributes, \
    AllAttributeOptions
from .models import Product, ProductAttributeValues, Category, Brand, AttributeOptions
from .product_repository import ProductRepository
from .serializers import PostProductComment, ProductSearchRequestSerializer, \
    SaveProductSerializer, UpdateProductSerializer
from comments.comment_repository import CommentRepository

logger = logging.getLogger('django')
User = settings.AUTH_USER_MODEL
repo = ProductRepository()
comment_repo = CommentRepository()
image_service = ImageService()


class ProductService:

    def find_by_uuid(self, uuid: str, fetch_children: bool = True) -> Product:
        return repo.find_by_uuid(uuid, fetch_children)

    @transaction.atomic
    def find_product_images_by_uuid(self, uuid: str) -> List[Images]:
        product = repo.find_by_uuid(uuid, False)
        return image_service.find_product_images(product.id)

    @transaction.atomic
    def find_similar_products(self, category_ids: List[int], limit: int) -> List[ProductWithPreviewImage]:
        product_results = repo.find_products_by_category_ids(category_ids, limit)
        products_with_preview_images = self.products_to_products_with_preview_images(product_results)
        return products_with_preview_images

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
        product_preview_images = image_service.find_product_profile_images(product_ids)
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

    @transaction.atomic
    def _save_product(self, data_dict: dict[str, object], logged_in_user: User, existing_product: Product | None) \
            -> Product:
        product_to_be_saved = None
        price = data_dict['price']
        inventory = data_dict['inventory']
        publish_status = data_dict['publishStatus']
        availability_status = data_dict['availabilityStatus']
        published_date = data_dict['publishedDate']

        if existing_product is None:
            sku = data_dict['sku']
            title = data_dict['title']
            product_to_be_saved = Product(sku=sku, title=title, price=price, inventory=inventory,
                                          publish_status=publish_status, availability_status=availability_status,
                                          published_date=published_date)
        else:
            product_to_be_saved = existing_product
            product_to_be_saved.price = price
            product_to_be_saved.inventory = inventory
            product_to_be_saved.publish_status = publish_status
            product_to_be_saved.availability_status = availability_status
            product_to_be_saved.published_date = published_date

        product_to_be_saved.user = logged_in_user

        if "content" in data_dict:
            content = data_dict['content']
            product_to_be_saved.content = content
        if "fabricDetails" in data_dict:
            fabric_details = data_dict['fabricDetails']
            product_to_be_saved.fabric_details = fabric_details
        if "careInstructions" in data_dict:
            care_instructions = data_dict['careInstructions']
            product_to_be_saved.care_instructions = care_instructions

        brand_id = int(data_dict['brand'])
        if product_to_be_saved.brand_id != brand_id:
            brand = repo.find_brands_by_id(brand_id)
            if brand is None:
                raise serializers.ValidationError({'brands': "Supplied Brands don't exist"})

            product_to_be_saved.brand = brand
        repo.save_product(product_to_be_saved)

        return product_to_be_saved

    def _check_attribute_input_validity(self, categories: List[Category], sizes: List[AttributeOptions],
                                        gender: AttributeOptions, colors: List[AttributeOptions]):
        if len(categories) == 0:
            raise serializers.ValidationError({'categories': "Supplied Categories don't exist"})
        if len(sizes) == 0:
            raise serializers.ValidationError({'sizes': "Supplied Sizes don't exist"})
        if gender is None:
            raise serializers.ValidationError({'genders': "Supplied Genders don't exist"})
        if len(colors) == 0:
            raise serializers.ValidationError({'colors': "Supplied Colors don't exist"})

    @transaction.atomic
    def _save_product_attributes(self, data_dict: dict[str, object], product: Product, is_edit: bool):
        total_product_attribute_values = []
        categories_changed = False
        gender_changed = False
        sizes_changed = False
        colors_changed = False
        category_ids: List[int] = data_dict['categories']
        size_ids: List[int] = data_dict['sizes']
        gender_id: int = data_dict['gender']
        color_ids: List[int] = data_dict['colors']

        categories = repo.find_categories_by_ids(category_ids)
        sizes = repo.find_sizes_by_ids(size_ids)
        gender = repo.find_genders_by_id(gender_id)
        colors = repo.find_colors_by_ids(color_ids)

        self._check_attribute_input_validity(categories, sizes, gender, colors)

        if is_edit:
            product_attribute_value_ids_to_be_deleted: List[int] = []
            existing_product_categories = repo.find_product_categories(product.uuid)
            existing_product_colors = repo.find_product_colors(product.uuid)
            existing_product_sizes = repo.find_product_sizes(product.uuid)
            existing_product_gender = repo.find_product_genders(product.uuid)

            existing_cat_ids = [category.id for category in existing_product_categories]
            existing_s_ids = [size.attribute_option_id for size in existing_product_sizes]
            existing_clr_ids = [color.attribute_option_id for color in existing_product_colors]

            categories_changed = True if len(category_ids) != len(existing_cat_ids) or \
                                         (len(category_ids) == len(existing_cat_ids) and sorted(category_ids) != sorted(
                                             existing_cat_ids)) else False
            sizes_changed = True if len(size_ids) != len(existing_s_ids) or \
                                    (len(size_ids) == len(existing_s_ids) and sorted(size_ids) != sorted(
                                        existing_s_ids)) else False
            colors_changed = True if len(color_ids) != len(existing_clr_ids) or \
                                     (len(color_ids) == len(existing_clr_ids) and sorted(color_ids) != sorted(
                                         existing_clr_ids)) else False

            gender_changed = False if len(existing_product_gender) > 0 and \
                                      existing_product_gender[0].attribute_option_id == gender.id else True
            logger.info(
                f'---> ProductService ---> save_product_attributes ---> categories_changed: {categories_changed}')
            logger.info(
                f'---> ProductService ---> save_product_attributes ---> sizes_changed: {sizes_changed}')
            logger.info(
                f'---> ProductService ---> save_product_attributes ---> colors_changed: {colors_changed}')
            logger.info(
                f'---> ProductService ---> save_product_attributes ---> gender_changed: {gender_changed}')

            if categories_changed:
                product.categories.clear()

            if len(existing_product_gender) > 0 and gender_changed:
                repo.delete_product_attribute_value(existing_product_gender[0].id)

            if sizes_changed and len(existing_product_sizes) > 0:
                product_attribute_value_ids_to_be_deleted.append(existing_product_sizes[0].attribute_id)

            if colors_changed and len(existing_product_colors) > 0:
                product_attribute_value_ids_to_be_deleted.append(existing_product_colors[0].attribute_id)

            if len(product_attribute_value_ids_to_be_deleted) > 0:
                repo.delete_product_attribute_values_by_attribute_ids(product.id,
                                                                      product_attribute_value_ids_to_be_deleted)

        if not is_edit or (is_edit and categories_changed):
            product.categories.add(*categories)

        if not is_edit or (is_edit and sizes_changed):
            size_product_attribute_values = [
                ProductAttributeValues(
                    product=product, attribute=size.attribute, attribute_option=size) for size in sizes
            ]
            total_product_attribute_values.extend(size_product_attribute_values)

        if not is_edit or (is_edit and gender_changed):
            gender_product_attribute_value = ProductAttributeValues(
                product=product, attribute=gender.attribute, attribute_option=gender)
            total_product_attribute_values.append(gender_product_attribute_value)

        if not is_edit or (is_edit and colors_changed):
            colors_product_attribute_values = [
                ProductAttributeValues(
                    product=product, attribute=color.attribute, attribute_option=color) for color in colors
            ]
            total_product_attribute_values.extend(colors_product_attribute_values)

        if len(total_product_attribute_values) > 0:
            repo.bulk_create_product_attribute_values(total_product_attribute_values)

    def _save_product_images(self, image_files: List[InMemoryUploadedFile], logged_in_user: User, product: Product):
        has_image_files = len(image_files) > 0
        logger.info(f'---> ProductService ---> create_product ---> has_image_files: {has_image_files}')
        if has_image_files:
            image_service.upload_product_images(image_files, logged_in_user, product)

    def update_product(self, existing_product: Product, request: UpdateProductSerializer,
                       image_files: List[InMemoryUploadedFile], logged_in_user: User) -> Product:
        serialized_data = request.data
        data_dict = dict(serialized_data)
        existing_product = self._save_product(data_dict, logged_in_user, existing_product)
        self._save_product_attributes(data_dict, existing_product, True)
        self._save_product_images(image_files, logged_in_user, existing_product)
        return existing_product

    def create_product(self, request: SaveProductSerializer, image_files: List[InMemoryUploadedFile],
                       logged_in_user: User) -> Product:
        serialized_data = request.data
        data_dict = dict(serialized_data)
        new_product = self._save_product(data_dict, logged_in_user, None)
        self._save_product_attributes(data_dict, new_product, False)
        self._save_product_images(image_files, logged_in_user, new_product)
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

    def find_first_product_attribute_value_size_by_product_id(self, product_id: int) -> ProductAttributeValues:
        return repo.find_first_product_attribute_value_size_by_product_id(product_id)

    def find_first_product_attribute_value_color_by_product_id(self, product_id: int) -> ProductAttributeValues:
        return repo.find_first_product_attribute_value_color_by_product_id(product_id)
