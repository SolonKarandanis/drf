from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class ProductIDField(models.CharField):
    description = "A unique product identifier"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        kwargs['unique'] = True
        super().__init__(*args, **kwargs)


class OrderField(models.PositiveIntegerField):

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                obj = self.model.objects.latest(self.attname)
                value = obj.order + 1
            except ObjectDoesNotExist:
                value = 1
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
