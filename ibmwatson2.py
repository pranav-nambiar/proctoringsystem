'''
Speech to text transcription, from your mike, in real-time, using IBM Watson.
'''

# import argparse
import time

import fluteline

import watson_streaming
import watson_streaming.utilities

import string

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from violationtracker import appendToViolation


def read_tokenize_return(data):
	filtered = []
	stop_words = set(stopwords.words('english'))   
	word_tokens = word_tokenize(data.translate(dict.fromkeys(string.punctuation))) ######### tokenizing sentence
	for w in word_tokens:   ####### Removing stop words
	    if w not in stop_words: 
	        filtered.append(w.lower())
	return set(filtered)

def ret_qs():
	##### checking whether proctor needs to be alerted or not
	if not ret_qs.filtered_questions:
		file = open("paper.txt") ## Question file
		data = file.read()
		file.close()
		# stop_words = set(stopwords.words('english'))   
		# word_tokens = word_tokenize(data) ######### tokenizing sentence
		# for w in word_tokens:   ####### Removing stop words
		#     if w not in stop_words: 
		#         ret_qs.filtered_questions.append(w)
		ret_qs.filtered_questions = read_tokenize_return(data)
	return ret_qs.filtered_questions 

ret_qs.filtered_questions = set()

'''
{'result_index': 0, 'results': [{'final': False, 'alternatives': [{'transcript': 'hello '}]}], 'warnings': ['Unknown URL query params: access_token. Websockets requests should have the
parameters in WS messages, not in URL.', 'Unknown arguments: x-watson-learning-learning-opt-out, low_latency.']}
'''

class PrinterProducer(fluteline.Consumer):
	def consume(self,item):
		if 'results' in item:
			# print(type(item['results']))
			if item['results'][0]['final']:
				text = item['results'][0]['alternatives'][0]['transcript']
				self.output.put(text)
				# print(text)


class ViolationChecker(fluteline.Consumer):
	def enter(self):
		self.script = ret_qs()
		print("Script has been processed!")
	def consume(self,item):
		# print(self.script)
		print("Consuming sentence")
		sentence = read_tokenize_return(item)
		print(sentence)
		inter = self.script.intersection(sentence)
		if len(inter):
			print("Possible violation detected! Reporting to the proctor.")
			appendToViolation(5,1)
			print("Detected the matches: ", inter)
			with open("violations.txt","a") as file1:
				file1.write(str(inter))

		


def startSTT():
	settings = {
		'inactivity_timeout': -1,  # Don't kill me after 30 seconds
		'interim_results': True,
	}

# watson_streaming.Transcriber(settings, apikey='88PYNfB8kng7I4uKF2D8OLub0V05-SYmDIA1_gySDEbb', hostname='gateway-wdc.watsonplatform.net'),
	nodes = [
		watson_streaming.utilities.MicAudioGen(),
		watson_streaming.Transcriber(settings, apikey='D8V1hwcYbr_F-EW6m2fddTvQX3kQ8s99D1G8cDwbIExV', hostname='us-east', instance_id='c72b4fe4-66b0-4788-a795-1387e5595e5e'),
		PrinterProducer(),
		ViolationChecker(),
	]

	fluteline.connect(nodes)
	fluteline.start(nodes)

	try:
		while True:
			time.sleep(10)
	except KeyboardInterrupt:
		pass
	finally:
		fluteline.stop(nodes)

def main():
	startSTT()

if __name__ == '__main__':
	main()