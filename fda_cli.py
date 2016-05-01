import base64
import copy
import json
import os
import random
import urllib.parse
import urllib.request
import getpass
import http.cookiejar

import struct
from lxml import html
from tabulate import tabulate
from Crypto.Cipher import AES

remote_url = 'http://calm-tundra-99675.herokuapp.com/'
local_url = 'http://localhost:8000'

base_url = remote_url

encrypt_file = False
print("Welcome to SafeCollab File Download Application")
choice = input("If you would like to encrypt a file, enter '1', otherwise to view reports, just hit 'enter': ")
try:
    if int(choice) == 1:
        encrypt_file = True
except ValueError:
    pass

if encrypt_file:
    chunksize = 16 * 1024
    path = input("Please enter full path of file to encrypt: ")
    key = getpass.getpass(prompt="Please enter key for encrypted file: ")
    f = open(path, 'rb')

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(path)
    with open(path, 'rb') as infile:
        with open(path + '.enc', 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))
    quit()
username = input("Please enter username: ")
password = getpass.getpass(prompt="Please enter password: ")

opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor,
)

login_form = opener.open(base_url + '/myapplication/login/').read()
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
login_page = opener.open(base_url + '/myapplication/fdalogin/', data)

# Use the following for debugging
# try:
#     reports = opener.open('http://localhost:8000/myapplication/fdalistreports/').read()
# except urllib.request.HTTPError as error:
#     f = open('error.html', 'wb')
#     f.write(error.read())

list = json.loads(opener.open(base_url + '/myapplication/fdalistreports/').read().decode("utf-8"))

if not list['success']:
    print("Login unsuccessful")
    quit()

data = list['reports']
overview = copy.deepcopy(data)
overview.pop("Content", None)
overview.pop("ID", None)
print(tabulate(overview, headers="keys", tablefmt="grid"))

report_input = input("Please enter report num to view: ")
try:
    report_num = int(report_input)
except ValueError:
    print("Value must be a number")
    quit()

if report_num > len(data['num']):
    print("Report doesn't exist")
    quit()

try:
    report_response = json.loads(opener.open(base_url + '/myapplication/fdagetreport?reportID=' + str(data['ID'][report_num-1])).read().decode("utf-8"))
except urllib.request.HTTPError as error:
    f = open('error.html', 'wb')
    f.write(error.read())
report = report_response['report']
print("\n============== REPORT ==============\n")
print("DESCRIPTION:", report['Description'])
print("AUTHOR:", report['Author'])
print("DATE:", report['Date'])
print("CONTENT:", report['Content'])
files_present = False
if report_response['files']:
    files_present = True
    print("FILES:")
    i = 0
    for file in report_response['files']:
        i+=1
        print("\t" + str(i) + ": " + file['name'][2:])
else:
    print("FILES: NONE")

if files_present:
    file_num = int(input("\nEnter number of file you would wish to download: "))
    file_path = input("Enter path where you would like to save the file: ")
    if report['Encrypted'] == 0:
        with open(file_path + report_response['files'][file_num-1]['name'][2:], 'wb') as out_file:
            download = opener.open(base_url + report_response['files'][file_num-1]['url']).read()
            out_file.write(download)
    else:
        chunksize = 16 * 1024
        with open(file_path + report_response['files'][file_num-1]['name'][2:].replace(".enc", ""), 'wb') as out_file:
            download = opener.open(base_url + report_response['files'][file_num-1]['url'])
            key = getpass.getpass(prompt="Files are encrypted, please enter key: ")
            origsize = struct.unpack('<Q', download.read(struct.calcsize('Q')))[0]
            iv = download.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)
            while True:
                chunk = download.read(chunksize)
                if len(chunk) == 0:
                    break
                out_file.write(decryptor.decrypt(chunk))