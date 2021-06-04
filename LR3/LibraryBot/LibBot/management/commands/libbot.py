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


		@bot.message_handler(commands=['change'])
		def change_reader_info(message):

			reader_set = db.get_telegram_reader(message.from_user.id)

			if reader_set is None:
				bot.send_message(message.from_user.id, 'Сначала авторизуйтесь.')
				return

			self._user_state.update({f'{message.from_user.id}':f'change'})
			bot.send_message(message.from_user.id, f'Введите данные по шаблону:\nФамилия Имя Отчество Адрес Номер_телефона.')


		@bot.message_handler(commands=['delete'])
		def delete_reader(message):

			reader_set = db.get_telegram_reader(message.from_user.id)

			if reader_set is None:
				bot.send_message(message.from_user.id, 'Вы не авторизованы')
				return

			if db.delete_telegram_reader(reader_set[0]):
				bot.send_message(message.from_user.id, 'Вы удалены из спика читателей, использующих услуги бота.'+
				   'Но Вы все еще считаетесь читателем библиотеки.')
			else:
				bot.send_message(message.from_user.id, 'Не удалось произвести удаление')


		@bot.message_handler(commands=['book'])
		def search_books(message):

			self._user_state.update({f'{message.from_user.id}':f'book'})
			bot.send_message(message.from_user.id, 'Введите название книги, фамилию и имя автора через пробел')


		@bot.message_handler(commands=['author'])
		def search_author_books(message):

			self._user_state.update({f'{message.from_user.id}':f'author'})
			bot.send_message(message.from_user.id, 'Введите фамилию и имя автора через пробел')


		#@bot.message_handler(commands=['pay'])
		#def search_books(message):

		#	self._user_state.update({f'{message.from_user.id}':f'pay'})
		#	bot.send_message(message.from_user.id, 'Введите название книги')


		@bot.message_handler(commands=['mybooks'])
		def search_author_books(message):

			reader_set = db.get_telegram_reader(message.from_user.id)

			if reader_set is None:
				bot.send_message(message.from_user.id, 'Сначала авторизуйтесь.')
				return

			reader_id = reader_set[0]
			books = db.get_list_of_reader_books(0, 5, reader_id)

			if books is None:
				bot.send_message(message.from_user.id, 'Нет книг, которые Вы не вернули')
				return

			bot.send_message(message.from_user.id, 'Книги, которые Вы еще не вернули:')

			for book_list in books:
				author = Author()
				author = Author(db.get_author(book_list[2]))
				genre = Genre()
				genre.from_list(db.get_genre(book_list[3]))
				book = Book()
				book.from_list(book_list, author, genre)
				bot.send_message(message.from_user.id, str(book))


		@bot.message_handler(content_types=['text'])
		def get_text_messages(message):

			state = self._user_state.get(f'{message.from_user.id}')

			if message.text.lower().find('привет') != -1 and message.text.find('?') == -1:
				bot.send_message(message.from_user.id, 'Привет!')

			elif state == 'book':
				self._user_state.pop(f'{message.from_user.id}')
				book_set = db.search_book_title(message.text)

				if book_set is None:
					bot.send_message(message.from_user.id, 'В библиотеке нет книг с таким названием.')
					return

				for book_list in book_set:
					author = Author()
					author.from_list(db.get_author(book_list[2]))
					genre = Genre()
					genre.from_list(db.get_genre(book_list[3]))
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
				author_set = db.search_author(surname, name)
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
				book_set = db.search_author_books(author_set[0])
				
				for book_list in book_set:
					genre = Genre()
					genre.from_list(db.get_genre(book_list[3]))
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

				if db.is_authorized(message.from_user.id):
					bot.send_message(message.from_user.id, 'Вы уже авторизованы.')

				else:
					# authorization
					reader_id = db.get_reader_id(surname, phone)

					if reader_id != 0:
						result = db.add_telegram_reader(reader_id, message.from_user.id)

					else:
						db.add_reader(surname, name, patronymic, address, phone)
						reader_id = db.get_reader_id(surname, phone)
						result = db.add_telegram_reader(reader_id, message.from_user.id)
					bot.send_message(message.from_user.id, 'Авторизация прошла успешно. '+
					  f'Ваш пароль {reader_id*1000 + int(phone/10000)}.')

			#elif state == 'pay':

			#	reader_set = db.get_telegram_reader(message.from_user.id)

			#	if reader_set is None:
			#		bot.send_message(message.from_user.id, 'Сначала авторизуйтесь.')
			#		return

			#	reader_id = reader_set[0]
			#	text = message.text.split(' ')

			#	try:
			#		title = text[0]
			#		surname = text[1]
			#		name = text[2]

			#	except IndexError:
			#		bot.send_message(message.from_user.id, 'Неправильный ввод.')
			#		bot.send_message(message.from_user.id, f'Введите данные название, фамилию и имя автора через пробел.')
			#		return

			#	self._user_state.pop(f'{message.from_user.id}')
			#	author_set = db.search_author(surname, name)
			#	author_id = 0

			#	if author_set is None or author_set[0] == 0:
			#		bot.send_message(message.from_user.id, 'Нет такого автора') 
			#		return

			#	else:
			#		author_id = author_set[0]

			#	book_set = db.search_book(title, author_id)

			#	if book_set is None:
			#		bot.send_message(message.from_user.id, 'В библиотеке нет книг с таким названием.')
			#		return

			#	if db.pay_audio_book(reader_id, book_set[0]):
			#		pass

			elif state == 'change':

				reader_set = db.get_telegram_reader(message.from_user.id)

				reader_id = reader_set[0]
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

				if db.change_reader(reader_id, surname, name, patronymic, address, phone):
					bot.send_message(message.from_user.id, 'Информация изменена успешно')
				else:
					bot.send_message(message.from_user.id, 'Ошибка. Информация не изменена')

			else:
				bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')

		bot.polling(none_stop=True)