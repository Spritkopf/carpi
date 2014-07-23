from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.uix.actionbar import ActionButton
from listitem import ListItem
from mediaprovider import MediaProvider

###Test imports###
from kivy.uix.button import Button

Builder.load_file('musicscreen.kv')

class MusicScreen(Screen):
	current_id = 0
	def __init__(self, **args):
		super(MusicScreen, self).__init__(**args)
		self.mediapath = App.get_running_app().config.getdefault('Genral','media_path','')
		App.get_running_app().root.player.bind(currentFile=self.songChanged)

	def clear_songs(self):
		self.songlayout.clear_widgets()

	def add_song_item(self, number, text, length, path):
		self.songlayout.add_widget(SongListItem(number=number, text=text, length=length, filepath=path))
		App.get_running_app().root.player.playlist.append(path)

	def load_album(self, id):
		songlist = MediaProvider(self.mediapath).get_songs_by_album_id(id)
		self.current_id = id
		if len(songlist)>0:
			self.cover = songlist[0][4]
			self.clear_songs()
			App.get_running_app().root.player.mode = 'Music'
			App.get_running_app().root.player.playlist[:] = []
			for i in range(len(songlist)):
				self.add_song_item(songlist[i][3],songlist[i][0],float(songlist[i][1]),songlist[i][2])

			App.get_running_app().root.player.load(songlist[0][2])

	def next_album(self):
		self.load_album(MediaProvider(None).get_next_album_id(self.current_id))

	def prev_album(self):
		self.load_album(MediaProvider(None).get_next_album_id(self.current_id,-1))

	def songChanged(self,player,currentFile):
		## Callback routine called, when currently played file in the player instance changes

		if App.get_running_app().root.player.mode == 'Music':
			print "CurrentFile changed to:", currentFile

			for item in self.songlayout.children:
				if item.filepath==currentFile:
					item.icon_visible = True
				else:
					item.icon_visible = False

	def init_actionbar(self):
		self.actionItems = {
		'btn_album_view': ActionButton(
					id='ctx_1',
                    icon='theme/new/queue.png',
                    color=(.3,.3,.3),
                    screen='Music',
                    on_release=lambda *x: App.get_running_app().change_screen('AlbumView')
                    )
		}

		for item in self.actionItems:
			App.get_running_app().root.bar.children[0].add_widget(self.actionItems[item])


class SongListItem(ListItem):
	filepath = StringProperty()
	length = NumericProperty(0)
	icon = 'theme/equalizer.gif'
	def __init__(self, **args):
		super(SongListItem, self).__init__(**args)
		
		### Add Label for song length
		length = '%02d:%02d'%(self.length/60,self.length%60)
		self.add_widget(Label(text=str(length), size_hint_x=.17, height=30, color=(0,0,0,.5)))

		App.get_running_app().root.player.bind(status=self.playerStateChanged)
 	### Overwriting the press() method
 	def press(self):
 		super(SongListItem, self).press()
 		print 'gepresst:', self.text, self.number
 		App.get_running_app().root.player.load(self.filepath)

 	def playerStateChanged(self, player, state):

 		if player.currentFile == self.filepath:
 			if state == 'play':
 				self.icon_visible = True
 			elif state == 'pause':
 				self.icon_visible = False



 		