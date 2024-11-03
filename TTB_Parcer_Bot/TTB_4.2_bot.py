import telebot
import requests
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

bot = telebot.TeleBot('TG_Token')

# Сопоставление классов и специализаций

class_mapping = {
    'разбойник': 'rogue', 'рога': 'rogue', 'пират': 'rogue',
    'охотник': 'hunter', 'хант': 'hunter',
    'жрец': 'priest', 'прист': 'priest',
    'шаман': 'shaman', 'шам': 'shaman',
    'воин': 'warrior', 'вар': 'warrior', 'протовар': 'protection', 'протвар': 'protection',
    'паладин': 'paladin', 'пал': 'paladin', 'протпал': 'protection', 'протопал': 'protection',
    'маг': 'mage',
    'чернокнижник': 'warlock', 'лок': 'warlock',
    'монах': 'monk', 'монк': 'monk',
    'друид': 'druid', 'дру': 'druid',
    'дх': 'demon_hunter', 'охотник_на_демонов': 'demon_hunter', 'пидр': 'demon_hunter', 'хавок': 'demon_hunter',
    'дк': 'death_knight', 'рыцарь_смерти': 'death_knight', 'бдк': 'death_knight',
    'дракон': 'evoker', 'пробудитель': 'evoker', 'опустошитель': 'evoker', 'девостейшен': 'evoker',
    'девостатор': 'evoker', 'девастейшен': 'evoker'
}

spec_mapping = {
    #   рога
    'ликвидация': 'assassination', 'яд': 'assassination',
    'головорез': 'outlaw', 'пират': 'outlaw',
    'скрытность': 'subtlety', 'шд': 'subtlety',
    #   вар
    'армс': 'arms', 'оружие': 'arms',
    'неистовство': 'fury', 'фури': 'fury', 'фурик': 'fury',
    'протовар': 'protection', 'протвар': 'protection',
    #   маг
    'лёд': 'frost', 'лед': 'frost',
    'тайная_магия': 'arcane', 'аркан': 'arcane',
    'фаер': 'fire', 'огонь': 'fire',
    #   лок
    'разрушение': 'destruction', 'дестр': 'destruction',
    'демонология': 'demonology', 'демон': 'demonology',
    'колдовство': 'affliction', 'афлик': 'affliction', 'афли': 'affliction',
    #   дк
    'кровь': 'blood', 'блад': 'blood', 'бдк': 'blood',
    'нечестивость': 'unholy', 'анхоли': 'unholy', 'анхолик': 'unholy',
    #   дру
    'страж': 'guardian', 'медведь': 'guardian',
    'сила_зверя': 'feral', 'кот': 'feral', 'ферал': 'feral', 'рыжик': 'feral',
    'баланс': 'balance', 'сова': 'balance', 'балон': 'balance', 'мун': 'balance', 'мункен': 'balance',
    #   пал
    'воздаяние': 'retribution', 'дд': 'retribution',
    'протопал': 'protection', 'протпал': 'protection',
    #   хант
    'мм': 'marksmanship', 'стрельба': 'marksmanship',
    'бм': 'beast_mastery', 'повелитель_зверей': 'beast_mastery',
    'выживание': 'survival', 'сурв': 'survival',
    #   прист
    'тьма': 'shadow', 'шп': 'shadow', 'тень': 'shadow', 'дпс': 'shadow',
    #   шам
    'стихии': 'elemental', 'энх': 'elemental',
    'совершенствование': 'enhancement', 'стихия': 'enhancement',
    #   дх
    'истребление': 'havoc', 'хавок': 'havoc',
    'месть': 'vengeance', 'вндженс': 'vengeance',
    #   дракон
    'опустошитель': 'devastation', 'девостейшен': 'devastation', 'девостатор': 'devastation',
    'девастейшен': 'devastation',
    #   монк
    'хмелевар': 'brewmaster', 'брю': 'brewmaster',
    'танцующий_с_ветром': 'windwalker', 'вв': 'windwalker', 'виндвейкер': 'windwalker', 'винд_вейкер': 'windwalker'
}


def fetch_trinket_name(url_trinket_name):
    try:
        response = requests.get(url_trinket_name)
        html_trinket_name = response.text
        soup_trinket_name = BeautifulSoup(html_trinket_name, 'lxml')
        # Очистка строчки:
        # Получение текста из тега <title>
        title_tag = soup_trinket_name.title
        if title_tag and title_tag.string:
            title_text = title_tag.string.strip()
            # Очистка строки
            parts = title_text.split(' - ')
            cleaned_name = None
            if parts[0].strip() is not None:
                cleaned_name = parts[0].strip()
        return cleaned_name

    except requests.RequestException as e:
        print(f"Ошибка при запросе к  fetch_trinket_name")
        return None


