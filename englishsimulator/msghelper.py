#-*- coding:utf-8 -*-

""" Предоставляет ряд функций для вывода сообщений """

def msg_inline(l, begining=u'', end=u'', delim=u', ', silence=False):
	if silence:
		return
	l = map(unicode, l)
	print u'{0}{1}{2}'.format(begining, delim.join(l), end)

def msg_multiline(l, startline=u'', endline=u'', numbers=False, startnum=1, delim=u'-', silence=False):
	if silence:
		return
	l = map(unicode, l)
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

def str_inline(l, begining=u'', end=u'', delim=u', ', silence=False):
	if silence:
		return ''
	l = map(unicode, l)
	return u'{0}{1}{2}'.format(begining, delim.join(l), end)

def str_multiline(l, startline=u'', endline=u'', numbers=False, startnum=1, delim=u'-', silence=False):
	if silence:
		return ''
	lines = []
	l = map(unicode, l)
	if startline:
		lines.append(startline)
	if numbers:
		for num,  line in enumerate(l, startnum):
			lines.append(u'{0} {1} {2}'.format(num, delim, line))
	else:
		for line in l:
			lines.append(line)
	if endline:
		lines.append(endline)
	return '\n'.join(lines)