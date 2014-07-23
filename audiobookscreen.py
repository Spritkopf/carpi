from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from audiobookprovider import AudiobookProvider
from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.properties import NumericProperty
from os import path
from kivy.uix.actionbar import ActionButton

Builder.load_file('audiobookscreen.kv')

class AudioBookScreen(Screen):
	progress_part = NumericProperty(0)
	part_count = NumericProperty(1)
	progress = NumericProperty(0)

	loaded = False
	def __init__(self, **args):
		super(AudioBookScreen, self).__init__(**args)

	def load_book(self, id):
		book = AudiobookProvider(None).get_book(id)

		self.title = book['info']['title']
		self.author = book['info']['author']
		self.cover = book['info']['cover']
		self.part_count = len(book['files'])
		self.length = book['info']['length']
		self.progress_part = book['info']['progress_part']
		self.progress_pos = book['info']['progress_pos']

		if self.progress_part == 1:
			self.progress = self.progress_pos
		else:
			self.progress = AudiobookProvider(None).get_progress(id,self.progress_part) / float(self.length)
		print 'progress_part', self.progress_part
		self.files = []

		for item in book['files']:
			self.files.append(item[3])

		self.loaded = True


	def startPlayback(self):
		if self.loaded:
			print 'starting Playback'
			App.get_running_app().root.player.mode = 'Audiobooks'
			App.get_running_app().root.player.playlist = self.files
			App.get_running_app().root.player.load(self.files[self.progress_part-1])
			self.playOverlay.opacity = 0
			self.playOverlay.disabled = True

			App.get_running_app().root.player.bind(currentFile=self.test)



	def test(self,*args):
		print 'file changed...'

	def init_actionbar(self):
		self.actionItems = {
		'btn_library': ActionButton(
					id='ctx_1',
                    icon='theme/books.png',
                    color=(.3,.3,.3),
                    on_release=lambda *x: App.get_running_app().change_screen('Library')
                    )
		}
		for item in self.actionItems:
			App.get_running_app().root.bar.children[0].add_widget(self.actionItems[item])

