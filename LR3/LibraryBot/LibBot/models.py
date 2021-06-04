from django.db import models

class Profile(models.Model):
	external_id = models.PositiveIntegerField(
		verbose_name='ID пользователя',
	)
	name = models.TextField(
		verbose_name='Имя пользователя'
	)

	class Meta:
		verbose_name = 'Профиль'
		verbose_name_plural = 'Профили'


class Message(models.Model):
	profile = models.ForeignKey(
		to='LibBot.Profile',
		verbose_name='Профиль',
		on_delete=models.PROTECT,
	)
	text = models.TextField(
		verbose_name='Текст',
	)
	created_at = models.DateTimeField(
		verbose_name='Время получения',
		auto_now_add=True,
	)

	class Meta:
		verbose_name='Сообщение'
		verbose_name_plural='Сообщения'


class Book(models.Model):
	book_id = models.IntegerField(
		verbose_name='ID книги',
	)
	title = models.TextField(
		verbose_name='Название',
	)
	author = models.ForeignKey(
		to='LibBot.Author',
		verbose_name='Автор',
		on_delete=models.PROTECT,
	)
	genre = models.ForeignKey(
		to='LibBot.Genre',
		verbose_name='Жанр',
		on_delete=models.PROTECT,
	)
	collateral_value = models.FloatField(
		verbose_name='Залоговая стоимость',
	)
	rental_coast = models.FloatField(
		verbose_name='Арендная стоимость',
	)
	amount = models.IntegerField(
		verbose_name='Количество',
	)

	def __str__(self):
		return (f'Название: {self.title}\n{str(self.author)}\n{str(self.genre)}\n'+
		  f'Залоговая стоимость: {self.collateral_value}\n'+
		  f'Арендная стоимость: {self.rental_coast}\nКоличество книг в библиотеке: {self.amount}')

	def from_list(self, list_book, author, genre):
		self.book_id = list_book[0]
		self.title = list_book[1]
		self.author = author
		self.genre = genre
		self.collateral_value = list_book[4]
		self.rental_coast = list_book[5]
		self.amount = list_book[6]

	class Meta:
		verbose_name = 'Книга'
		verbose_name_plural = 'Книги'



class Author(models.Model):
	author_id = models.IntegerField(
		verbose_name='ID автора',
	)
	surname = models.TextField(
		verbose_name='Фамилия',
	)
	name = models.TextField(
		verbose_name='Имя',
	)

	def __str__(self):
		return (f'Автор: {self.surname} {self.name}')

	def from_list(self, list):
		self.author_id = list[0]
		self.surname = list[1]
		self.name = list[2]

	class Meta:
		verbose_name = 'Автор'
		verbose_name_plural = 'Авторы'


class Genre(models.Model):
	genre_id = models.IntegerField(
		verbose_name='ID жанра',
	)
	genre = models.TextField(
		verbose_name='Название жанра')

	def __str__(self):
		return (f'Жанр: {self.genre}')

	def from_list(self, list):
		self.genre_id = list[0]
		self.genre = list[1]

	class Meta:
		verbose_name = 'Жанр'
		verbose_name_plural = 'Жанры'