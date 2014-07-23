from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from os import path
from kivy.properties import StringProperty,NumericProperty
from kivy.uix.actionbar import ActionButton
from audiobookprovider import AudiobookProvider

Builder.load_string('''
#:import CircleProgress circleprogress.CircleProgress
<LibraryView>:
	bookLayout: bookLayout
	name: 'Library'
	on_enter: self.init_actionbar()
	GridLayout:
		id: bookLayout
		canvas.before:
			Color:
				rgb: .9, .9, .9
			Rectangle:
				size: root.size
				pos: (0,0)
		spacing: 20
		padding: 20
		rows: 1
		
		row_default_height: (self.height-2*self.padding[0])/self.rows
		row_force_default: True
		col_default_width: (self.width-2*self.padding[0])/3
		col_force_default: True


<BookItem>:
	orientation: 'vertical'
	canvas:
		Color:
			rgb: (1,1,1)
		Rectangle:
			size: self.size
			pos: self.pos
		Color:
			rgb: (.6,.6,.6)
		Line:
			points:[self.x,self.y,self.x+self.width,self.y]
			width:1
	Image:
		canvas:
			Color:
				rgb: (.6,.6,.6)
			Line:
				points:[self.x,self.y,self.x+self.width,self.y]
		size_hint_y: .6
		size_hint_x: 1
		source: 'img/no_cover.png' if root.cover == '' else root.cover
	RelativeLayout:
		size_hint: (1,.2)
		Label:
			size_hint: (.9,None)
			height: 30
			text_size: self.size
			text: root.title
			pos_hint: {'top': 1}
			x: 20
			color: (0,0,0,1)
			font_name: './fonts/Roboto-Regular.ttf'
			font_size: '18sp'
			halign: 'left'
			valign: 'middle'
		Label:
			size_hint: (.9,None)
			height: 30
			text_size: self.size
			text: root.author
			pos_hint: {'top': .7}
			x: 20
			color: (0,0,0,.8)
			font_name: './fonts/Roboto-Regular.ttf'
			font_size: '15sp'
			halign: 'left'
			valign: 'middle'
		Label:
			size_hint: (None,None)
			color: (0,0,0,1)
			size:(70,30)
			text_size: self.size
			text: str('%02d:%02d:%02d'%(root.length/3600,(root.length%3600)/60,(root.length%3600)%60))
			font_name: './fonts/RobotoCondensed-Regular.ttf'
			font_size: '14sp'
			pos_hint: {'top': 1}
			x: root.width - self.width - 20
			halign: 'right'
			valign: 'middle'

		CircleProgress:
			id: circleProgress
			size: (2*self.radius,2*self.radius)
			x: root.width - self.width - 20
			y: 20
			line_color:(.4,.4,.4)
			value: root.progress
			radius:17
''')

class LibraryView(Screen):
	def __init__(self, **args):
		super(LibraryView, self).__init__(**args)

		self.displayBooks()

	def displayBooks(self):
		
		booklist = AudiobookProvider(None).getAudiobookList()
		self.bookLayout.clear_widgets()

		for book in booklist:

			progress = book[7]/float(book[4])

			self.bookLayout.add_widget(BookItem(
				id=book[0],
				title=book[1],
				author=book[2], 
				cover=book[3],
				length=book[4],
				progress=progress))

	def refresh(self, *args):
		mediapath = App.get_running_app().config.getdefault('General','audiobook_path','test2')
		AudiobookProvider(mediapath).scanAudiobooks()

		self.displayBooks()

	def init_actionbar(self):
		self.actionItems = {
		'btn_refresh': ActionButton(
					id='ctx_1',
                    icon='theme/refresh.png',
                    color=(.3,.3,.3),
                    on_release=self.refresh
                    )
		}

		for item in self.actionItems:
			App.get_running_app().root.bar.children[0].add_widget(self.actionItems[item])
		


class BookItem(BoxLayout):
	id = NumericProperty()
	title = StringProperty()
	author = StringProperty()
	cover = StringProperty()
	length = NumericProperty()
	progress = NumericProperty()
	def __init__(self, **args):
		super(BookItem, self).__init__(**args)

	def on_touch_up(self, touch):
		if super(BookItem, self).on_touch_up(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			App.get_running_app().audiobook_load_book(self.id)