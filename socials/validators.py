from rest_framework import serializers
from auth.user_repository import UserRepository
from socials.social_repository import SocialRepository

social_repo = SocialRepository()
userRepo = UserRepository()


def validate_user_id(self):
    qs = userRepo.user_user_id_exists(id=self)
    if not qs:
        raise serializers.ValidationError(f"User id: {self} does not exist")
    return self


def validate_social_id(self):
    qs = social_repo.exists_social_by_social_by_id(id=self)
    if not qs:
        raise serializers.ValidationError(f"Social id: {self} does not exist")
    return self
