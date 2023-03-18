import requests

endpoint = "https://httpbin.org/status/200"
endpoint = "http://localhost:8000/products/"

#get_response = requests.get(endpoint)
post_response = requests.post(endpoint,json={"title":"post"})
print(post_response.json())
