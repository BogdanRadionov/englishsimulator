#-*- coding:utf-8 -*-

import sys
from dataloader import Loader
from words import Words
import tts
from msghelper import *
from rules import *

encoding = sys.stdin.encoding
loader = Loader()

def setings_tts():
	while True:
		print u"Setings of text to speech:"
		print u'1 - Choose synthesiser'
		print u'2 - Set sinthesiser volume'
		print u'3 - Set synthesiser rate'
		print u'0 - Exit'
		try:
			command = int(raw_input())
		except ValueError:
			print u'Please, select item of menu'
			continue
		if command == 0:
			return
		elif command == 1:
			print u"Choose synthesiser of list:"
			tts.show_list_of_voices()
			try:
				tts.set_voice(int(raw_input()))
				continue
			except ValueError:
				print u'Command is wrong!'
				continue
		elif command == 2:
			print u'Set volume for voice 0 - 100: (Default 100)'
			volume = raw_input()
			try:
				volume = int(volume) if volume else 100
				tts.set_volume(volume)
				continue
			except ValueError:
				print u'Command is wrong!'
				continue
		elif command == 3:
			print u'Set temp for voice 0 - 100: (Default 50)'
			temp = raw_input()
			try:
				temp = int(temp) if temp else 50
				tts.set_rate(temp)
				continue
			except ValueError:
				print u'Command is wrong!'
				continue

def choicebase(multi=False):
	bases = loader.get_all_bases()
	while True:
		selectedbases = []
		msg_multiline(bases, numbers=True)
		try:
			nums = map(int, raw_input().split())
		except ValueError:
			print u'Enter one number or some numbers bases of list!'
			continue
		if not multi:
			return [bases[nums[0]-1]]
		else:
			for i in nums:
				selectedbases.append(bases[i-1])
		return selectedbases

def newword():
	print u"Enter word in English:"
	en = raw_input().decode(encoding)
	print u'Enter word in Russian:'
	ru = raw_input().decode(encoding)
	return [en.lower(), ru.lower()]

def addtobase():
	print u'Choise base of list:'
	select = choicebase()
	data = loader.load(select)
	while True:
		print u'1 - add word'
		print u'2 - exit'
		try:
			command = int(raw_input())
		except ValueError:
			print u'Please, select item of menu!'
			continue
		if command == 1:
			word = newword()
			data.append(word)
			loader.save(select, data)
		elif command == 2:
			break

def newbase():
	print u'Enter name for creation  base:'
	if loader.create_base(raw_input()):
		print u'All Right!'
	else:
		print u'Error! Base is not create!'

def getwords():
	print u'Enter several numbers:'
	bases = choicebase(multi=True)
	data = loader.load(bases)
	return Words(data)

def startmenu():
	while True:
		print u'Your choice:'
		print u'1 - The study'
		print u'2 - Questions Irregular verbs'
		print u'3 - start question'
		print u'4 - add word to base'
		print u'5 - create base'
		print u'6 - Setings tts'
		print u'0 - exit'
		try:
			command = int(raw_input())
		except ValueError:
			print u'Please, select item of menu'
			continue
		if command == 2:
			IrregularVerbs(getwords()).start()
		elif command == 1:
			Study(getwords()).start()
		elif command == 3:
			RulesQuestion(getwords()).start_question_translate()
		elif command == 4:
			addtobase()
		elif command == 5:
			newbase()
		elif command == 6:
			setings_tts()
		elif command == 0:
			return