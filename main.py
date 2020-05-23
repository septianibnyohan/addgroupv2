from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random
import logging

#Create Client Object and Logging
logging.basicConfig(filename="addgroup.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w')
#Creating an object 
logger=logging.getLogger() 
  
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 

api_id = 1149072
api_hash = '594c72967c4184f92a7a88b3b07cfd1f'
#phone = '+6285778151604'
phone = '+62' + input('Enter your phone number: +62')
client = TelegramClient('ses/'+phone, api_id, api_hash)
 
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

#Read Members from CSV File
#input_file = sys.argv[1]
input_file = 'input.csv'
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

#Choose a Group to Add Members
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print('Choose a group to add members:')
i=0
for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1
 
g_index = input("Enter a Number: ")
target_group=groups[int(g_index)]
 
target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
 
#Ask User to Enter the Adding Mode
mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
 
#Add Members to the Selected Group
n = 0 
for user in users:
    n += 1
    if n % 50 == 0:
        sleep(900)
    try:
        print ("Adding {}".format(user['id']))
        logger.info("Adding {}".format(user['id'])) 

        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        #print("Waiting for 60-180 Seconds...")
        seconds = random.randrange(2880, 4320)

        while seconds > 0 :
            sys.stdout.write("\rWaiting for {seconds} Seconds".format(seconds=seconds))
            sys.stdout.flush()
            seconds = seconds - 1
            time.sleep(1)
        #time.sleep(random.randrange(2880, 4320))
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        logger.error("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        break
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
        logger.error("The user's privacy settings do not allow you to do this. Skipping.")
    except:
        traceback.print_exc()
        print("Unexpected Error")
        other = traceback.format_exc()
        logger.error(other)
        continue