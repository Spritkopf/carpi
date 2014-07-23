from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.graphics import Color,Rectangle
from kivy.lang import Builder

Builder.load_file('navdrawer2.kv')



class NavDrawer(FloatLayout):

	def __init__(self, **args):
		super(NavDrawer, self).__init__(**args)

	def on_touch_down(self, touch):
		if super(NavDrawer, self).on_touch_down(touch):
			return True
	def open(self):
	 	self.outside.disabled = True
	 	anim = Animation(opacity=1, t='in_quad', duration=.3)
	 	anim2 = Animation(x=0, t='out_quad', duration=.3)
	 	anim.start(self.outside)
	 	anim2.start(self.panel)
	def close(self):
	 	self.outside.disabled = False
	 	anim = Animation(opacity=0, t='in_quad', duration=.3)
	 	anim2 = Animation(x=-250, t='in_cubic', duration=.3)
	 	anim.start(self.outside)
	 	anim2.start(self.panel)