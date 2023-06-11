import vk_api
from telethon import TelegramClient, events
from constant import TOKEN_VK, API_ID, API_HASH, CHANNEL_ID, GROUP_VK_ID


# Данные доступа VK API
TOKEN_VK = TOKEN_VK
GROUP_ID = GROUP_VK_ID

# Данные доступа Telegram API
TELEGRAM_API_ID = API_ID
TELEGRAM_API_HASH = API_HASH
# ID вашего канала Telegram
CHANNEL_ID = CHANNEL_ID


# Функция для отправки сообщения в группу VK
def post_to_vk_group(access_token, group_id, text):
    vk_session = vk_api.VkApi(token=access_token)
    vk = vk_session.get_api()
    vk.wall.post(owner_id='-' + group_id, message=text)


# Создаем объект клиента Telegram
client = TelegramClient('session_name', TELEGRAM_API_ID, TELEGRAM_API_HASH)

# Запускаем клиента Telegram
client.start()


# Выполнение процесса авторизации
if not client.is_user_authorized():
    client.send_code_request('<ваш номер телефона>')
    client.sign_in('<ваш номер телефона>', input('Введите код подтверждения: '))
else:
    print(' Уже идетифицирован ')

# Функция для обработки новых сообщений в канале Telegram
@client.on(events.NewMessage(chats=CHANNEL_ID))
async def my_event_handler(event):
    # Вызываем функцию для отправки сообщения в группу VK
    post_to_vk_group(access_token=TOKEN_VK, group_id=GROUP_ID, text='экскаватор_2')
    print('работаю')
    await event.respond('Сообщение получено и обработано!')



# Запуск цикла обработки событий клиента Telegram
client.run_until_disconnected()


