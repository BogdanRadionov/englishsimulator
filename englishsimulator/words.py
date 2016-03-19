#-*- coding:utf-8 -*-

""" Описывает классы для слова и набора слов. Фактически объект words - лист-враппер для списка слов """

import os
import re
import random
from bass import Bass
from msgexcept import *

pattern_iv = re.compile(ur'#1: *(\w.*\w) *#2: *(\w.*\w) *#3: *(\w.*\w)', re.UNICODE)
path_audio = r'data\audio'

class Word(object):

	""" Реализует класс для отдельного слова, принимает две строки с английским и русским вариантом.
	Если необходимо записать несколько возможных вариантов слов, передаем их строкой, разделенной '|', Фактически, любой вариант строки переданный в объект, будет храниться в виде списка 1 или более слов """

	def __init__(self, en, ru):
		self.en = self.parse_iv(en)
		self.ru = ru.split('|')
		self.multien = True if len(self.en) > 1 else False
		self.multiru = True if len(self.ru) > 1 else False
		_base = None
		self._audio = None

	def play(self):
		if self._audio:
			self._audio.play()
		else:
			self._audio = Bass(os.path.join(path_audio, self._base, self.find_audio_file()))
			self._audio.play()

	def find_audio_file(self):
		name = ''
		for i in os.listdir(os.path.join(path_audio, self._base)):
			if self.en[0].startswith(' '.join(i.replace('.mp3', '').split('_')).lower()) and len(i) > len(name):
				name = i.lower()
		return name

	def iscorrect(self, w):
		if w in self.en:
			return self.en
		elif w in self.ru:
			return self.ru

	def parse_iv(self, en):
		if pattern_iv.search(en):
			en = pattern_iv.search(en).groups()
			en = [i.split('|') for i in en]
			self.irregularverb = True
			return en
		else:
			self.irregularverb = False
			return en.split('|')

				

	def spelling(self):
		return [' '.join(i).replace('   ', ' space ') for i in self.en]

	def __getitem__(self, k):
		return {'en': self.en, 'ru': self.ru}[k]


class Words(object):

	""" Принимает в себя список сложенных списков попарных элементов строк, которые обрабатываются и превращаются в отдельные объекты слов, СМ выше.
	Выполняет роль списка слов с соответствующими методами взаимодействия """

	def __init__(self, words):
		self._list_words = []
		self.add_words(words)

	def add_word(self, word):
		w = Word(w[0], w[1])
		w._base = word.basename
		self._list_words.append(w)

	def add_words(self, words):
		for w in words:
			word = Word(w[0], w[1])
			word._base = w.basename
			self._list_words.append(word)

	def get_random_word(self, delete=True):
		try:
			rand = random.randint(0, len(self._list_words)-1)
			return self._list_words.pop(rand) if delete else self._list_words[rand]
		except (IndexError, ValueError):
			raise WordsEnded()

	def get_word(self, first=True, delete=True):
		try:
			if first:
				return self._list_words.pop(0) if delete else self._list_words[0]
			return self._list_words.pop(-1) if delete else self._list_words[-1]
		except IndexError:
			raise WordsEnded()


	def __len__(self):
		return len(self._list_words)

def __nonzero(self):
		return bool(self._list_words)