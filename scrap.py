from bs4 import BeautifulSoup
import urllib.request as urllib2

# for Text to Speech
import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS

class Last_fm():
	# For list.fm
	def extract_artists(self,t):
		artsts = []
		for artists in t.find_all('td', class_="globalchart-track-artist-name", limit=10):
			artist = artists.findChildren('a')
			for arti in artist:
				artsts.append(arti.text)		
		return artsts

	# For last.fm	
	def extract_tracks(self,t):
		tracks = t.find_all('a', class_="link-block-target", limit=10)
		trks = []
		artsts = self.extract_artists(t)
		for track in tracks:
			trks.append(track.text)
		
		#print(trks)
		file = open("audios/to_speak.txt", "w+")
		for i,j in zip(trks,artsts):
			track_name = i+ " By "+j
			file.write(track_name)
			file.write('\n')
		file.close()

	# Scrap Last.fm
	def scrap_last_fm(self):
		# Query (Top Tracks, Top Artists, Most loved)
		q = "Top Tracks"

		# List.fm url
		url = 'https://www.last.fm/music'

		# url to html
		response = urllib2.urlopen(url) 
		html = response.read()
		
		# scrap 
		soup = BeautifulSoup(html,"lxml")
		for tag in soup.find_all("div",class_='music-charts-col'):
			child = tag.findChildren('h2')
			for schild in child:
				if schild.text == q:
					self.extract_tracks(tag)
					break

					
class Billboard():
	def scrap_billy(self):
		
		# Billboard url
		url = 'http://www.billboard.com/charts/hot-100'

		# url to html
		response = urllib2.urlopen(url)
		html = response.read()
		tracks = []
		artists = []
		
		# scrap Tracks
		soup = BeautifulSoup(html,"lxml")
		for li in soup.find_all("h2", class_='chart-row__song', limit=10):
			tracks.append(li.text)
		
		# scrap Artists
		for li in soup.find_all("a", class_='chart-row__artist', limit=10):
			artists.append(li.text.strip('\n').strip(' '))
		
		#print(artists)
		#for i, j in zip(tracks, artists):
		#	print(str(i) + " By "+ str(j))
			
		file = open("audios/to_speak.txt", "w+")
		for i,j in zip(tracks,artists):
			track_name = i+ " By "+j
			file.write(track_name)
			file.write('\n')
		file.close()
					
# Text to Speech
def speak_top_10(site, audioString):
	print(audioString)
	if site == "Last.fm":
		str = "Top 10 songs on "+ "Last dot fm" + " are, "+ audioString
	else:
		str = "Top 10 songs on "+ site + " are, "+ audioString
	tts = gTTS(text=str, lang='en')
	tts.save("audios/audio.mp3")
	os.system("mpg123.exe audios/audio.mp3")
	os.remove("audios/audio.mp3")

	
# Record Audio
def recordAudio():
    # Record Audio
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)
 
    # Speech recognition using Google Speech Recognition
	data = ""
	try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		data = r.recognize_google(audio)
		print("You said: " + data)
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
	return data



#recordAudio()


q = input('Top 10 list from ?(Last.fm/Billboard): ')
if q == "billboard".lower():
	bill = Billboard()
	bill.scrap_billy()
	fil = open('audios/to_speak.txt','r')
	data = fil.read()
	speak_top_10("Billboard", data)
elif q == "last.fm".lower():
	lstfm = Last_fm()
	lstfm.scrap_last_fm()
	fil = open('audios/to_speak.txt','r')
	data = fil.read()
	speak_top_10("Last.fm", data)
