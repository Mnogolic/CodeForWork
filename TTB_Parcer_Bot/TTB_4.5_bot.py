import telebot
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class ClassSpecMapper:  # Класс - словарь для удобства обращения вывел отдельно
    # Сопоставление классов к английскому названию
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
    # Сопоставление русских названий специализаций к английскому названию
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


class TrinketFetcher:  # Класс специально под selenium
    # Как мы будем обращаться к классу - словарю
    def __init__(self):
        self.class_spec_mapper = ClassSpecMapper()

    def top_from_link(self, url):  # Открывает динамически bloodmallet, чтоб мы получили номер предмета
        # номер предмета нам нужен, чтоб открыть его уже на сайте wowhead
        # К сожалению придётся парсить каждый раз так, JS, без Dev API
        chrome_options = Options()  # Стандартные настройки, как я понял чтоб браузер не высплывал на экране
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Указываю где расположен мой дравйер, с помощью которого и будем открывать нужную страницу
        driver_path = ('C:\\Users\\kasja\\.wdm\\drivers\\chromedriver\\win64\\130.0.6723.91\\chromedriver-win32'
                       '\\chromedriver.exe')
        # Применяем к дрйверу эту настройку
        driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

        start_time = time.time()
        print(f'Время получение запроса - {datetime.now()}')
        try:
            driver.get(url)
            # Продолжим выполнение только если страница прогрузится, на ожидание 10 сек
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'chart')))
            time.sleep(0.8)

            html = driver.page_source  # Сохраним код всей страницы
            soup = BeautifulSoup(html, 'lxml')  # Обрабатываем код с помощью парсера
            chart_div = soup.find('div', id='chart')  # Ищем по id-шнику 'chart'

            trinkets = []
            if chart_div:
                # Сайт там крайне тупой, он берёт имена с другого сайта, на сайте это имена - гиперссылки на этом
                # сайте нормально язык поменять нельзя, так что придётся идти по гиперссылке, меняя яызк уже на нём
                links = chart_div.find_all('a', href=True)
                i = 0
                for link in links[1:11]:
                    link_href = link['href']
                    # меняем язык страницы на русский, так же нам нужен только номер предмета, например
                    # "https://www.wowhead.com/item=133300"
                    # нам нужно поменять её на
                    # "https://www.wowhead.com/ru/item=133300/"
                    ru_link = f'https://www.wowhead.com/ru/item={link_href.split('=')[1]}/'
                    trinkets.append(ru_link)  # А вот и ссылка на wowhead с нужным предметом
                    i += 1
                    print(f'{i} - {ru_link} |||||| {link}')
                print('КОНЕЦ ЗАПРОСА\n\n')
            else:
                print('Div с id "chart" не найден.')

            return [self.fetch_trinket_name(url) for url in trinkets]  # Возвращаем имена тринкетов уже на русском
        finally:  # Исполняется в любом случае
            driver.quit()
            elapsed_time = time.time() - start_time
            print(f"[{datetime.now()}] Время выполнения запроса: {elapsed_time:.2f} секунд.")

    @staticmethod
    def fetch_trinket_name(url):  # Ф
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            title_tag = soup.title
            if title_tag and title_tag.string:  # Проверим: существует ли тег страницы, есть ли в нём string
                title_text = title_tag.string.strip()  # избавимся от лишних пробелов
                parts = title_text.split(' - ')

                return parts[0].strip() if parts else None
        except requests.RequestException:
            print("Ошибка при запросе к fetch_trinket_name")
        return None


class DataRetriever:  # Класс для перехода на правильную ссылку, так же учёт
    def __init__(self):  # сленговых наименований классов и специализаций
        self.class_spec_mapper = ClassSpecMapper()

    def get_data_from_website(self, class_type, spec, patch_number):
        base_url = 'https://bloodmallet.com/chart'
        class_type = self.class_spec_mapper.class_mapping.get(class_type, class_type)
        spec = self.map_spec(class_type, spec)
        # на bloodmallet если кол-во таргетов не указано, то кол-во таргетов - 1 (написал исключение)
        patch = 'castingpatchwerk' if patch_number == '1' else f'castingpatchwerk{patch_number}'
        url = f'{base_url}/{class_type}/{spec}/trinkets/{patch}'

        response = requests.get(url)
        if response.status_code == 200:
            return url
        else:
            return 'Не удалось получить данные с сайта'

    def map_spec(self, class_type, spec):  # Логика определения сленговых названий классов, в игре
        # Рыцарь смерти кровь == бдк == дк танк
        if (class_type == 'warrior') and (spec in ['танк', 'защита', 'прот']):
            return 'protection'
        elif (class_type == 'paladin') and (spec in ['танк', 'защита', 'прот']):
            return 'protection'
        elif (class_type == 'demon_hunter') and (spec == 'танк'):
            return 'vengeance'
        elif (class_type == 'monk') and (spec == 'танк'):
            return 'brewmaster'
        elif (class_type == 'death_knight') and (spec == 'танк'):
            return 'blood'
        return self.class_spec_mapper.spec_mapping.get(spec, spec)


class TelegramBot:
    def __init__(self, token):
        # То как мы обращаемся к другим классами, и к самим функциям
        self.bot = telebot.TeleBot(token)
        self.trinket_fetcher = TrinketFetcher()
        self.data_retriever = DataRetriever()

        self.bot.message_handler(commands=['start', 'help'])(self.send_welcome)
        self.bot.message_handler(commands=['info'])(self.send_info)

    def send_welcome(self, message):
        self.bot.reply_to(message,
                          "Привет! Напиши команду в формате /info <класс> <спек> <кол-во таргетов>, чтобы получить "
                          "информацию.\nПример: /info разбойник ликвидация 1\nили сокращённо: /info рога лика 1")

    def send_info(self, message):
        try:
            class_type, spec, patch_number = message.text.split()[1:4]
            url = self.data_retriever.get_data_from_website(class_type, spec, patch_number)
            # Приветственное сообщение, пользователю, с просьбой подождать
            self.bot.reply_to(message, 'Привет пользователь, дай мне пол минуты собрать актуальные данные с сайта'
                                       ' ,вот пока тебе ссылка откуда я собираю данные: ' + url)

            top_trinkets = self.trinket_fetcher.top_from_link(url)  # Идём по ссылке собирать данные
            # Пронумируем (составим топ тринек)
            print(f'[{datetime.now()}] время начала формирования сообщения')
            top_trinkets_text = '\n'.join([f"{i + 1} - {trinket}" for i, trinket in enumerate(top_trinkets)])
            self.bot.reply_to(message, f'Топ тринкетов для {class_type} {spec}:\n\n' + top_trinkets_text)
            print(f"[{datetime.now()}] время, когда запрос ушёл в тг\n\n")
        except ValueError:
            self.bot.reply_to(message, "Неверный формат команды. Используйте: /info <класс> <спек> <кол-во таргетов>.")

    def start(self):

        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    TOKEN = 'TG_Token'
    bot = TelegramBot(TOKEN)
    bot.start()
