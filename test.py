import hashlib
import csv

password = 'matin@123'.encode("utf-8")
encryptPassword = hashlib.md5(password).hexdigest()
print(encryptPassword)

test = {}
test['Mohammad'] = 'matin@123'
print('Mohammad' in test.keys())

test['Ali'] = ['matin@123', 'offline']

print(test)

with open('credentials.csv', mode='r') as infile:
    reader = csv.reader(infile)
    credentialsData = {rows[0] : rows[1] for rows in reader}

print(credentialsData)

with open('credentials.csv', mode='a') as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            writer.writerow(['Mohammad', encryptPassword])