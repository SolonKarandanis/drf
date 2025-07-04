import logging
import random
from typing import List

from django.core.files.uploadedfile import InMemoryUploadedFile

from images.models import Images, ImagesManager
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL
MEDIA_URL = settings.MEDIA_URL
logger = logging.getLogger('django')


class ImageRepository:

    def _model_manager(self) -> ImagesManager:
        return Images.objects

    def find_image_by_id(self, image_id: int) -> Images:
        return self._model_manager().get(pk=image_id)

    def find_image_by_object_id(self, object_id: int) -> List[Images]:
        return self._model_manager().filter(object_id=object_id)

    def find_profile_image(self, object_id: int) -> Images:
        images = self._model_manager().get_queryset().is_profile_image().filter(object_id=object_id, content_type_id=17)
        if len(images) >= 1:
            return images[0]
        return None

    def find_product_images(self, object_id: int) -> List[Images]:
        return self._model_manager().filter(object_id=object_id, content_type_id=18)

    def find_product_profile_images(self, object_ids: List[int]) -> List[Images]:
        return self._model_manager().get_queryset().is_profile_image().filter(object_id__in=object_ids, content_type_id=18)

    def find_product_profile_image(self, object_id: int) -> Images:
        return self._model_manager().get_queryset().is_profile_image() \
            .filter(object_id=object_id, content_type_id=18) \
            .first()

    def upload_profile_image(self, image: InMemoryUploadedFile, title: str, alt: str, user: User,
                             logged_in_user: User) -> None:
        size: int = image.size
        type: str = image.content_type
        self._model_manager().create(title=title, alt=alt, image=image, content_object=user,
                              uploaded_by=logged_in_user, is_profile_image=True, size=size, image_type=type)

    def upload_product_image(self, image: InMemoryUploadedFile, title: str, alt: str, product: Product,
                             logged_in_user: User) -> None:
        self._model_manager().create(title=title, alt=alt, image=image, content_object=product, uploaded_by=logged_in_user)

    def delete_product_images(self, image_names: List[str], object_id: int) -> None:
        self._model_manager() \
            .filter(image__in=image_names) \
            .filter(object_id=object_id, content_type_id=18) \
            .delete()

    def bulk_create_images(self, product: Product, logged_in_user: User, images: List[InMemoryUploadedFile],
                           has_profile_image_changed: bool) -> None:
        title = product.sku
        image_objects = [
            Images(title=f"{title}-{random.random()}", alt=f"{title}-{random.random()}", image=image, content_object=product,
                   uploaded_by=logged_in_user, image_type=image.content_type, size=image.size)
            for index, image in enumerate(images)
        ]
        if has_profile_image_changed:
            image_objects[0].is_profile_image = True
        self._model_manager().bulk_create(image_objects, batch_size=20)

    def update_image_is_profile_image(self, image: Images) -> None:
        image.save(update_fields=['is_profile_image'])

    def update_image(self, image: Images) -> None:
        image.save()
