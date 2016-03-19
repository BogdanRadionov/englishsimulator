#-*- coding:utf-8 -*-

import os
import re
import json

pathdata = 'data\\'
pattern = r'^([a-zA-Z0-9-_]*)\.json$'

class LoadList(list):
	def __init__(self, *args, **kwargs):
		super(LoadList, self).__init__(*args, **kwargs)
		self.basename = None

class Loader(object):
	def __init__(self, path=pathdata, pattern=pattern):
		self.pathdata = pathdata
		self.pattern = re.compile(pattern)

	def get_all_bases(self):
		files = os.listdir(self.pathdata)
		return [self.pattern.match(f).groups()[0] for f in files if self.pattern.match(f) and os.path.isfile(os.path.join(self.pathdata, f))]

	def load(self, args):
		data = []
		for i in args:
			for j in json.load(open(os.path.join(self.pathdata, i + '.json'))):
				j = LoadList(j)
				j.basename = i.lower()
				data.append(j)
		return data

	def create_base(self, name):
		if os.path.exists(os.path.join(self.pathdata, name + '.json')):
			return False
		json.dump([], open(os.path.join(self.pathdata, name + '.json'),'w'),ensure_ascii=False)
		return True

	def save(self, bases, words):
		for base in bases:
			data = json.dumps(words, ensure_ascii=False, encoding='utf-8')
			open(os.path.join(self.pathdata, base + '.json'),'w').write(data.encode('utf-8'))