from django.core.management.base import BaseCommand
from LibraryBot import settings
import telebot
from ...models import Book, Author, Genre
from ...db import db


class Command(BaseCommand):
	_user_state = dict()
	admin = 0

	def is_pswd_correct(self, pswd):
		return pswd == settings.ADMIN_PSWD

	def handle(self, *args, **options):
		bot = telebot.TeleBot(settings.TOKEN)


		@bot.message_handler(commands=['start'])
		def send_welcome(message):

			bot.send_message(message.from_user.id, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')


		@bot.message_handler(commands=['help'])
		def send_help(message):

			bot.send_message(message.from_user.id, f'Я студенческий проект-телеграм бот для библиотеки)')


		# get rights of admin
		@bot.message_handler(commands=['admin'])
		def get_admin_rights(message):

			self._user_state.update({f'{message.from_user.id}':f'admin'})
			bot.send_message(message.from_user.id, f'Введите пароль')


		# add librarian (for admin)
		@bot.message_handler(commands=['add_librarian'])
		def add_librarian(message):

			if not self.admin == message.from_user.id:
				bot.send_message(message.from_user.id, f'Не понимаю, что это значит.')
			bot.send_message(message.from_user.id, f'Введите данные по шаблону:\nФамилия Имя Отчество '+
				   f'Адрес Номер_телефона Пароль_библиотекаря.')
			self._user_state.update({f'{message.from_user.id}':f'add_librarian'})


		# delete librarian (for admin)
		@bot.message_handler(commands=['del_librarian'])
		def del_librarian(message):

			if not self.admin == message.from_user.id:
				bot.send_message(message.from_user.id, f'Не понимаю, что это значит.')
			bot.send_message(message.from_user.id, f'Введите фамилию и пароль библиотекаря через пробел')
			self._user_state.update({f'{message.from_user.id}':f'del_librarian'})

		
		# authorization for readers
		@bot.message_handler(commands=['authorize'])
		def authtorize(message):

			self._user_state.update({f'{message.from_user.id}':f'authorize'})
			bot.send_message(message.from_user.id, f'Введите данные по шаблону:\nФамилия '+
					'Имя Отчество Адрес Номер_телефона.')


		# reader changes information about himself
		@bot.message_handler(commands=['change'])
		def change_reader_info(message):

			reader_set = db.get_telegram_reader(message.from_user.id)

			if reader_set is None:
				bot.send_message(message.from_user.id, 'Сначала авторизуйтесь.')
				return

			self._user_state.update({f'{message.from_user.id}':f'change'})
			bot.send_message(message.from_user.id, f'Введите данные по шаблону:\nФамилия '+
					'Имя Отчество Адрес Номер_телефона.')


		# reader removes himself from the list of readers using the bot
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


		# display a list of books with the entered title
		@bot.message_handler(commands=['book'])
		def search_books(message):

			self._user_state.update({f'{message.from_user.id}':f'book'})
			bot.send_message(message.from_user.id, 'Введите название книги, фамилию и имя автора через пробел')


		# display list of books with enterd author
		@bot.message_handler(commands=['author'])
		def search_author_books(message):

			self._user_state.update({f'{message.from_user.id}':f'author'})
			bot.send_message(message.from_user.id, 'Введите фамилию и имя автора через пробел')


		# display list of not returned books
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


		# bot-user enter some text
		@bot.message_handler(content_types=['text'])
		def get_text_messages(message):

			state = self._user_state.get(f'{message.from_user.id}')

			# say hello
			if message.text.lower().find('привет') != -1 and message.text.find('?') == -1:
				bot.send_message(message.from_user.id, 'Привет!')

			# get rights of admin
			elif state == 'admin':

				text = message.text

				try:
					pswd = int(text)
				except ValueError:
					bot.send_message(message.from_user.id, 'Пароль должен быть числом')
					return

				if not self.is_pswd_correct(pswd):
					bot.send_message(message.from_user.id, 'Неверный пароль')
					return

				self.admin = message.from_user.id
				bot.send_message(message.from_user.id, 'Вы успешно авторизованы как админ')

			# add librarian (for admin)
			elif state == 'add_librarian':

				text = message.text.split(' ')

				try:
					surname = text[0]
					name = text[1]
					patronymic = text[2]
					address = text[3]
					phone = int(text[4])
					pswd = int(text[5])
					pswd ^= 9512; # encrypt pswd 

				except IndexError:
					bot.send_message(message.from_user.id, 'Неправильный ввод.')
					bot.send_message(message.from_user.id, f'Введите данные по шаблону:\nФамилия '+
					  'Имя Отчество Адрес Номер_телефона.')
					return

				except ValueError:
					bot.send_message(message.from_user.id, 'Неправильный ввод. Номер телефона '+
					  'и пароль должены быть числами')
					return

				self._user_state.pop(f'{message.from_user.id}')

				if db.add_librarian(surname, name, patronymic, address, phone, pswd):
					bot.send_message(message.from_user.id, 'Библиотекарь добавлен.')
				else:
					bot.send_message(message.from_user.id, 'Ошибка. Библиотекарь не добавлен.')

			# delete librarian (for admin)
			elif state == 'del_librarian':

				text = message.text.split(' ')

				try:
					surname = text[0]
					pswd = int(text[1])
					pswd ^= 9512; # decrypt pswd

				except IndexError:
					bot.send_message(message.from_user.id, 'Неправильный ввод.')
					bot.send_message(message.from_user.id, f'Введите фамилию и пароль библиотекаря через пробел.')
					return

				except ValueError:
					bot.send_message(message.from_user.id, 'Неправильный ввод. Пароль должен быть числом.')
					return

				self._user_state.pop(f'{message.from_user.id}')

				if db.del_librarian(surname, pswd):
					bot.send_message(message.from_user.id, 'Библиотекарь удален.')
				else:
					bot.send_message(message.from_user.id, 'Ошибка. Библиотекарь не был удален.')

			# authorization for readers
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
					bot.send_message(message.from_user.id, f'Введите данные по шаблону:\nФамилия '+
					 'Имя Отчество Адрес Номер_телефона.')
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

			# reader changes information about himself
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
					bot.send_message(message.from_user.id, f'Введите данные по шаблону:\nФамилия Имя '+
					  'Отчество Адрес Номер_телефона.')
					return

				except ValueError:
					bot.send_message(message.from_user.id, 'Неправильный ввод. Номер телефона должен быть числом')
					return

				self._user_state.pop(f'{message.from_user.id}')

				if db.change_reader(reader_id, surname, name, patronymic, address, phone):
					bot.send_message(message.from_user.id, 'Информация изменена успешно. '+
					  f'Ваш пароль {reader_id*1000 + int(phone/10000)}.')
				else:
					bot.send_message(message.from_user.id, 'Ошибка. Информация не изменена')

			# display a list of books with the entered title
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

			# display list of books with enterd author
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

			# bot don't know what user want
			else:
				bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')

		bot.polling(none_stop=True)