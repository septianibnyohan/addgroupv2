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

#Create Client Object and Login
api_id = 1149072
api_hash = '594c72967c4184f92a7a88b3b07cfd1f'
phone = '+6285778151604'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

receiver = InputPeerUser(398354398, 8876181226392590228)
client.send_message(receiver, "test telegram")
