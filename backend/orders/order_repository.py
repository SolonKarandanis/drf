from .models import Order


class OrderRepository:

    def find_order_ids_with_is_shipped(self):
        return Order.objects.get_queryset().order_ids_with_is_shipped()
