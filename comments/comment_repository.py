from django.conf import settings

from orders.models import Order
from products.models import Product
from .models import Comment

User = settings.AUTH_USER_MODEL

class CommentRepository:

    def create_order_comment(self, comment: str, order: Order, logged_in_user: User) -> None:
        username = logged_in_user.username
        user_email = logged_in_user.email
        first_name = logged_in_user.first_name
        last_name = logged_in_user.last_name
        Comment.objects.create(content=comment, content_object=order, user=logged_in_user,
                               user_username=username, user_email=user_email, user_first_name=first_name,
                               user_last_name=last_name)

    def create_product_comment(self, comment: str, product: Product, logged_in_user: User) -> None:
        username = logged_in_user.username
        user_email = logged_in_user.email
        first_name = logged_in_user.first_name
        last_name = logged_in_user.last_name
        Comment.objects.create(content=comment, content_object=product, user=logged_in_user,
                               user_username=username, user_email=user_email, user_first_name=first_name,
                               user_last_name=last_name)
