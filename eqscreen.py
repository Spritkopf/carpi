from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.graphics import Rectangle, Color
from kivy.storage.jsonstore import JsonStore
from kivy.uix.modalview import ModalView
from kivy.uix.actionbar import ActionButton, ActionGroup, ActionItem
from kivy.uix.spinner import Spinner, SpinnerOption


Builder.load_string('''
<EQScreen>:
	name: 'Equalizer'
	preset_title: preset_title
	on_enter: self.init()
	BoxLayout:
		id: eqlayout
		spacing: 5
		size_hint:(.8,.7)
		pos_hint:{'center_x':.5}
		y: 50
		canvas.after:
			Color:
				rgb: (0,0,0)
			Line:
				points: (self.x,self.y,self.x+self.width,self.y)
			Line:
				points: (self.x,self.y+self.height,self.x+self.width,self.y+self.height)
			Line:
				points: (self.x,self.y+(self.height/36)*24,self.x+self.width,self.y+(self.height/36)*24)
		EQBar:
			id: band0
			frequency: '30'
			index: 0
		EQBar:
			id: band1
			frequency: '60'
			index: 1
		EQBar:
			id: band2
			frequency: '120'
			index: 2
		EQBar:
			id: band3
			frequency: '240'
			index: 3
		EQBar:
			id: band4
			frequency: '450'
			index: 4
		EQBar:
			id: band5
			frequency: '1k'
			index: 5
		EQBar:
			id: band6
			frequency: '1.9k'
			index: 6
		EQBar:
			id: band7
			frequency: '3.7k'
			index: 7
		EQBar:
			id: band8
			frequency: '7.5k'
			index: 8
		EQBar:
			id: band9
			frequency: '15k'
			index: 9

	Label:
		id: preset_title
		color: (0,0,0,1)
		x: root.width/2 - self.width/2
		y: eqlayout.x + eqlayout.height - 10
		size: (root.width/2,50)
		text_size: self.size
		halign: 'center'
		text: 'sfdsfsdf'
		font_name: './fonts/RobotoCondensed-Light.ttf'
		font_size: '22sp'



	


<EQBar>:
	value: 0
	frequency: '0'
	dbLabel: dbLabel
	bar_height: 7
	spacing: 3
	size_hint:(1,1)
	canvas.before:
		Color:
			rgb: (1,1,1)
		Rectangle:
			size: self.size
			pos: self.pos

	Label:
		id: dbLabel
		color: (0,0,0,1)
		pos:root.pos
		size: (root.width,20)
		text_size: self.size
		halign:'center'
		text: '%.1f dB' % root.value
		font_name: './fonts/RobotoCondensed-Light.ttf'

	Label:
		color: (0,0,0,1)
		pos:(root.x,root.y-self.height-10)
		size: (root.width,20)
		text_size: self.size
		halign:'center'
		text: root.frequency
		font_name: './fonts/RobotoCondensed-Light.ttf'



	''')

