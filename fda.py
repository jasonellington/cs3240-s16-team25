import json
import urllib.parse
import urllib.request
import getpass
import http.cookiejar
from lxml import html

username = input("Please enter username: ")
password = getpass.getpass(prompt="Please enter password: ")

opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor,
)

login_form = opener.open('http://localhost:8000/myapplication/login').read()
csrf_token = html.fromstring(login_form).xpath(
    '//input[@name="csrfmiddlewaretoken"]/@value'
)[0]

values = {
    'username': username,
    'password': password,
    'csrfmiddlewaretoken': csrf_token,
}

data = urllib.parse.urlencode(values)
data = data.encode('utf-8')
login_page = opener.open('http://localhost:8000/myapplication/login', data)
print(login_page.read())