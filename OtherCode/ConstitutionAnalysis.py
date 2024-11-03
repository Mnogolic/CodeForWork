import fitz  # PyMuPDF
import os

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import FreqDist
import nltk

import re


class PdfToTxt:
    constitution_path = r"C:\Users\kasja\PycharmProjects\CodeForWork\Constitution_RF_12.11.1.pdf"
    constitution_txt_path = r"C:\Users\kasja\PycharmProjects\CodeForWork\Constitution_RF_12.11.1.txt"

    def __init__(self):
        pass

    def if_txt_doesnt_exists(self):
        # Проверка существования текстового файла
        print('\n')
        if not os.path.isfile(self.constitution_txt_path):
            print("Текстовый файл не найден. Создаю копию...\n")

            # Открываем PDF и извлекаем текст
            with fitz.open(self.constitution_path) as pdf_document:
                text = ""
                for page_num in range(pdf_document.page_count):
                    page = pdf_document[page_num]
                    text += page.get_text()

            # Сохраняем текст в файл .txt
            with open(self.constitution_txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)

            print(f"Файл успешно создан по адресу {self.constitution_txt_path}")
        else:
            print("Текстовый файл уже существует.")

    def check_file_pathes(self):
        print('\n')
        # Проверка существования PDF-файла
        if os.path.isfile(self.constitution_path):
            print(f"Файл <Constitution_RF_12.11.1.pdf> существует по адресу - {self.constitution_path}\n")
        else:
            print(f"Файл <Constitution_RF_12.11.1.pdf> не найден.\n")

        # Проверка существования TXT-файла
        if os.path.isfile(self.constitution_txt_path):
            print(f"Файл <Constitution_RF_12.11.1.txt> существует по адресу - {self.constitution_txt_path}\n")
        else:
            print(f"Файл <Constitution_RF_12.11.1.txt> не найден.\n")
            self.if_txt_doesnt_exists()  # Создаем файл, если его нет
            self.check_file_pathes()  # Рекурсивно проверяем снова


class FunctionsWithFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.stop_words = set(stopwords.words('russian'))

    # Передача куда угодно переменной с записанным в неё файлом
    def read_our_txt(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            text = file.read()

        return text

    def split_articles(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Используем регулярное выражение для поиска статей
        articles = re.split(r'(Статья \d+)', text)

        # Объединяем номера статей с текстом статей
        articles = [f"{articles[i]}{articles[i + 1]}" for i in range(1, len(articles) - 1, 2)]

        return articles

    def top_ten_words(self):
        # Токенизация текста
        words = word_tokenize(self.read_our_txt(), language='russian')

        #   isalpha - проверка только рус букв
        filtered_words = [
            word for word in words
            if (re.match(r'^[а-яА-ЯёЁ]+$', word) and word.lower()
                not in self.stop_words)

        ]

        # Подсчет частоты слов
        freq_dist = FreqDist(filtered_words)
        most_common_words = freq_dist.most_common(10)  # 10 самых распространенных слов

        # Вывод результатов
        print("10 самых распространенных слов:")
        for word, frequency in most_common_words:
            print(f"{word}: {frequency}")

    def constitution_news(self):
        articles = self.split_articles()
        for article in articles:
            if 'конституция' in article.lower() or 'конституции' in article.lower():
                print(article)
                print("\n\n" + "=" * 60 + "\n" + "=" * 60 + "\n\n")


""" 
if __name__ == '__main__':
    analysis = PdfToTxt()
    analysis.check_file_pathes()
"""

if __name__ == '__main__':
    nltk.download('popular')
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')

    analysis = PdfToTxt()
    functions = FunctionsWithFile(analysis.constitution_txt_path)

    analysis.check_file_pathes()
    # Выполняем анализ текста после создания файла
    functions.top_ten_words()
    functions.constitution_news()
