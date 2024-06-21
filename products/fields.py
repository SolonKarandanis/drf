from django.db import models


class ProductIDField(models.CharField):
    description = "A unique product identifier"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        kwargs['unique'] = True
        super().__init__(*args, **kwargs)
