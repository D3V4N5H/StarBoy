from __future__ import print_function

from config import *
from MusixMatch import *

import re
from collections import OrderedDict

import pyaudio
from bs4 import BeautifulSoup
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
from threading import Thread

#2851948

def get_Genius_Lyrics(song_ID):
	search_url = genius_Base_Url + '/songs/'+str(song_ID)+'?text_format=plain'
	response=requests.get(search_url, headers=headers)
	if response.json()['meta']['status']==200:
		url = response.json()['response']['song']['url']
		if url:
			page = requests.get(url)
			html = BeautifulSoup(page.text, "html.parser")
			return html.find("div", class_="lyrics").get_text()

lyrics=get_Genius_Lyrics(2851948)
lyrics=re.split(', | |\n',lyrics)
lyrics = list(filter(None, lyrics))
lyrics=list(OrderedDict.fromkeys(lyrics))
print(lyrics)

try:
	from Queue import Queue, Full
except ImportError:
	from queue import Queue, Full

CHUNK = 1024
BUF_MAX_SIZE = CHUNK * 10
q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))
audio_source = AudioSource(q, True, True)

speech_to_text = SpeechToTextV1(iam_apikey=Watson_Ears,url=Watson_Gateway_URL)

class MyRecognizeCallback(RecognizeCallback):
	def __init__(self):
		RecognizeCallback.__init__(self)
	def on_transcription(self, transcript):
		print(transcript[0]['transcript'])
		earLobe.append(transcript[0]['transcript'])
		for word in transcript[0]['transcript'].split(' '):
			if word in lyrics:
				print('✅ '+word + ' detected from lyrics')
	def on_connected(self):
		print('Connection was successful')
	def on_error(self, error):
		print('Error received: {}'.format(error))
	def on_inactivity_timeout(self, error):
		print('Inactivity timeout: {}'.format(error))
	def on_listening(self):
		print('👂🏻 Watson is listening')
	# def on_hypothesis(self, hypothesis):
		# print(hypothesis)
	# def on_data(self, data):
		# print(data)
	def on_close(self):
		print("Connection closed")

def recognize_using_weboscket(*args):
	mycallback = MyRecognizeCallback()
	speech_to_text.recognize_using_websocket(
					audio=audio_source,
					content_type='audio/l16; rate=44100',
					recognize_callback=mycallback,
					interim_results=True)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def pyaudio_callback(in_data, frame_count, time_info, status):
	try:
		q.put(in_data)
	except Full:
		pass
	return (None, pyaudio.paContinue)

audio = pyaudio.PyAudio()

stream = audio.open(
	format=FORMAT,
	channels=CHANNELS,
	rate=RATE,
	input=True,
	frames_per_buffer=CHUNK,
	stream_callback=pyaudio_callback,
	start=False
)

print("Enter CTRL+C to end recording...")
stream.start_stream()
earLobe=[]
try:
	recognize_thread = Thread(target=recognize_using_weboscket, args=())
	recognize_thread.start()
	while True:
		pass
except KeyboardInterrupt:
	audio_source.completed_recording()
	stream.stop_stream()
	stream.close()
	audio.terminate()

print(earLobe)
