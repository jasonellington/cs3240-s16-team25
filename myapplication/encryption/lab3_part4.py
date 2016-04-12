# Daniel Codos (dbc5ba)\

import json
from Crypto.Cipher import DES

message_dict = {}

key = input("Enter a key: ")
message = input("Enter a message: ")
des = DES.new(key, DES.MODE_ECB)
cipher_text = des.encrypt(message)

message_dict["Encrypted File"] = cipher_text

with open('secret.txt', 'w') as output:
    json.dump(message, output)