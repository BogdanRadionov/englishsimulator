#-*- coding:utf-8 -*-

""" Предоставляет ряд функций для вывода сообщений """

def msg_inline(l, begining='', end='', delim=', ', silence=False):
	if silence:
		return
	l = map(str, l)
	print u'{0}{1}{2}'.format(begining, delim.join(l), end)

def msg_multiline(l, startline='', endline='', numbers=False, startnum=1, delim='-', silence=False):
	if silence:
		return
	l = map(str, l)
	if startline:
		print startline
	if numbers:
		for num,  line in enumerate(l, startnum):
			print u'{0} {1} {2}'.format(num, delim, line)
	else:
		for line in l:
			print line
	if endline:
		print endline