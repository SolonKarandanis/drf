from auth.user_repository import UserRepository

user_repo = UserRepository()


def remove_unverified_users() -> None:
    user_repo.remove_unverified_users(3)
