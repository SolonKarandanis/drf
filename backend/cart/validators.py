from rest_framework import serializers


def is_quantity_valid(self):
    if self <= 0:
        raise serializers.ValidationError({'quantity': 'Quantity needs to be a positive number'})
    return self
