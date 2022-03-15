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

api_id = input("Введите api_id: ") #Введите api_id
api_hash = input("Введите api_hash id: ") #Введите api_hash id
phone = input("Введите номер телефона с кодом страны, пример: +79999999999: ") #Введите номер телефона с кодом страны, пример: +79999999999
client = TelegramClient(phone, api_id, api_hash)
async def main():
    await client.send_message('me', 'Привет !!!!')



SLEEP_TIME_1 = 100
SLEEP_TIME_2 = 100

with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('40779'))

users = []
with open(r"Scrapped.csv", encoding='UTF-8') as f:  
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print('Выберите чат:')
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1

g_index = input("Введите число: ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = int(2)

n = 0

for user in users:
    n += 1
    if n % 80 == 0:
        sleep(60)
    try:
        print("Добавляю {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Ошибка. Повторите попытку.")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Жду 60-180 секунд...")
        time.sleep(random.randrange(60, 90))
    except PeerFloodError:
        print("Ошибка флуда, лучше повторить попытку позже.")
        print("Жду {} секунд".format(SLEEP_TIME_2))
        time.sleep(SLEEP_TIME_2)
    except UserPrivacyRestrictedError:
        print("Нельзя добавить участника. Пропускаю.")
        print("Жду 5 секунд...")
        time.sleep(random.randrange(5, 0))
    except:
        traceback.print_exc()
        print("Ошибка")
        continue
