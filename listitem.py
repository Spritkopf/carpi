from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty


Builder.load_string('''
<ListItem>:
	size_hint: (None,None)
	orientation: 'horizontal'
	text: 'standard'
	#icon: ''
	number: -1
	background_normal: (1,1,1)
	text_color: (0,0,0,1)
	iconimg: iconimg
	icon_visible: False
	canvas:
		Color:
			rgb: self.background_normal
		Rectangle:
			size: self.size
			pos: self.pos
		Color:
			rgb: (.7,.7,.7)
		Line:
			points:[self.x,self.y,self.x+self.width,self.y]
			width:1
	Label:
		text: str(root.number) + '.' if root.number>0 else ''
		size_hint_x: .1
		color: root.text_color
	Image:
		id: iconimg
		size_hint_x: .2
		source: root.icon
		opacity: 1 if root.icon_visible else 0
		anim_delay: .05
		allow_stretch: False

	Label:
		
		halign: 'left'
		valign: 'middle'
		text_size: (self.width,50)
		font_size: '14sp'
		font_name: './fonts/Roboto-Regular.ttf'
		padding_x: -20
		color: root.text_color
		text: root.text
		''')

class ListItem(BoxLayout):	
	icon = StringProperty('')
	def __init__(self, **args):
		super(ListItem, self).__init__(**args)
		
		if 'text' in args:
			self.text = args['text']

		if 'icon' in args:
			self.icon = args['icon']
		if 'number' in args:
			self.number = args['number']

	def on_touch_down(self, touch):
		if super(ListItem, self).on_touch_down(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			self.press()
			return True

	def on_touch_up(self, touch):
		if super(ListItem, self).on_touch_up(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			self.release()

	def press(self):
		with self.canvas.after:
			Color(.3,.8,.3,.5)
			Rectangle(size=self.size, pos=self.pos)

	def release(self):
		self.canvas.after.clear()
