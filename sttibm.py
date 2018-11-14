from __future__ import print_function
import pyaudio
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
from threading import Thread

try:
	from Queue import Queue, Full
except ImportError:
	from queue import Queue, Full

CHUNK = 1024
BUF_MAX_SIZE = CHUNK * 10
q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))
audio_source = AudioSource(q, True, True)

speech_to_text = SpeechToTextV1(iam_apikey=iam_apikey,url=url)

class MyRecognizeCallback(RecognizeCallback):
	def __init__(self):
		RecognizeCallback.__init__(self)
	def on_transcription(self, transcript):
		print(transcript[0]['transcript'])
		earLobe.append(transcript[0]['transcript'])
	def on_connected(self):
		print('Connection was successful')
	def on_error(self, error):
		print('Error received: {}'.format(error))
	def on_inactivity_timeout(self, error):
		print('Inactivity timeout: {}'.format(error))
	def on_listening(self):
		print('Watson is listening')
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
