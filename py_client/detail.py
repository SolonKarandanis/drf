import requests

endpoint = "http://localhost:8000/api/products/1/"


post_response = requests.get(endpoint)
print(post_response.json())
