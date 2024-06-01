from typing import List

from images.models import Images
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL


class ImageRepository:

    def find_image_by_id(self, image_id: int) -> Images:
        return Images.objects.get(pk=image_id)

    def find_image_by_object_id(self, object_id: int) -> List[Images]:
        return Images.objects.filter(object_id=object_id)

    def upload_profile_image(self, image, title: str, alt: str, user: User, logged_in_user: User) -> None:
        Images.objects.create(title=title, alt=alt, image=image, content_object=user, user=logged_in_user)

    def upload_product_image(self, image, title: str, alt: str, product: Product, logged_in_user: User) -> None:
        Images.objects.create(title=title, alt=alt, image=image, ontent_object=product, user=logged_in_user)
