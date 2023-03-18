import requests

endpoint = "http://localhost:8000/api/products/"

data ={
    "title":"This field is done"
}

post_response = requests.post(endpoint,data)
print(post_response.json())
