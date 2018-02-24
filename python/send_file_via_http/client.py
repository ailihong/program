import requests

#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file

#url = "http://192.168.168.198:8081/"
url = "http://localhost:8081/"

fin = open('20180211091741a.jpg', 'rb')
files = {'file': fin}
try:
  r = requests.post(url, files=files)
  print r.text
finally:
	fin.close()
