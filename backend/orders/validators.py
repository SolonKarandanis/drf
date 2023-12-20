from rest_framework import serializers
from .models import Order


def order_exists(self):
    qs = Order.objects.filter(pk=self)
    exists = qs.exists()
    if not exists:
        raise serializers.ValidationError(f"Order does not exist")
    return self
