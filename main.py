from telethon.sync import TelegramClient
from itertools import count
import pymysql
import schedule
from constant import HOST, NAME_BD, PASSW_HOST, USER_LOG_HOST, API_ID, API_HASH, CHANNEL_ID, MY_URL, MY_URL_2



def telegram_scraper_one():
    ''' Получаем текст последнего сообщения телеграмм канала ЯМ, меняем ссылку на свою '''

    # Создаем экземпляр клиента
    client = TelegramClient('session_name', api_id=API_ID, api_hash=API_HASH)

    # Авторизуемся в Telegram
    client.start()

    #Находим канал по его названию
    channel = client.get_entity(CHANNEL_ID)

    # Выводим список последних 1 сообщений из канала в обратном порядке (последнее сообщение в начале)
    messages = client.iter_messages(channel, limit=1)
    messages = reversed(list(messages))
    # Перебираем сообщение и забираем ссылки из него
    new_message = str()
    for message in messages:
        sentence = message.message
        url = 'https://market.yandex.ru'
        sentence_new = sentence.replace('\n\xa0\n', '<p><br></p>').replace('\n', ' ') # меняем абзац в телеграмме на абзац в html, и перенос на пробел
        words = sentence_new.split(' ')  # Разбиваем предложение на отдельные слова
        # words = sentence.split()  # Разбиваем предложение на отдельные слова
        for word_1 in words:
            word = word_1.replace("'", "")
            if url in word:
                if '?' in word:
                    my_url_word = word.strip() + MY_URL_2 # добавялем свою уникальную ссылку
                    new_message = new_message.rstrip() + '<p>Ссылка: ' + f'<a href="{my_url_word}" rel="sponsored" target="_blank">{my_url_word}</a>' + '</p>'
                else:
                    my_url_word = word.strip() + MY_URL # добавялем свою уникальную ссылку
                    new_message = new_message.rstrip() + '<p>Ссылка: ' + f'<a href="{my_url_word}" rel="sponsored" target="_blank">{my_url_word}</a>' + '</p>'
            else:
                new_message = new_message + ' ' + word

# Сохраняем полученные сообщения в файл
# with open('messages.txt', 'w', encoding='utf-8') as f:
#     for message in messages:
#         f.write(f'{message.message}\n')
#         print(f'{message.message}\n')

    # Останавливаем клиента
    client.disconnect()
    my_new_message = '<p><br></p>' + new_message
    return my_new_message


def telegram_scraper_two():
    ''' Получаем текст последнего сообщения телеграмм канала ЯМ, меняем ссылку на свою '''

    # Создаем экземпляр клиента
    client = TelegramClient('session_name', api_id=API_ID, api_hash=API_HASH)

    # Авторизуемся в Telegram
    client.start()

    #Находим канал по его названию
    channel = client.get_entity(CHANNEL_ID)

    # Выводим список последних 1 сообщений из канала в обратном порядке (последнее сообщение в начале)
    messages = client.iter_messages(channel, limit=2)
    messages = reversed(list(messages))
    new_message = str()
    for message in messages:
        sentence = message.message
        url = 'https://market.yandex.ru'
        sentence_new = sentence.replace('\n\xa0\n', '<p><br></p>').replace('\n', ' ') # меняем абзац в телеграмме на абзац в html, и перенос на пробел
        words = sentence_new.split(' ')  # Разбиваем предложение на отдельные слова
        for word_1 in words:
            word = word_1.replace("'", "")
            if url in word:
                if '?' in word:
                    my_url_word = word.strip() + MY_URL_2 # добавялем свою уникальную ссылку
                    new_message = new_message.rstrip() + '<p>Ссылка: ' + f'<a href="{my_url_word}" rel="sponsored" target="_blank">{my_url_word}</a>' + '</p>'
                else:
                    my_url_word = word.strip() + MY_URL # добавялем свою уникальную ссылку
                    new_message = new_message.rstrip() + '<p>Ссылка: ' + f'<a href="{my_url_word}" rel="sponsored" target="_blank">{my_url_word}</a>' + '</p>'
            else:
                new_message = new_message + ' ' + word

