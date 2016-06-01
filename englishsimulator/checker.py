#-*- coding:utf-8 -*-

import os
import json

for f in os.listdir(os.path.join(os.getcwd(), 'data')):
	data = []
	if os.path.isfile(os.path.join(os.getcwd(),'data',f)):
		for en, ru in json.load(open(os.path.join(os.getcwd(),'data',f))):
			data.append([en.lower().encode('utf-8'), ru.lower().encode('utf-8')])
		json.dump(data, open(os.path.join(os.getcwd(),'data',f), 'w'), encoding='utf-8', ensure_ascii=False, indent=4)