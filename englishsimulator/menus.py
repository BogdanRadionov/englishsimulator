#-*- coding:utf-8 -*-

import sys
from dataloader import Loader
from words import Words
from msghelper import *
from rules import RulesQuestion

encoding = sys.stdin.encoding
loader = Loader()

def choicebase(multi=False):
	bases = loader.get_all_bases()
	selectedbases = []
	msg_multiline(bases, numbers=True)
	nums = map(int, raw_input().split())
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
		command = int(raw_input())
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
		print u'1 - start question'
		print u'2 - add word to base'
		print u'3 - create base'
		print u'0 - exit'
		command = int(raw_input())
		if command == 1:
			RulesQuestion(getwords()).start_question_translate()
		elif command == 2:
			addtobase()
		elif command == 3:
			newbase()
		elif command == 0:
			return