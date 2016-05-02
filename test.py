import requests

number = "+19086421986"

data = '{"to": "' + number + '","body": "You have a new message on SafeCollab!"}'
headers = {
    'Content-Type': 'application/json',
    }
url = "https://5726cb496e1ff90008000003:0b191af91f1c3a5f9a73f87178915955@api.easysmsapp.com/accounts/5726cb496e1ff90008000003" + '/messages'
r = requests.post(url, headers=headers, data=data)
print(r.status_code)
print(r.content)