# Сохраняем полученные сообщения в файл
# with open('messages.txt', 'w', encoding='utf-8') as f:
#     for message in messages:
#         f.write(f'{message.message}\n')
#         print(f'{message.message}\n')

    # Останавливаем клиента
    client.disconnect()
    my_new_message = '<p><br></p>' + new_message
    one_text = telegram_scraper_one()
    one_text = one_text.replace('<p><br></p>', '')
    my_new_message = my_new_message.replace(one_text, '')  # убераем текст последнего сообщения и оставляем текст предыдущего сообщения
    return my_new_message

def check_message_for_keywords(message, list_controller):
    ''' Функция для проверки не нужных сообщений '''
    for keyword in list_controller:
        if keyword.lower() in message.lower():
            return True
    return False


def insert_text_after(string, insert_text, target):
    ''' Добавляем сообщение с телеграм в текст сайта '''
    index = string.find(target) + len(target)
    return string[:index] + insert_text + string[index:]


'''********************** Соединение с БД и вывод текста с страницы скидок ******************'''

def connect_bd_skidka(text_telegram):
    try:
        connection = pymysql.connect(
            host=HOST,
            port=3306,
            user=USER_LOG_HOST,
            password=PASSW_HOST,
            database=NAME_BD,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            '''************* Выборка артикул=цена  *************'''
            with connection.cursor() as cursor:
                select_status = "SELECT shop_page.id, shop_page.content FROM `shop_page`"
                cursor.execute(select_status)
                rows = cursor.fetchall()
                text_skidka = rows[0]['content'].split() # забераем первый словарь из списка, по ключу забераем текст, разбиваем на слова и переводим в список
                text_skidka_proverka = ' '.join(text_skidka)
                list_controller = ['Уважаемые партнеры', 'партнеры', 'вознаграждения', 'тарифах', 'тариф', 'тарифами', 'трафика', 'трафик', 'Справке'] # создаем список для проверки не нужных сообщений
                text_indikator = '20px;">Актуальные_Скидки:</span></strong></p>' # текст после которого будет вставлятся наш текст с телеграм
                new_text_site = ''
                text_telegram_proverka = ' '.join(text_telegram.split())
                if text_telegram_proverka in text_skidka_proverka:
                    print(' Скидка 1 указана на сайте ')
                    pass
                elif check_message_for_keywords(text_telegram, list_controller) == True:
                    print(' В сообщении 1 от телеграмм есть стоп слово ')
                    pass
                else:
                    new_text_site = insert_text_after(text_skidka_proverka, text_telegram, text_indikator)

        finally:
            connection.close()
    
    except Exception as ex:
        print('Connection refused...')
        print(ex)
    
    print(len(new_text_site))
    if len(new_text_site) == 0:
        return text_skidka_proverka
    else:    
        return new_text_site


def text_zapis(value, key=1):
    ''' Записываем данные в БД '''
    try:
        connection = pymysql.connect(
            host=HOST,
            port=3306,
            user=USER_LOG_HOST,
            password=PASSW_HOST,
            database=NAME_BD,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            '''************* записываем данные в бд  *************'''
            with connection.cursor() as cursor:
                update_query = "UPDATE shop_page SET content = '%s' WHERE id = '%s'"
                cursor.execute(update_query %(value,key))
                connection.commit()
                print(f'Конец, УРА!')
        finally:
            connection.close()

    except Exception as ex:
        print('Connection refused...')
        print(ex)


def zapusk():
    text_telegram_one = telegram_scraper_one()
    text_telegram_two = telegram_scraper_two()
    text_telegram_list = [text_telegram_one, text_telegram_two]
    for text_telegram in text_telegram_list:
        text_zapis(connect_bd_skidka(text_telegram), 1)


def main():
    ''' Функция для автозапуска кода по рассписаниею '''
    schedule.every(59).minutes.do(zapusk)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()