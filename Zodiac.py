# Программа для получения информации о гороскопах с веб-сайта (используя библиотеки requests и beautifulsoup),
# и создания общего гороскопа на основе этих данных с использованием библиотеки markovify.
# Программа использует мультипроцессинг для ускорения получения информации с 12 интернет страниц.
# Текст переводится на английский язык перед созданием модели, для лучшей работы алгоритма.

import markovify
import bs4
import requests
from multiprocessing import Pool
from deep_translator import GoogleTranslator


# Функция для обработки гороскопов по знакам зодиака
def f (str):
	text_zodiac = ""
	# Запрос к веб-сайту для получения гороскопа по указанному знаку зодиака
	html = requests.get('https://horo.mail.ru/prediction/' + str + '/today/')
	zodiac_soup = bs4.BeautifulSoup(html.text, features="html.parser")
	goroskops = zodiac_soup.findAll('p')
	
	# Обработка текста гороскопа
	if len(goroskops) > 0:
		for goroskop in goroskops:
			text_zodiac += goroskop.text
	# Перевод гороскопа на английский с использованием Google Translator
	translated = GoogleTranslator(source='auto', target='en').translate(text_zodiac)
	return translated


# Список знаков зодиака
Zodiac = ['aries',
          'taurus',
          'gemini',
          'cancer',
          'leo',
          'virgo',
          'libra',
          'scorpio',
          'sagittarius',
          'capricorn',
          'aquarius',
          'pisces']
text_zodiac = ''

if __name__ == '__main__':
	print("Анализ положения звёзд...")
	# Использование мультипроцессинга для ускорения получения гороскопов
	with Pool(5) as p:
		texts = p.map(f, Zodiac)
	
	print('\n Пять гороскопов на сегодня: ')
	# Объединение текстов гороскопов
	for text in texts:
		text_zodiac += text
	
	# Создание модели markovify на основе общего гороскопа
	text_model = markovify.Text(text_zodiac, state_size=5)
	# Генерация пяти предложений с использованием markovify
	for i in range(5):
		sentence = text_model.make_sentence(tries=1000, test_output=False)
		# Перевод предложения на русский с использованием Google Translator
		translated = GoogleTranslator(source='auto', target='ru').translate(sentence)
		print(str(i + 1) + '. ' + translated)