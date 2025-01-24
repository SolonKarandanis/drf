import logging
from typing import List

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

from cfehome.constants.constants import image_save_folder
from images.image_repository import ImageRepository
from images.models import Images
from django.conf import settings

from products.models import Product

User = settings.AUTH_USER_MODEL
MEDIA_URL = settings.MEDIA_URL
logger = logging.getLogger('django')
image_repo = ImageRepository()


class ImageService:

    def find_image_by_id(self, image_id: int) -> Images:
        return image_repo.find_image_by_id(image_id)

    def find_image_by_object_id(self, object_id: int) -> List[Images]:
        return image_repo.find_image_by_object_id(object_id)

    def find_profile_image(self, object_id: int) -> Images:
        return image_repo.find_profile_image(object_id)

    def find_product_images(self, object_id: int) -> List[Images]:
        return image_repo.find_product_images(object_id)

    def find_product_profile_images(self, object_ids: List[int]) -> List[Images]:
        return image_repo.find_product_profile_images(object_ids)

    def find_product_profile_image(self, object_id: int) -> Images:
        return image_repo.find_product_profile_image(object_id)

    def upload_profile_image(self, image: InMemoryUploadedFile, title: str, alt: str, user: User,
                             logged_in_user: User) -> None:
        image_repo.upload_profile_image(image, title, alt, user, logged_in_user)

    def upload_product_image(self, image: InMemoryUploadedFile, title: str, alt: str, product: Product,
                             logged_in_user: User) -> None:
        image_repo.upload_product_image(image, title, alt, product, logged_in_user)

    def delete_product_images(self, image_names: List[str], object_id: int) -> None:
        image_repo.delete_product_images(image_names, object_id)

    @transaction.atomic
    def upload_product_images(self, images: List[InMemoryUploadedFile], logged_in_user: User, product: Product,
                              is_edit: bool) -> None:
        for image in images:
            logger.info(f'---> ImageRepository ---> upload_product_images ---> image name: {image.name}')
            logger.info(f'---> ImageRepository ---> upload_product_images ---> image type: {image.content_type}')
            logger.info(f'---> ImageRepository ---> upload_product_images ---> image size: {image.size}')
            logger.info(f'------------------------------------------------------------------------')

        if is_edit:
            existing_product_images = self.find_product_images(product.id)
            current_profile_image = next(filter(lambda pi: pi.is_profile_image, existing_product_images), None)
            delimiter = f"{MEDIA_URL}{image_save_folder}"
            array_string = current_profile_image.image.url.split(delimiter)
            image_name = array_string[1]
            has_profile_image_changed = images[0].name != image_name
            logger.info(
                f'---> ImageRepository ---> upload_product_images ---> has_profile_image_changed: {has_profile_image_changed}')
            if has_profile_image_changed:
                current_profile_image.is_profile_image = False
                self.update_image_is_profile_image(current_profile_image)
            existing_images = []
            for existing_image in existing_product_images:
                array_string = existing_image.image.url.split(delimiter)
                image_name = array_string[1]
                existing_images.append(image_name)
            incoming_images = [image.name for image in images]
            images_changed = True if len(incoming_images) != len(existing_images) or \
                                     (len(incoming_images) == len(existing_images) and sorted(
                                         incoming_images) != sorted(
                                         existing_images)) else False
            logger.info(
                f'---> ImageRepository ---> upload_product_images ---> images_changed: {images_changed}')
            if images_changed:
                images_to_be_deleted = list(set(existing_images) - set(incoming_images))
                logger.info(
                    f'---> ImageRepository ---> upload_product_images ---> images_to_be_deleted: {len(images_to_be_deleted)}')
                if len(images_to_be_deleted) > 0:
                    images_to_be_deleted = [image_save_folder + image for image in images_to_be_deleted]
                    self.delete_product_images(images_to_be_deleted, product.id)
                images_to_be_added = list(set(incoming_images) - set(existing_images))
                logger.info(
                    f'---> ImageRepository ---> upload_product_images ---> images_to_be_added: {images_to_be_added}')
                logger.info(
                    f'---> ImageRepository ---> upload_product_images ---> images_to_be_added: {len(images_to_be_added)}')
                if len(images_to_be_added) > 0:
                    image_repo.bulk_create_images(product, logged_in_user, images, has_profile_image_changed)
        else:
            image_repo.bulk_create_images(product, logged_in_user, images, True)

    def update_image_is_profile_image(self, image: Images) -> None:
        image_repo.update_image_is_profile_image(image)
