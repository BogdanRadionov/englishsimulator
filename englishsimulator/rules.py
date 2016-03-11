#-*- coding:utf-8 -*-

import sys
import random
from msgexcept import *
from msghelper import *

encoding = sys.stdin.encoding

class RulesQuestion(object):
	def __init__(self, w, rand=True):
		self.words = w
		self.rand = rand

	def question_translate(self, to, repeat=1, silence=False):
		s = 0
		if self.rand:
			word = self.words.get_random_word()
		else:
			word = self.words.get_word()
		if not silence: print u'Words left - {0}'.format(len(self.words))
		while s < repeat	:
			if not silence: print u'Enter your answer - attempts {0}'.format(repeat-s)
			s+=1
			if to=='ru':
				for i in word.en:
					print i
				if word.multiru:
					print u'Variants for translate {0}'.format(len(word.ru))
			elif to=='en':
				for i in word.ru:
					print i
				if word.multien:
					print u'Variants for translate {0}'.format(len(word.en))
			answer = raw_input().decode(encoding)
			if word.iscorrect(answer):
				if not silence: print u'Correct, {0}'.format(answer)
				if to=='ru' and word.multiru:
					print u'All variants:'
					for i in word.ru:
						print i
				elif to=='en' and word.multien:
					print u'All variants:'
					for i in word.en:
						print i
				return True
			else:
				if not silence: print u'Incorrect, please try again!'
		else:
			if not silence: print u"Correct answer was:"
			if to=='ru':
				for i in word.ru:
					print i
			elif to=='en':
				for i in word.en:
					print i
				return False

	def start_question_translate(self):
		correctanswers = 0
		totalanswers = len(self.words)
		print u'Enter translate to: "ru", "en", "random" (default ru)'
		to = raw_input()
		print u'Repeat question (default 3)'
		repeat = raw_input()
		to = to if to else 'ru'
		repeat = int(repeat) if repeat else 3
		if to=='random':
			to = ['en', 'ru']
		else:
			to = [to]
		while True:
			try:
				if self.question_translate(random.choice(to), repeat):
					correctanswers+=1
				else:
					pass
			except WordsEnded:
				print u'End question!'
				print u'Total answers - {0}'.format(totalanswers)
				print u'Correct answers - {0}'.format(correctanswers)
				print u'press enter to return'
				raw_input()
				return

class Study(object):
	def __init__(self, w):
		self.words = w

	def survey(self, variant):
		while not raw_input().decode(encoding) in variant:
			print u'Wrong!'
			msg_multiline(variant, startline='Variants:')

	def start(self):
		while True:
			try:
				w = self.words.get_word()
			except WordsEnded:
				print u'Happy end!\npress enter to return'
				raw_input()
				return
			msg_multiline(w.en, startline='English:')
			msg_multiline(w.ru, startline='Russian:')
			print u'Enter english variant:'
			self.survey(w.en)
			print u'Enter russian variant:'
			self.survey(w.ru)
"""
class IrregularVerbs(object):
	def __init__(self, w):
		self.words = w

	def survey(self, w, repeat):

	def start(self):
		print u'Question language: "en", "ru" (default "en")'
		question_lang = raw_input()
		print u'Repeat question (default 3)'
		repeat = raw_input()
		question_lang = question_lang if question_lang else 'en'
		repeat = int(repeat) if repeat else 3
		while True:
		w = self.words.get_word()
		msg_multiline(w[question_lang])
"""