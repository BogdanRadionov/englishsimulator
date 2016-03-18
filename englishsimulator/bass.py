#-*- coding:utf-8 -*-

import os
import ctypes
bass = ctypes.windll.LoadLibrary(os.path.abspath(os.curdir)+'\\bass.dll')

bass.BASS_Init(-1, 44100, 0,0,0)

class Bass(object):
	def __init__(self, filename):
		self.filename = filename
		self.stream = bass.BASS_StreamCreateFile(False, filename,0,0,0,0,0)

	def play(self):
		bass.BASS_ChannelPlay(self.stream, True)