def top_from_link(data):
    # Настройка Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск браузера без графического интерфейса
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Инициализация веб-драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # URL страницы
    url = data
    # Загрузка страницы
    print(url)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'chart')))
    except Exception as e:
        print(f"Ошибка при загрузке страницы: {e}")
        driver.quit()
        return []
    print(url, '\n')

    # Дайте странице время на загрузку и выполнение JavaScript
    """ 
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'chart'))
    )
    """
    time.sleep(0.7)  # Увеличьте время ожидания, если нужно

    # Получите HTML страницы
    html = driver.page_source
    driver.quit()

    # Проанализируйте HTML с BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')

    # Найдите div с id 'chart'
    chart_div = soup.find('div', id='chart')

    trinkets = []
    # Проверьте, найден ли div с id 'chart'
    if chart_div:
        # Найдите все ссылки внутри найденного div
        links = chart_div.find_all('a', href=True)
        print(f'links: {links}')
        for link in links[1:11]:
            print(f'\tlink: {link}')
            # Переделка ссылки в русский
            link_href = link['href']
            ru_link = f'https://www.wowhead.com/ru/item={link_href.split('=')[1]}/'

            print('Найденная ссылка:', link['href'], 'и Ру версия:', ru_link)
            trinkets.append(ru_link)
    else:
        print('Div с id "chart" не найден.')

    names = []
    for url_trinket_name in trinkets:
        names.append(fetch_trinket_name(url_trinket_name))
    return names


def get_data_from_website1(class_type, spec, patch_number):
    base_url = 'https://bloodmallet.com/chart'

    class_type = class_mapping.get(class_type, class_type)
    # исправление логики
    if (class_type == 'warrior') and ((spec == 'танк') or (spec == 'защита') or (spec == 'прот')):
        spec = 'protection'
    elif (class_type == 'paladin') and ((spec == 'танк') or (spec == 'защита') or (spec == 'прот')):
        spec = 'protection'
    elif (class_type == 'demon_hunter') and (spec == 'танк'):
        spec = 'vengeance'
    elif (class_type == 'monk') and (spec == 'танк'):
        spec = 'brewmaster'
    elif (class_type == 'death_knight') and (spec == 'танк'):
        spec = 'blood'
    else:
        spec = spec_mapping.get(spec, spec)

    patch = 'castingpatchwerk' if patch_number == '1' else f'castingpatchwerk{patch_number}'
    url = f'{base_url}/{class_type}/{spec}/trinkets/{patch}'

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.text
        # return f'URL: {url}\nTitle: {title}'
        return url
    else:
        return 'Не удалось получить данные с сайта'


def get_data_from_website2(class_spec, patch_number):
    base_url = 'https://bloodmallet.com/chart'

    class_type = class_mapping.get(class_spec, class_spec)
    spec = spec_mapping.get(class_spec, class_spec)

    patch = 'castingpatchwerk' if patch_number == '1' else f'castingpatchwerk{patch_number}'
    url = f'{base_url}/{class_type}/{spec}/trinkets/{patch}'

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.text
        # return f'URL: {url}\nTitle: {title}'
        return url
    else:
        return 'Не удалось получить данные с сайта'


# комманды /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print("Команда /start или /help получена")
    bot.reply_to(message,
                 "Привет! Напиши команду в формате /info <класс> <спек> <кол-во таргетов>, чтобы получить "
                 "информацию.\nПример: /info разбойник ликвидация 1\nили сокращённую версию\n"
                 "Пример: /info бдк 3"

                 )


# комманда /info
@bot.message_handler(commands=['info'])
def send_info(message):
    try:
        command_params = message.text.split()
        if len(command_params) == 4:
            class_type = command_params[1].lower()
            spec = command_params[2].lower()
            patch_number = command_params[3]
            if patch_number not in ['1', '3', '5']:
                raise ValueError("Кол-во таргетов должно быть 1, 3 или 5.")
            data = get_data_from_website1(class_type, spec, patch_number)

            # Ссылочка, что бне скучал
            bot.send_message(message.chat.id, 'Дай пол минуты, я выведу тебе топ 10 тринек\nвот, пока ссылка на '
                                              'bloodmallet: ' + data)

            top_trinkets_array = top_from_link(data)
            # top_trinkets_text = '\n'.join(top_trinkets_array)
            # Cоставляем топ тринек
            top_trinkets_text = f'{command_params[1]}, {command_params[2]}, кол-во таргетов: {command_params[3]}:\n'
            for index, item in enumerate(top_trinkets_array, start=1):
                top_trinkets_text += f'\tтоп {index} - {item}\n'
                print(top_trinkets_text)

        elif len(command_params) == 3:
            class_spec = command_params[1].lower()
            patch_number = command_params[2]
            if patch_number not in ['1', '3', '5']:
                raise ValueError("Кол-во таргетов должно быть 1, 3 или 5.")
            data = get_data_from_website2(class_spec, patch_number)

            # Ссылочка, что бне скучал
            bot.send_message(message.chat.id, 'Дай пол минуты, я выведу тебе топ 10 тринек\nвот, пока ссылка на '
                                              'bloodmallet:' + data)

            top_trinkets_array = top_from_link(data)
            # top_trinkets_text = '\n'.join(top_trinkets_array)
            # Cоставляем топ тринек
            top_trinkets_text = f'{command_params[1], command_params[2]}:\n'
            top_trinkets_text = f'{command_params[1]} кол-во таргетов - {command_params[2]}:\n'
            for index, item in enumerate(top_trinkets_array, start=1):
                top_trinkets_text += f'\tтоп {index} - {item}\n'
        else:
            raise IndexError

        bot.send_message(message.chat.id, top_trinkets_text)

    except IndexError:
        bot.send_message(message.chat.id,
                         "Пожалуйста, используйте формат команды: /info <класс> <спек> <кол-во "
                         "таргетов>\nПример:\n/info рыцарь_смерти кровь 1\n/info дк танк 3\n/info бдк 5")
    except ValueError as ve:
        bot.send_message(message.chat.id, str(ve))
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')


bot.polling(none_stop=True)
