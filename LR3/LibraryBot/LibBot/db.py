import pyodbc
from LibraryBot import settings

class db(object):
	@staticmethod
	def _db_connection():
		driver = settings.DATABASES['default']['DRIVER']
		server = settings.DATABASES['default']['SERVER']
		database = settings.DATABASES['default']['NAME']
		conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
		return conn


	@staticmethod
	def search_book_title(title):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			cursor.execute('{call [dbo].[searchBookTitle](?)}', [title])
			result_set = cursor.fetchall()

			if result_set:
				return result_set

			else:
				return None

		except Exception:
			return None

		finally:
			cursor.close()


	@staticmethod
	def get_author(author_id):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			cursor.execute('{call [dbo].[getAuthor](?)}', [author_id])
			result_set = cursor.fetchone()

			if result_set:
				return result_set

			else:
				return None

		except Exception:
			return None

		finally:
			cursor.close()


	@staticmethod
	def search_author_books(author_id):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			cursor.execute('{call [dbo].[searchAuthorBooks](?)}', [author_id])
			result_set = cursor.fetchall()

			if result_set:
				return result_set

			else:
				return None

		except Exception:
			return None

		finally:
			cursor.close()


	@staticmethod
	def search_author(surname, name):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			cursor.execute('{call [dbo].[searchAuthor](?, ?)}', [surname, name])
			result_set = cursor.fetchone()

			if result_set:
				return result_set

			else:
				return None

		except Exception:
			return None

		finally:
			cursor.close()


	@staticmethod
	def search_book(title, author_id):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			cursor.execute('{call [dbo].[searchBook](?, ?)}', [title, author_id])
			result_set = cursor.fetchone()

			if result_set:
				return result_set

			else:
				return None

		except Exception:
			return None

		finally:
			cursor.close()


	@staticmethod
	def get_genre(genre_id):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			cursor.execute('{call [dbo].[getGenre](?)}', [genre_id])
			result_set = cursor.fetchone()

			if result_set:
				return result_set

			else:
				return None

		except Exception:
			return None

		finally:
			cursor.close()


	@staticmethod
	def is_authorized(user_id):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			cursor.execute('{call [dbo].[searchTelegramReader](?)}', [user_id])
			result = cursor.fetchone()

			if result is None:
				return False

			else:
				return True

		except Exception:
			return False

		finally:
			cursor.close()


	@staticmethod
	def get_reader_id(surname, phone):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			cursor.execute('{call [dbo].[searchReader](?, ?)}', [surname, phone])
			result = cursor.fetchone()
			return int(result[0])

		except Exception:
			return 0

		finally:
			cursor.close()


	@staticmethod
	def add_telegram_reader(reader_id, telegram_id):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			sql = '{call [dbo].[addTelegramReader](?, ?)}'
			values = (reader_id, telegram_id)
			cursor.execute(sql, (values))
			conn.commit()
			return True

		except Exception:
			return False

		finally:
			cursor.close()


	@staticmethod
	def add_reader(surname, name, patronymic, address, phone_number):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			sql = '{call [dbo].[addReader](?, ?, ?, ?, ?)}'
			values = (surname, name, patronymic, address, phone_number)
			cursor.execute(sql, (values))
			conn.commit()
			return True

		except Exception:
			return False

		finally:
			cursor.close()


	@staticmethod
	def get_list_of_reader_books(offset, count, reader_id):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			cursor.execute('{call [dbo].[getListOfReaderBooks](?, ?, ?)}', [offset, count, reader_id])
			result_set = cursor.fetchall()

			if result_set:
				return result_set

			else:
				return None

		except Exception:
			return None

		finally:
			cursor.close()


	@staticmethod
	def search_telegram_reader(user_id):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			cursor.execute('{call [dbo].[searchTelegramReader](?)}', [user_id])
			result = cursor.fetchone()

			return result

		except Exception:
			return None

		finally:
			cursor.close()


	@staticmethod
	def change_reader(reader_id, surname, name, patronymic, address, phone):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			sql = '{call [dbo].[changeReaderInfo](?, ?, ?, ?, ?, ?)}'
			values = (reader_id, surname, name, patronymic, address, phone)
			cursor.execute(sql, (values))
			conn.commit()
			return True

		except Exception:
			return False

		finally:
			cursor.close()


	@staticmethod
	def delete_telegram_reader(reader_id):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			sql = '{call [dbo].[deleteTelegramReader](?)}'
			values = (reader_id)
			cursor.execute(sql, (values))
			conn.commit()
			return True

		except Exception:
			return False

		finally:
			cursor.close()


	@staticmethod
	def add_librarian(surname, name, patronymic, address, phone, pswd):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			sql = '{call [dbo].[addLibrarian](?, ?, ?, ?, ?, ?)}'
			values = (surname, name, patronymic, address, phone, pswd)
			cursor.execute(sql, (values))
			conn.commit()
			return True

		except Exception:
			return False

		finally:
			cursor.close()


	@staticmethod
	def del_librarian(surname, pswd):

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			sql = '{call [dbo].[deleteLibrarian](?, ?)}'
			values = (surname, pswd)
			cursor.execute(sql, (values))
			conn.commit()
			return True

		except Exception:
			return False

		finally:
			cursor.close()


	@staticmethod
	def get_telegram_readers_id():

		conn = db._db_connection()
		cursor = conn.cursor()

		try:
			cursor.execute('{call [dbo].[getTelegramReaderId]}')
			result = cursor.fetchall()
			return result

		except Exception:
			return None

		finally:
			cursor.close()
