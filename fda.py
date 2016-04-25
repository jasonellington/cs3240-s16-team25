import copy
import json
import urllib.parse
import urllib.request
import getpass
import http.cookiejar
from lxml import html
from tabulate import tabulate

username = input("Please enter username: ")
password = getpass.getpass(prompt="Please enter password: ")

opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor,
)

login_form = opener.open('http://localhost:8000/myapplication/login/').read()
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
login_page = opener.open('http://localhost:8000/myapplication/fdalogin/', data)

# Use the following for debugging
# try:
#     reports = opener.open('http://localhost:8000/myapplication/fdalistreports/').read()
# except urllib.request.HTTPError as error:
#     f = open('error.html', 'wb')
#     f.write(error.read())

list = json.loads(opener.open('http://localhost:8000/myapplication/fdalistreports/').read().decode("utf-8"))

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
    report_response = json.loads(opener.open('http://localhost:8000/myapplication/fdagetreport?reportID=' + str(data['ID'][report_num-1])).read().decode("utf-8"))
except urllib.request.HTTPError as error:
    f = open('error.html', 'wb')
    f.write(error.read())
report = report_response['report']
print("Description:", report['Description'])
print("Author:", report['Author'])
print("Date:", report['Date'])
print("Content:", report['Content'])
files_present = False
if report_response['files']:
    files_present = True
    print("FILES:")
    i = 0
    for file in report_response['files']:
        i+=1
        print("\t" + str(i) + ": " + file['name'])
else:
    print("FILES: NONE")

if files_present:
    file_num = int(input("Enter number of file you would wish to download: "))
    file_path = input("Enter path where you would like to save the file: ")

    with open(file_path + report_response['files'][file_num-1]['name'][2:], 'wb') as out_file:
        download = opener.open('http://localhost:8000' + report_response['files'][file_num-1]['url']).read()
        out_file.write(download)