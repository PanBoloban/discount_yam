import schedule
# from itertools import count
from vk import zapusk
from constant import HOST, NAME_BD, PASSW_HOST, USER_LOG_HOST, API_ID, API_HASH, CHANNEL_ID, MY_URL, MY_URL_2, TOKEN_VK, GROUP_VK_ID


def main():    
    ''' Функция для автозапуска кода по рассписаниею '''
    schedule.every(2).minutes.do(zapusk)

    while True:
        schedule.run_pending() 



if __name__ == '__main__':
    main()
    