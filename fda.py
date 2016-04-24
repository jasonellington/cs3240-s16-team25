import json
import urllib.parse
import urllib.request
import getpass

username = input("Please enter username: ")
password = getpass.getpass(prompt="Please enter password: ")

values = {
    'username': username,
    'password': password
}

data = urllib.parse.urlencode(values)
data = data.encode('ascii')
response = urllib.request.urlopen('http://localhost:8000/myapplication/fdalogin', data)

print(response.read())