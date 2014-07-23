from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

Builder.load_string('''

<EqualizerScreen>:
	name: 'Equalizer'
	padding: 20
	BoxLayout:
		spacing: 5
		size_hint:(.8,.7)
		pos_hint:{'center_x':.5}
		y: 50
		EQBar:
		EQBar:
		EQBar:
		EQBar:
		EQBar:
		EQBar:
		EQBar:
		EQBar:
		EQBar:
		EQBar:

<EQBar>:
	value: .4
	orientation: 'lr-bt'
	canvas:
		Color:
			rgb: (1,1,1)
		Rectangle:
			size: self.size
			pos: self.pos
	size_hint: (1,1)
	height: 20
	spacing: 3

	EQpart:

		

<EQpart@Widget>:
	canvas:
		Color:
			hsv: (.8,1,1)
		Rectangle:
			size: self.size
			pos: self.pos

	size_hint:(1,None)
	height: 5


''')

class EqualizerScreen(Screen):
	def __init__(self, **args):
		super(EqualizerScreen, self).__init__(**args)

class EQBar(StackLayout):
	value = NumericProperty()
	def __init__(self,**args):
		super(EQBar,self).__init__(**args)

		self.bind(value=self.on_value)
	
	def on_touch_down(self, touch):
		if super(EQBar, self).on_touch_down(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:

			self.setValue(touch.pos[1])
			return True

	def setValue(self,ypos):
		count = len(self.children)
		currentValue = ((count*(self.spacing[0]+5))-self.spacing[0])/self.height
		value = (ypos-self.y)/self.height
		self.value = value

		if currentValue < value:
			diff = int(((value - currentValue)*self.height)/(self.spacing[0]+5))
			
			for x in xrange(diff):
				self.add_widget(EQPart())

		else:
			for bar in reversed(self.children):
				if bar.y > ypos:
					self.remove_widget(bar)
		#print currentValue, value

	def on_value(self,*args):
		print 'The value changed to: ',self.value

class EQPart(Widget):
	pass
	


