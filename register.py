import os
from telethon.sync import TelegramClient

if not os.path.isdir('ses'):
    os.mkdir('ses')

phonelist = []
with open ('phonelist.txt', 'rt') as myfile: # Open lorem.txt for reading text data.
    for myline in myfile:                # For each line, stored as myline,
        phonelist.append(myline.strip())           # add its contents to mylines.
#print(mylines)


api_id = 1149072
api_hash = '594c72967c4184f92a7a88b3b07cfd1f'

for phone in phonelist:
    print('Phone Number :', phone)
    client = TelegramClient('ses/'+phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))