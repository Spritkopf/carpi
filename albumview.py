from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from mediaprovider import MediaProvider
from kivy.uix.actionbar import ActionButton


from listitem import ListItem

Builder.load_file('albumview.kv')

class AlbumView(Screen):
	def __init__(self, **args):
		super(AlbumView, self).__init__(**args)

		self.show_artists()
		
	def show_artists(self):
		self.artistlist.artistlayout.clear_widgets()

		for i in MediaProvider(None).getArtistList():
			self.artistlist.artistlayout.add_widget(ArtistListItem(text=i[0]))

	def load_albums(self, list, artist):
		self.albumlist.albumlayout.clear_widgets()

		for i in MediaProvider(None).getAlbumList(artist):
			self.albumlist.albumlayout.add_widget(AlbumItem(album=i[0], artist=artist, cover=i[1], id=i[2]))
			print i
	
	def init_actionbar(self):
		self.actionItems = {
		'btn_refresh': ActionButton(
					id='ctx_1',
                    icon='theme/new/sync.png',
                    color=(.3,.3,.3),
                    on_release=self.refresh
                    )
		}
		for item in self.actionItems:
			App.get_running_app().root.bar.children[0].add_widget(self.actionItems[item])
	
	def refresh(self, *args):
		mediapath = App.get_running_app().config.getdefault('General','media_path','test')
		MediaProvider(mediapath).scan_media()

		self.show_artists()

class AlbumItem(BoxLayout):
 	album = StringProperty()
 	artist = StringProperty()
 	cover = StringProperty()
 	id = NumericProperty()

 	def on_touch_down(self, touch):
		if super(AlbumItem, self).on_touch_down(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			self.press()
			return True

	def on_touch_up(self, touch):
		if super(AlbumItem, self).on_touch_down(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			self.release()

	def press(self):
		with self.canvas.after:
			Color(.3,.8,.3,.5)
			Rectangle(size=self.size, pos=self.pos)

		### Close the albumview and load the songs of rhe selected Album into the MusicView
		App.get_running_app().music_load_album(self.id, self.cover)

	def release(self):
		self.canvas.after.clear()

class ArtistListItem(ListItem):
	icon = StringProperty('theme/equalizer.gif')
	albumlist = []
	def __init__(self, **args):
		super(ArtistListItem, self).__init__(**args)
		self.remove_widget(self.iconimg)
 	### Overwriting the press() method
 	def press(self):
 		super(ArtistListItem, self).press()

 		#print 'gepresst:', self.text, self.albumlist
 		self.parent.parent.parent.load_albums(self.albumlist, self.text)
