import requests

endpoint = "https://httpbin.org/status/200"
endpoint = "http://localhost:8000/api/products/"

#get_response = requests.get(endpoint)
post_response = requests.get(endpoint)
print(post_response.json())
