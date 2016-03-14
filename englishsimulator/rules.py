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
			startline = 'English:'
			if w.irregularverb:
				en = []
				for i in w['en']:
					for j in i:
						en.append(j)
				en = [' '.join(en)]
				startline = 'Irregular verb:'
			msg_multiline(en, startline=startline)
			msg_multiline(w.ru, startline='Russian:')
			print u'Enter english variant:'
			self.survey(en)
			print u'Enter russian variant:'
			self.survey(w.ru)

class IrregularVerbs(object):
	def __init__(self, w):
		self.words = w
		self.msg_forms = ['Enter first form:', 'Enter second form:', 'Enter third form:']

	def survey(self, forms, repeat):
		forms = list(forms)
		f = 0
		while any(forms) and f <= 2:
			print self.msg_forms[f]
			s = 0
			while forms[f] and s <= 2:
				answer = raw_input().decode(encoding)
				try:
					forms[f].remove(answer)
					print u'is correct'
					if forms[f]:
						print u'Enter next variant:'
				except ValueError:
					print u'Incorrect, please try again!'
					s+=1
			else:
				f+=1

	def start(self):
		print u'Question language: "en", "ru" (default "en")'
		question_lang = raw_input()
		print u'Repeat question (default 3)'
		repeat = raw_input()
		question_lang = question_lang if question_lang else 'en'
		repeat = int(repeat) if repeat else 3
		while self.words:
			w = self.words.get_word()
			msg_inline(w[question_lang][0]) if question_lang == 'en' else msg_inline(w[question_lang])
			self.survey(w['en'], repeat)
		else:
			print u'Happy end!'
			print u'Press enter to return'
			raw_input()
			return