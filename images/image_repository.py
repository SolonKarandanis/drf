from images.models import Images


class ImageRepository:

    def find_image_by_id(self, image_id: int):
        return Images.objects.get(pk=image_id)

    def find_user_profile_image(self, user_id: int):
        pass

    def upload_image(self):
        pass