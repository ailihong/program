import requests
r = requests.post("http://127.0.0.1:12345/", data={'foo': 'your data gg'})
# And done.
print(r.text) # displays the result body.
