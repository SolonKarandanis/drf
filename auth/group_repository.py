from typing import List
from django.contrib.auth.models import Group


class GroupRepository:

    def exists_by_name(self, name: str) -> bool:
        exists = Group.objects.filter(name=name).exists()
        return exists

    def find_by_name(self, name: str) -> Group:
        qs = Group.objects.get(name=name)
        return qs

    def create(self, name: str) -> None:
        Group.objects.create(name=name)

    def find_all_groups(self) -> List[Group]:
        return Group.objects.all()
