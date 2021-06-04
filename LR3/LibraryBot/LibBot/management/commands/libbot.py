from django.core.management.base import BaseCommand
from LibraryBot import settings
import telebot
from ...models import Book, Author, Genre
from ...db import db


class Command(BaseCommand):
	_user_state = dict()

	def handle(self, *args, **options):
		bot = telebot.TeleBot(settings.TOKEN)


		@bot.message_handler(commands=['start'])
		def send_welcome(message):

			bot.send_message(message.from_user.id, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')


		@bot.message_handler(commands=['help'])
		def send_help(message):

			bot.send_message(message.from_user.id, f'Я студенческий проект-телеграм бот для библиотеки)')


		@bot.message_handler(commands=['authorize'])
		def send_authtorization(message):

			self._user_state.update({f'{message.from_user.id}':f'authorize'})
			bot.send_message(message.from_user.id, f'Введите данные по шаблону:\nФамилия Имя Отчество Адрес Номер_телефона.')


		@bot.message_handler(commands=['book'])
		def search_books(message):

			self._user_state.update({f'{message.from_user.id}':f'book'})
			bot.send_message(message.from_user.id, 'Введите название книги')


		@bot.message_handler(commands=['author'])
		def search_author_books(message):

			self._user_state.update({f'{message.from_user.id}':f'author'})
			bot.send_message(message.from_user.id, 'Введите фамилию и имя автора через пробел')


		@bot.message_handler(content_types=['text'])
		def get_text_messages(message):

			state = self._user_state.get(f'{message.from_user.id}')

			if message.text.lower().find('привет') != -1 and message.text.find('?') == -1:
				bot.send_message(message.from_user.id, 'Привет!')

			elif state == 'book':
				self._user_state.pop(f'{message.from_user.id}')
				book_set = db._search_book_title(message.text)

				if book_set is None:
					bot.send_message(message.from_user.id, 'В библиотеке нет книг с таким названием.')
					return

				for book_list in book_set:
					author = Author()
					author.from_list(db._get_author(book_list[2]))
					genre = Genre()
					genre.from_list(db._get_genre(book_list[3]))
					book = Book()
					book.from_list(book_list, author, genre)
					bot.send_message(message.from_user.id, str(book))

			elif state == 'author':

				try:
					space = message.text.find(' ')
					surname = message.text[0: space]
					name = message.text[space + 1: len(message.text)]

				except IndexError:
					bot.send_message(message.from_user.id, 'Введите фамилию и имя автора через пробел') 
					return

				self._user_state.pop(f'{message.from_user.id}')
				author_set = db._search_author(surname, name)
				author_id = 0

				if author_set is None or author_set[0] == 0:
					bot.send_message(message.from_user.id, 'Нет такого автора') 
					return

				else:
					author_id = author_set[0]

				author = Author()
				author.author_id = author_id
				author.surname = surname
				author.name = name
				book_set = db._search_author_books(author_set[0])
				
				for book_list in book_set:
					genre = Genre()
					genre.from_list(db._get_genre(book_list[3]))
					book = Book()
					book.from_list(book_list, author, genre)
					bot.send_message(message.from_user.id, str(book)) 

			elif state == 'authorize':

				text = message.text.split(' ')

				try:
					surname = text[0]
					name = text[1]
					patronymic = text[2]
					address = text[3]
					phone = int(text[4])

				except IndexError:
					bot.send_message(message.from_user.id, 'Неправильный ввод.')
					bot.send_message(message.from_user.id, f'Введите данные по шаблону:\nФамилия Имя Отчество Адрес Номер_телефона.')
					return

				except ValueError:
					bot.send_message(message.from_user.id, 'Неправильный ввод. Номер телефона должен быть числом')
					return

				self._user_state.pop(f'{message.from_user.id}')

				if db._is_authorized(message.from_user.id):
					bot.send_message(message.from_user.id, 'Вы уже авторизованы.')

				else:
					# authorization
					reader_id = db._get_reader_id(surname, phone)

					if reader_id != 0:
						result = db._add_telegram_reader(reader_id, message.from_user.id)

					else:
						db._add_reader(surname, name, patronymic, address, phone)
						reader_id = db._get_reader_id(surname, phone)
						result = db._add_telegram_reader(reader_id, message.from_user.id)
					bot.send_message(message.from_user.id, 'Авторизация прошла успешно. '+
					  f'Ваш пароль {reader_id*1000 + int(phone/10000)}.')

			else:
				bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')

		bot.polling(none_stop=True)