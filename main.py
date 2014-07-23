
### kivy modules ###
import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from kivy.properties import StringProperty

### custom modules ###
from navdrawer2 import NavDrawer
from musicscreen import MusicScreen
from albumview import AlbumView
from audiobookscreen import AudioBookScreen
from libraryview import LibraryView
from eqscreen import EQScreen

###  TEST MODULES ###
from mediaprovider import MediaProvider



class carpiApp(App):
	screen_title = StringProperty()
	def build(self):

		self.musicScreen = MusicScreen()
		self.albumView = AlbumView()
		self.audiobookScreen = AudioBookScreen()
		self.libraryView = LibraryView()
		self.eqScreen = EQScreen()

		self.drawer = NavDrawer()
		self.root.add_widget(self.drawer)

		self.root.sm.add_widget(self.musicScreen)
		self.root.sm.add_widget(self.albumView)
		self.root.sm.add_widget(self.audiobookScreen)
		self.root.sm.add_widget(self.libraryView)
		self.root.sm.add_widget(self.eqScreen)
		
		self.change_screen('Music')

	def build_config(self, config):
		config.setdefaults('General', {
        	'media_path': './test',
        	'audiobook_path': './test2'
        })
		
        
	def build_settings(self, settings):
		settings.add_json_panel('CarPi',self.config, 'settings.json')
		settings_screen = Screen(name='Settings')
		settings_screen.add_widget(settings)
		self.root.sm.add_widget(settings_screen)


	def display_settings(self, *args):
		self.last_displayed_screen = self.root.sm.current_screen.name
		self.change_screen('Settings')


	def close_settings(self, *args):
		self.change_screen(self.last_displayed_screen, True)



		
	
	def open_drawer(self):
		### Certain screens will cause the screenmanager to go back
		### to the previous screen, instead of opening the drawer
		current_screen = self.root.sm.current
		if(current_screen == 'AlbumView'):
			self.change_screen('Music', True)
		elif(current_screen == 'Settings'):
			self.close_settings()
		elif(current_screen == 'Library'):
			self.change_screen('Audiobooks', True)
		else:
			self.drawer.open()
	
	def test(self):
		print 'test: ', self.root.player.length

	def clear_actionbar_context(self):
		for item in reversed(self.root.bar.children[0].children):
			try:
				if 'ctx' in item.id:
					self.root.bar.children[0].remove_widget(item)
			except:
				pass


	def change_screen(self, screen_name, back=False):
		direction = 'right' if back else 'left'
		self.root.sm.transition=SlideTransition(duration=0.3,direction=direction)
		if screen_name != self.root.sm.current:
			self.clear_actionbar_context()
			self.root.sm.current = screen_name
		self.set_screen_title(screen_name)
		self.drawer.close()

		#self.set_actionbar_context(screen_name)

	# def set_actionbar_context(self, context):
	# 	### Workaround for the non-functioning ContextActionGroup Kivy class.
	# 	### Each contextual ActionItem has a property 'context' .If context matches 
	# 	###the current screen-name, the Item will be displayed

	# 	for item in self.root.bar.children[0].children:
	# 		try:					
	# 			if item.context in [context,'all']:
	# 				item.opacity = 1
	# 				item.width = 30
	# 			else:
	# 				item.opacity = 0
	# 				item.width = 0
	# 		except:
	# 			pass
		
	def set_screen_title(self, title):
		if title != None:
			self.screen_title = title

	def music_load_album(self, id, cover):
		print 'switching to album', id

		self.root.player.mode = 'Music'
		self.musicScreen.load_album(id)

		self.change_screen('Music', True)

	def audiobook_load_book(self, id):
		print 'loading book:', id

		if self.root.player.mode == 'Audiobooks':
			print 'TODO: call method to Save currentAudiobook state'
		self.root.player.mode = 'Audiobooks'
		self.audiobookScreen.load_book(id)

		self.change_screen('Audiobooks', True)
		
	def next_file(self):
		if not self.root.player.next():
			self.musicScreen.next_album()
	def prev_file(self):
		if not self.root.player.previous():
			self.musicScreen.prev_album()


if __name__ == '__main__':
	carpiApp().run()