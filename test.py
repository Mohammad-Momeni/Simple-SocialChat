import hashlib
import csv

password = 'matin@123'.encode("utf-8")
encryptPassword = hashlib.md5(password).hexdigest()
print(encryptPassword)

test = {}
test['Mohammad'] = 'matin@123'
print('Mohammad' in test.keys())

test['Ali'] = ['matin@123', 'offline']

test['Ali'][1] = 'online'

print(test)


message = '&private&matin&hello'
message = message.split('&')
print(message)