from orders.models import Order
from products.models import Product
from .models import Comment


class CommentRepository:

    def create_order_comment(self, order: Order):
        Comment.objects.create(content="", content_object=order)

    def create_product_comment(self, product: Product):
        Comment.objects.create(content="", content_object=product)
