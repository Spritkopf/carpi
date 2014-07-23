from random import shuffle
from kivy.app import App
from kivy.core.audio import SoundLoader, Sound
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import OptionProperty, StringProperty, BooleanProperty, NumericProperty
from kivy.lang import Builder
from mediaprovider import MediaProvider
from audiobookprovider import AudiobookProvider
from mutagen.mp3 import MP3
from kivy.graphics import Color,Rectangle

Builder.load_string('''
<AudioPlayer>:
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

class AudioPlayer(BoxLayout):
	shuffle = BooleanProperty(False)
	state = OptionProperty('stop',options=['play','stop'])
	mode = OptionProperty('Music',options=['Music','Audiobooks'])
	currentFile = StringProperty('')
	length = NumericProperty(0)
	sound = Sound()
	playlist = []
	shuffle_temp_playlist = []
	first_after_shuffle = False

	def load(self, filename):
		self.currentFile = filename
		if self.sound:
			self.sound.unload()

		self.sound = SoundLoader.load(filename)

		if self.sound:
			try:
				self.length = MP3(filename).info.length
			except:
				print 'No length information available'
			print ("Sound found at %s" % self.sound.source)
			print ("Sound is %.3f seconds" % self.length)
			self.read_meta_data()
			self.sound.play()
			self.state = 'play'

	def play(self):
		print 'Play'
		if self.sound:
			self.sound.load()
			self.sound.play()
			self.state = 'play'

	def pause(self):
		print 'Pause'
		if self.sound:
			self.sound.stop()
			self.state = 'stop'

	def stop(self):
		if self.sound:
			self.sound.stop()
			self.sound.seek(0)
			self.state = 'stop'

	def next(self):
		if self.sound:
			self.sound.stop()

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

	def previous(self):
		if self.sound:
			self.sound.stop()
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

	def getPos(self):
		return self.sound.get_pos()

	def getLength(self):
		return self.sound.length

	def seek(self, percent):
		#self.sound.seek(seconds)
		print 'seek to %f seconds' % (percent*self.length)

	def seek_relative(self, difference):
		#self.sound.seek(self.sound.get_pos()+difference)
		print 'seek to %f seconds by %d' % (self.sound.get_pos()+difference,difference)

	def setVolume(self, vol):
		self.sound.volume = vol

	def read_meta_data(self):
		if self.mode=='Audiobooks':
			metadata = AudiobookProvider(None).get_file_info(self.currentFile)
			self.title = '%s (%s/%s)' % (str(metadata['title']),self.get_current_index()+1, len(self.playlist))
			self.artist = str(metadata['author'])
			self.cover = str(metadata['cover'])
		else:
			metadata = MediaProvider(None).getSongInfo(self.currentFile)
			self.title = str(metadata['title'])
			self.artist = str(metadata['artist'])
			self.album = str(metadata['album'])
			self.cover = str(metadata['cover'])

		del metadata

	def get_current_index(self):
		for i in range(len(self.playlist)):
			if self.playlist[i] == self.currentFile:
				return i

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
		if super(AudioPlayer, self).on_touch_down(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			with self.canvas.after:
				Color(.3,.8,.3,.5)
				Rectangle(size=self.size, pos=self.pos)


	def on_touch_up(self, touch):
		if super(AudioPlayer, self).on_touch_up(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			self.canvas.after.clear()

			App.get_running_app().change_screen(self.mode)

	def on_mode(self, *args):
		self.playlist = []




