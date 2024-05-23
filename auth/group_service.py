from typing import List
from django.contrib.auth.models import Group
from .group_repository import GroupRepository

groupRepo = GroupRepository()


class GroupService:

    def exists_by_name(self, name: str) -> bool:
        return groupRepo.exists_by_name(name)

    def find_by_name(self, name: str) -> Group:
        return groupRepo.find_by_name(name)

    def create(self, name: str) -> Group:
        groupRepo.create(name)
        return self.find_by_name(name)

    def find_all_groups(self) -> List[Group]:
        return groupRepo.find_all_groups()
