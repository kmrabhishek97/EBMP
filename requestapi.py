import requests
 
# api-endpoint
URL = "http://localhost:8000/classify/"
 
# location given here
location = "delhi technological university"
 
# defining a params dict for the parameters to be sent to the API
PARAMS = {'address':location}
files = {'image': open('dataset/6.jpg', 'rb')}
# sending get request and saving the response as response object
r = requests.post(url = URL, params = PARAMS, files=files)
print(r)
# extracting data in json format
data = r.json()
 
print(data)
