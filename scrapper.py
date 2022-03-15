from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = input("Введите api_id: ") #Введите api_id
api_hash = input("Введите api_hash id: ") #Введите api_hash id
phone = input("Введите номер телефона с кодом страны, пример: +79999999999: ") #Введите номер телефона с кодом страны, пример: +79999999999
client = TelegramClient(phone, api_id, api_hash)
async def main():
    await client.send_message('me', 'Привет !!!!')
with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Введите код подтверждения: '))


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

print('Выберите чат, из которого хотите получить список участников:')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input("Введите число: ")
target_group=groups[int(g_index)]

print('Получаю участников...')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=False)

print('Сохраняю в файл...')
with open("Scrapped.csv","w",encoding='UTF-8') as f:#Enter your file name.
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
print('Успешно записал все данные в файл.......')
