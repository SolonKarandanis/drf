from django.http import HttpResponse

from search.documents import ProductDocument
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination


class SearchService:
    product_document = ProductDocument

    def search_products(self, query: str):
        try:
            q = Q(
                "multi_match",
                query=query,
                fields=[
                    "product.name",
                    "product.title",
                    "brand.name",
                    "product.content",
                    "product.fabric_details",
                    "product.care_instructions",
                ],
                fuzziness="auto",
            ) & Q(
                should=[
                    Q("match", is_default=True),
                ],
                minimum_should_match=1,
            )
            search = self.product_document.search().query(q)
            response = search.execute()
            
        except Exception as e:
            return HttpResponse(e, status=500)