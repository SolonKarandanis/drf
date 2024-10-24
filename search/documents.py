from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from products.models import Product


@registry.register_document
class ProductDocument(Document):

    user = fields.ObjectField(
        properties={"id": fields.IntegerField(), "username": fields.TextField()}
    )
    brand = fields.ObjectField(properties={"name": fields.TextField()})
    category = fields.ObjectField(properties={"name": fields.TextField()})

    class Index:
        name = "product_index"

    class Django:
        model = Product

        fields = [
            "id",
            "sku",
            "title",
            "content",
            "fabric_details",
            "care_instructions",
            "price",
            "inventory",
            "number_sold",
            "uuid"
        ]