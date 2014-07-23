### Gstreamer 1.0 initialization
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
GObject.threads_init()
Gst.init(None)

from random import shuffle
from kivy.app import App
from kivy.core.audio import SoundLoader, Sound
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import OptionProperty, StringProperty, BooleanProperty, NumericProperty, ListProperty
from kivy.lang import Builder
from mediaprovider import MediaProvider
from audiobookprovider import AudiobookProvider
from mutagen.mp3 import MP3
from kivy.graphics import Color,Rectangle


Builder.load_string('''
<Player>:
	size_hint: (None,None)
	orientation: 'horizontal'
	artist: ''
	album: ''
	title: ''
	cover: ''

	Image:
        source: 'img/no_cover.png' if root.cover=='' else root.cover
        size_hint_x: .3
    BoxLayout:
    	orientation: 'vertical'
    	Label:	
            text: root.title
            font_name: './fonts/RobotoCondensed-Regular.ttf'
            font_size: '14sp'
            size_hint: (1,None)
            color: (0,0,0,1)
            height: 30
            text_size: (self.width,self.height)
            x:70
            y:30
            halign: 'left'
            valign:'middle'
        Label:
            text: root.artist
            font_name: './fonts/RobotoCondensed-Light.ttf'
            font_size: '14sp'
            size_hint: (1,None)
            color: (0,0,0,1)
            height: 30
            text_size: (self.width,self.height)
            x:70
            y:0
            halign: 'left'
            valign:'middle'

''')

class Player(BoxLayout):
	bands = ListProperty([0,0,0,0,0,0,0,0,0,0])
	volume = NumericProperty(0)
	mute = BooleanProperty(False)
	balance = NumericProperty(0)
	shuffle = BooleanProperty(False)
	status = OptionProperty('pause',options=['play','pause'])
	mode = OptionProperty('Music',options=['Music','Audiobooks'])
	currentFile = StringProperty('')
	length = NumericProperty(0)
	sound = Sound()
	playlist = []
	shuffle_temp_playlist = []
	first_after_shuffle = False

	def __init__(self,**args):
		super(Player,self).__init__(**args)

		self.pipeline = Gst.Pipeline()

		### File Source
		### properties:
		###		location  - file path
		self.filesrc = Gst.ElementFactory.make('filesrc',None)
		self.pipeline.add(self.filesrc)

		self.mp3decoder = Gst.ElementFactory.make('mad',None)
		self.pipeline.add(self.mp3decoder)

		self.audioconvert = Gst.ElementFactory.make('audioconvert',None)
		self.pipeline.add(self.audioconvert)

		### Equalizer
		###	properties:
		###	bandN	- N = [0...10], values from -24 .. +12 [dB]
		self.equalizer = Gst.ElementFactory.make('equalizer-10bands',None)
		self.pipeline.add(self.equalizer)

		###  Volume and Balance Elements
		###  properties:
		###	 audiovolume.volume  - volume 0...1
		###  audiopanorama.panorama - balance -1...1
		self.audiovolume = Gst.ElementFactory.make('volume',None)
		self.pipeline.add(self.audiovolume)
		self.audiopanorama = Gst.ElementFactory.make('audiopanorama',None)
		self.pipeline.add(self.audiopanorama)

		### Sink - Alsasink
		self.sink = Gst.ElementFactory.make('alsasink',None)
		self.pipeline.add(self.sink)

		self.filesrc.link(self.mp3decoder) 
		self.mp3decoder.link(self.audioconvert)
		self.audioconvert.link(self.equalizer)
		self.equalizer.link(self.audiovolume)
		self.audiovolume.link(self.audiopanorama)
		self.audiopanorama.link(self.sink)
     

	def load(self,filepath):

		self.pipeline.set_state(Gst.State.NULL)
		self.filesrc.set_property('location',filepath)
		self.currentFile = filepath
		self.read_meta_data()
		self.play()

	def next(self):
		if len(self.playlist)>0:
			if not self.first_after_shuffle:
				idx = self.get_current_index()		
			else:
				idx = -1
				self.first_after_shuffle = False
			print 'audioplayer: playlist=', self.playlist
			if idx < (len(self.playlist)-1):
				self.load(self.playlist[idx+1])
			else:
				print 'Ende der Liste erreicht'
				return False
			return True
		return True

	def previous(self):
		if len(self.playlist)>0:
			if not self.first_after_shuffle:
				idx = self.get_current_index()
			else:
				idx = 1
				self.first_after_shuffle = False
					
			if idx > 0:
				self.load(self.playlist[idx-1])
			else:
				print 'Anfang der Liste erreicht'
				return False
			return True
		return True

	def play(self):
		print 'Player: play'
		self.status = 'play'
		self.pipeline.set_state(Gst.State.PLAYING)

	def pause(self):
		print 'Player: pause'
		self.status = 'pause'
		self.pipeline.set_state(Gst.State.PAUSED)

	def seek(self, percent):
		#self.sound.seek(seconds)
		print 'seek to %f seconds' % (percent*self.length)

	def seek_relative(self, difference):
		#self.sound.seek(self.sound.get_pos()+difference)
		print 'seek to %f seconds by %d' % (self.sound.get_pos()+difference,difference)

	def setVolume(self, vol):
		self.volume = vol

	def read_meta_data(self):
		if self.mode=='Audiobooks':
			metadata = AudiobookProvider(None).get_file_info(self.currentFile)
			self.title = '%s (%s/%s)' % (str(metadata['title']),self.get_current_index()+1, len(self.playlist))
			self.artist = str(metadata['author'])
			self.cover = str(metadata['cover'])
		else:
			metadata = MediaProvider(None).get_song_info_db(self.currentFile)
			self.title = str(metadata['title'])
			self.artist = str(metadata['artist'])
			self.album = str(metadata['album'])
			self.cover = str(metadata['cover'])
			self.length = int(float(metadata['length']))

		del metadata

	def get_current_index(self):
		for i in xrange(len(self.playlist)):
			if self.playlist[i] == self.currentFile:
				return int(i)

	def togglePlayPause(self, state):
		if state == 'down':
			self.play()
		elif state =='normal':
			self.pause()

	def toggleShuffle(self, state):
		if state == 'normal':
			self.shuffle = False
		elif state =='down':
			self.shuffle = True

	def toggleMute(self, state):
		if state == 'normal':
			self.mute = False
		elif state =='down':
			self.mute = True



##############################################
#####		Event Handlers   #################
##############################################

	def on_shuffle(self, *args):
		if args[1]:
			print 'shuffling playlist...'
			self.shuffle_temp_playlist = list(self.playlist)
			shuffle(self.playlist)
			self.first_after_shuffle = True
		else:
			print 'restoring sorted playlist...'
			self.playlist = list(self.shuffle_temp_playlist)

	def on_touch_down(self, touch):
		if super(Player, self).on_touch_down(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			with self.canvas.after:
				Color(.3,.8,.3,.5)
				Rectangle(size=self.size, pos=self.pos)


	def on_touch_up(self, touch):
		if super(Player, self).on_touch_up(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			self.canvas.after.clear()

			App.get_running_app().change_screen(self.mode)

	def on_mode(self, *args):
		self.playlist = []

	def on_mute(self, inst, value):
		print 'mute?', value

	def on_bands(self,instance,value):
		for i in xrange(len(value)):
			self.equalizer.set_property('band'+str(i),value[i])

	def on_volume(self,instance,value):
		self.audiovolume.set_property('volume',value)

	def on_balance(self,instance,value):
		self.audiopanorama.set_property('panorama', value)

