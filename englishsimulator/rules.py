#-*- coding:utf-8 -*-

import sys
import random
import tts
from msgexcept import *
from msghelper import *

encoding = sys.stdin.encoding

class RulesQuestion(object):
	def __init__(self, w):
		self.words = w

	def delay_tts(self, text):
		while not self.tts_mode:
			tts.speak(text)
			answer = raw_input().decode(encoding)
			if answer:
				return answer
		return raw_input().decode(encoding)

	def question_translate(self, to, repeat, rand, silence=False):
		s = 0
		if rand == 'b':
			word = self.words.get_word()
		elif rand == 'e':
			word = self.words.get_word(first=False)
		elif rand == 'r':
			word = self.words.get_random_word()
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
			if to == 'ru':
				if not word.irregularverb:
					answer = self.delay_tts(', '.join(word.en))
				else:
					answer = self.delay_tts(', '.join([', '.join(word.en[0]), ', '.join(word.en[1]), ', '.join(word.en[2])]))
			else:
				answer = raw_input().decode(encoding)
			if word.iscorrect(answer):
				if not silence: print u'Correct, {0}'.format(answer)
				if to == 'en':
					tts.speak(answer, silence=self.tts_mode)
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
				tts.speak(', '.join(word.en), silence=self.tts_mode)
				return False

	def start_question_translate(self):
		correctanswers = 0
		totalanswers = len(self.words)
		print u'Enter translate to: "ru", "en", "random" (default ru)'
		to = raw_input()
		print u'Repeat question (default 3)'
		repeat = raw_input()
		print u'Order of words: "b" - with begin, "e" - with end: "r" - randomly. (Default "r")'
		rand = raw_input()
		print u"Range of words - 1 {0} (default - 1 {0})".format(totalanswers)
		rangewords = raw_input().split()
		if rangewords:
			self.words.trim_words(int(rangewords[0])-1, int(rangewords[1]))
		totalanswers = len(self.words)
		print u'Enable tts: enable - "e", disable - "d" (Default "d")'
		self.tts_mode = False if raw_input() == 'e' else True
		to = to if to else 'ru'
		repeat = int(repeat) if repeat else 3
		rand = rand if rand else 'r'
		if to=='random':
			to = ['en', 'ru']
		else:
			to = [to]
		while True:
			try:
				if self.question_translate(random.choice(to), repeat, rand):
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
		self.flag_speak = True

	def delay_tts(self, text):
		while not self.tts_mode and self.flag_speak:
			tts.speak(text)
			answer = raw_input().decode(encoding)
			if answer:
				return answer
		return raw_input().decode(encoding)

	def survey(self, variant):
		if self.options == 'a' or self.options == 'ta':
			answer = self.delay()
		else:
			answer = self.delay_tts(', '.join(variant))
		while not answer in variant:
			print u'Wrong!'
			if self.options == 'a':
				answer = self.delay()
				continue
			elif self.options == 'ta':
				msg_multiline(variant, startline='Variants:')
				answer = self.delay()
				continue
			elif self.options == 't':
				msg_multiline(variant, startline='Variants:')
				answer = self.delay_tts(', '.join(variant))
				continue
		if not self.tts_mode:
			self.flag_speak = False if self.flag_speak else True


	def start(self):
		totalanswers = len(self.words)
		print u'Only text: "t", only audio: "a", text plus audio: "ta". (Default "t")'
		options = raw_input()
		self.options = options if options else 't'
		print u'Enable tts: enable - "e", disable - "d" (Default "d")'
		self.tts_mode = False if raw_input() == 'e' else True
		print u"Range of words - 1 {0} (default - 1 {0})".format(totalanswers)
		rangewords = raw_input().split()
		if rangewords:
			self.words.trim_words(int(rangewords[0])-1, int(rangewords[1]))
		while True:
			try:
				self.w = self.words.get_word()
			except WordsEnded:
				print u'Happy end!\npress enter to return'
				raw_input()
				return
			startline = 'English:'
			en = self.w.en
			if self.w.irregularverb:
				en = []
				for i in self.w['en']:
					for j in i:
						en.append(j)
				en = [', '.join(en)]
				startline = 'Irregular verb:'
			if self.options == 't' or options == 'ta':
				msg_multiline(en, startline=startline)
			msg_multiline(self.w.ru, startline='Russian:')
			print u'Enter english variant:'
			self.survey(en)
			print u'Enter russian variant:'
			self.survey(self.w.ru)

	def delay(self):
		while True:
			self.w.play()
			answer = raw_input().decode(encoding)
			if answer:
				return answer

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
					tts.speak(answer, self.tts_mode)
					if forms[f]:
						print u'Enter next variant:'
				except ValueError:
					print u'Incorrect, please try again!'
					s+=1
					if s == repeat:
						print u'Answer was:'
						msg_multiline(forms[f], endline=' ')
						tts.speak(forms[f][0], self.tts_mode)
			else:
				f+=1

	def start(self):
		totalanswers = len(self.words)
		print u'Question language: "en", "ru" (default "en")'
		question_lang = raw_input()
		print u'Repeat question (default 3)'
		repeat = raw_input()
		print u'Order of words: "b" - with begin, "e" - with end: "r" - randomly. (Default "b")'
		rand = raw_input()
		print u"Range of words - 1 {0} (default - 1 {0})".format(totalanswers)
		rangewords = raw_input().split()
		if rangewords:
			self.words.trim_words(int(rangewords[0])-1, int(rangewords[1]))
		print u'Enable tts: enable - "e", disable - "d" (Default "d")'
		self.tts_mode = False if raw_input() == 'e' else True
		question_lang = question_lang if question_lang else 'en'
		repeat = int(repeat) if repeat else 3
		rand = rand if rand else 'b'
		while self.words:
			if rand == 'b':
				self.w = self.words.get_word()
			elif rand == 'e':
				self.w = self.words.get_word(first=False)
			elif rand == 'r':
				self.w = self.words.get_random_word()
			msg_inline(self.w[question_lang][0]) if question_lang == 'en' else msg_inline(self.w[question_lang])
			if question_lang == 'en':
				tts.speak(self.w['en'][0][0], self.tts_mode)
			self.survey(self.w['en'], repeat)
		else:
			print u'Happy end!'
			print u'Press enter to return'
			raw_input()
			return