class EQScreen(Screen):

	changed = BooleanProperty(False)

	def __init__(self, **args):
		super(EQScreen, self).__init__(**args)

		

	def load_preset(self,inst, key):

		store = JsonStore('eq_presets.json')
		if store.exists(key):
			self.preset_title.text = key
			self.store_config(key)

			bands = store[key]['bands']
			for x in xrange(10):
				self.ids['band'+str(x)].value = bands[x]
				self.ids['band'+str(x)].paint_bars()
		self.changed = False

	def on_changed(self,inst,value):
		self.actionItems['accept'].disabled = not value
		self.actionItems['accept'].opacity = 1 if value else 0
		self.actionItems['accept'].width = 40 if value else 1

	def init(self):

		## Define ActionItems
		self.actionItems = {
		'spinner': ActionSpinner(id='ctx_1', color=(.3,.3,.3,1), option_cls=new_option),
		'new': ActionButton(id='ctx_2', icon='theme/action_new.png',on_release=self.new_preset),
		'accept': ActionButton(id='ctx_3', icon='theme/action_accept.png',on_release=self.save, disabled=True, opacity=0, width=1)
		}

		## Set up the spinner
		self.current_preset = App.get_running_app().config.getdefault('Audio','eq_preset','standard')
		store = JsonStore('eq_presets.json')
		
		self.actionItems['spinner'].bind(text=self.load_preset)
		for preset in store.keys():
			self.actionItems['spinner'].values.append(preset)
		self.actionItems['spinner'].text = self.current_preset

		## Add Items to ActionBar
		for item in self.actionItems:
			App.get_running_app().root.bar.children[0].add_widget(self.actionItems[item])


	def new_preset(self, *args):
		self.actionItems['spinner'].text = '<custom>'
		self.changed = True

	def save(self,*args):
		if self.actionItems['spinner'].text == '<custom>':

			self.mv = Builder.load_string('''
ModalView:
	id: mv
	txt_input: txt_input
	saveBtn: saveBtn
	size_hint: (None,None)
	size: (400,200)
	canvas:
		Color:
			rgb: (1,1,1)
		Rectangle:
			pos: self.pos
			size: self.size
	FloatLayout:
		Label:
			color: (0,0,0,1)
			x: root.x
			y: root.y + root.height - 35
			size: (root.width,20)
			text_size: self.size
			halign:'center'
			text: 'Enter name'
			font_name: './fonts/Roboto-Light.ttf'
			font_size: '18sp'
		TextInput:
			id: txt_input
			multiline: False
			size_hint: (None,None)
			size: (root.width*0.7,50)
			x: root.x + root.width*0.15
			y: root.y + 85
			font_size: '22sp'
			halign: 'center'
		Button:
			id: saveBtn
			color: (0,0,0,1)
			text: 'Save'
			size_hint: (None,None)
			size: (200,60)
			x: root.x + root.width/2 - self.width/2
			y: root.y + 10
			on_release: root.dismiss()
''')
			self.mv.saveBtn.bind(on_release=self.save_preset)
			self.mv.open()
		else:
			store = JsonStore('eq_presets.json')
			bands = []
			for x in xrange(10):
				bands.append(round(float(self.ids['band'+str(x)].value),1))
			store.put(self.preset_title.text,bands=bands)
			self.changed = False


	def save_preset(self,*inst):
		#preset_name = inst.txt_input.text
		preset_name = self.mv.txt_input.text
		store = JsonStore('eq_presets.json')

		bands = []
		for x in xrange(10):
			bands.append(round(float(self.ids['band'+str(x)].value),1))

		store.put(preset_name,bands=bands)
		
		self.preset_title.text = preset_name
		self.actionItems['spinner'].values.append(preset_name)
		self.actionItems['spinner'].text = preset_name
		self.changed = False

	def store_config(self,preset_name):
		App.get_running_app().config.set('Audio','eq_preset',preset_name)
		App.get_running_app().config.write()
		


class EQBar(Widget):
	value = NumericProperty()
	def __init__(self,**args):
		super(EQBar,self).__init__(**args)
	
	def on_touch_down(self, touch):
		if super(EQBar, self).on_touch_down(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			self.set_value((touch.pos[1]-self.y)/self.height)
			return True

	def set_value(self, pos):
		self.value = 36*pos-24
		
		#if not self.parent.parent.changed:
		#	self.parent.parent.append_preset()
		self.parent.parent.changed = True
		self.paint_bars()
		

	def paint_bars(self):
		value = (float(self.value)+24)/36
		target_value = int(self.height*value/(self.bar_height+self.spacing))+1

		self.dbLabel.y = self.y+int(self.height*value)+5
		self.canvas.after.clear()
		for x in xrange(target_value):
			self.canvas.after.add(Color(value/3,.7,.7, mode='hsv'))
			#self.canvas.after.add(Color(-value+1,-value+1,-value+1, mode='rgb'))
			self.canvas.after.add(Rectangle(size=(self.width, self.bar_height),pos=(self.x,self.y+(x*(self.bar_height+self.spacing)))))

	def on_value(self,instace, value):
		App.get_running_app().root.player.bands[self.index] = value

class ActionSpinner(Spinner,ActionItem):
	text = StringProperty()

class new_option(SpinnerOption):
	color = (.3,.3,.3,1)