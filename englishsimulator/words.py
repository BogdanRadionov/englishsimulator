#-*- coding:utf-8 -*-

""" Описывает классы для слова и набора слов. Фактически объект words - лист-враппер для списка слов """

import random

class Word(object):

	""" Реализует класс для отдельного слова, принимает две строки с английским и русским вариантом.
	Если необходимо записать несколько возможных вариантов слов, передаем их строкой, разделенной '|', Фактически, любой вариант строки переданный в объект, будет храниться в виде списка 1 или более слов """

	def __init__(self, en, ru):
		self.en = en.split('|')
		self.ru = ru.split('|')
		self.multien = True if len(self.en) > 1 else False
		self.multiru = True if len(self.ru) > 1 else False
	def iscorrect(self, w):
		if w in self.en:
			return self.en
		elif w in self.ru:
			return self.ru
	def spelling(self):
		return [' '.join(i).replace('   ', ' space ') for i in self.en]

class Words(object):

	""" Принимает в себя список сложенных списков попарных элементов строк, которые обрабатываются и превращаются в отдельные объекты слов, СМ выше.
	Выполняет роль списка слов с соответствующими методами взаимодействия """

	def __init__(self, words):
		self._list_words = []
		self.add_words(words)

	def add_word(self, word):
		self._list_words.append(Word(w[0], w[1]))

	def add_words(self, words):
		for w in words:
			self._list_words.append(Word(w[0], w[1]))

	def get_random_word(self, delete=True):
		rand = random.randint(0, len(self._list_words)-1)
		return self._list_words.pop(rand) if delete else self._list_words[rand]

	def get_word(self, first=True, delete=True):
		if first:
			return self._list_words.pop(0) if delete else self._list_words[0]
		return self._list_words.pop(-1) if delete else self._list_words[-1]

	def __len__(self):
		return len(self._list_words)

def __nonzero(self):
		return bool(self._list_words)