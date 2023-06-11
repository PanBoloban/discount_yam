import vk_api
from telethon import TelegramClient, events, sync
from main import main
from constant import TOKEN_VK, API_ID, API_HASH, CHANNEL_ID, GROUP_VK_ID


def post_to_vk_group(access_token, group_id, text):
    # Создаем сессию VK API
    vk_session = vk_api.VkApi(token=access_token)
    vk = vk_session.get_api()

    # Отправляем сообщение в группу ВКонтакте
    vk.wall.post(owner_id='-' + group_id, message=text)
    print(' напечатал в вк ')


# Вставьте свои API_ID и API_HASH
api_id = API_ID
api_hash = API_HASH

# Создание объекта клиента
client = TelegramClient('session_name_for_vk', api_id, api_hash)

# Связываем обработчик сообщений, который будет вызываться при получении новых сообщений
@client.on(events.NewMessage(chats=CHANNEL_ID))
async def my_event_handler(event):
    # Вызов функции
    print('dspsdf.')
    post_to_vk_group(access_token=TOKEN_VK,group_id=GROUP_VK_ID,text='экскаватор_2')
    print(' работаю ')
    main()
    # await client.send_message(event.chat_id, 'Сообщение получено и обработано!') # отправляет сообщение обратно в канал


def waiting_message():
    # Запускаем клиента
    client.start()
    client.run_until_disconnected()

waiting_message()


