#-*- coding:cp1251 -*-

import os.path
import win32com
import win32com.client
import json

tts = win32com.client.Dispatch('SAPI.SPVoice')
SPEECH_CONFIG_FILE_NAME="tts.cfg"
speech_config={'rate': 50, 'volume': 100}

def speech_load_config():
	global speech_config
	if not os.path.isfile(SPEECH_CONFIG_FILE_NAME): return
	speech_config=json.load(open(SPEECH_CONFIG_FILE_NAME))
	for v in tts.GetVoices():
		if v.Id==speech_config["voice"]:
			while True:
				if hasattr(tts, 'SetVoice'):
					tts.SetVoice(v)
					break
			break
	tts.Rate=(int(speech_config["rate"])-50)/5
	tts.Volume = speech_config.get('volume', 100)

speech_load_config()

def speech_save_config():
	json.dump(speech_config, open(SPEECH_CONFIG_FILE_NAME,"w"), indent=4)

def speak(message, silence=False, queue=False):
	"""Произносит фразу текущим выбраным голосом.
	queue - Добавлять сообщение в очередь на произнесение, не прерывая текущей фразы
	"""
	if not silence:
		flags=1
		if not queue:
			flags=2
		tts.Speak(message, flags)

def show_list_of_voices():
	"""Выводит список голосов."""
	strings=[u"Список доступных голосов:"]
	for i,v in enumerate(tts.GetVoices()):
		strings.append("%d) %s"%(i+1, v.GetDescription()))
	print "\n".join(strings)

def set_voice(num):
	"""Устанавливает голос по номеру в списке."""
	try:
		v=tts.GetVoices()[num-1]
		while True:
			if hasattr(tts, 'SetVoice'):
				tts.SetVoice(v)
				break
		speech_config["voice"]=v.Id
		speech_save_config()
		print u"Chose voice %s"%v.GetDescription()
	except IndexError:
		print u"That voice is not found!"

def set_rate(rate):
	"""Устанавливает темп речи.
	rate - параметр от 0 до 100
	"""
	tts.Rate=(rate-50)/5
	speech_config["rate"]=rate
	speech_save_config()

def set_volume(volume):
	tts.Volume = volume
	speech_config["volume"] = volume
	speech_save_config()
