#-*- coding:utf-8 -*-

import random

class Word(object):
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
	def __init__(self, words):
		self.list_words = []
		self.add_words(words)

	def add_word(self, word):
		self.list_words.append(Word(w[0], w[1]))

	def add_words(self, words):
		for w in words:
			self.list_words.append(Word(w[0], w[1]))

	def get_random_word(self, delete=True):
		rand = random.randint(0, len(self.list_words)-1)
		return self.list_words.pop(rand) if delete else self.list_words[rand]

	def get_word(self, first=True, delete=True):
		if first:
			return self.list_words.pop(0) if delete else self.list_words[0]
		return self.list_words.pop(-1) if delete else self.list_words[-1]

	def __len__(self):
		return len(self.list_words)