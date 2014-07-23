from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('navigationdrawer.kv')

class NavigationDrawer(FloatLayout):
	def open(self):
	 	self.disabled = True
	 	anim = Animation(opacity=1, t='in_quad', duration=.3)
	 	anim2 = Animation(x=0, t='in_quad', duration=.3)
	 	anim.start(self.outside)
	 	anim2.start(self.panel)

 	def close(self):
	 	self.disabled = True
	 	anim = Animation(opacity=0, t='in_quad', duration=.3)#+Animation(width=0, duration=.1)
	 	anim2 = Animation(x=-250, t='in_quad', duration=.3)
	 	anim.start(self.outside)
	 	anim2.start(self.panel)

# 	def on_touch_down(self, touch):
# #		if not self.collide_point(touch.x, touch.y):
# #			return False

# 		if self.outside.collide_point(touch.x, touch.y):
# 			self.close()
# 			#return True
# #		if self.panel.collide_point(touch.x, touch.y):
# #			print 'fdgfdg'
# #			return False

class DrawerItem(BoxLayout):
 	screen1 = StringProperty('sd')
# 	def on_touch_down(self, touch):
# 		print self.y
# 		# if not self.collide_point(touch.x, touch.y):
# 		# 	return False
# 		# else:
# 		# 	print 'item'
# 		# 	self.press()
# 		if self.collide_point(touch.x, touch.y):
# 			print 'item geklickt'

# 	def on_touch_up(self, touch):
# 		if super(DrawerItem, self).on_touch_down(touch):
# 			return True
# 		if not self.collide_point(touch.x, touch.y):
# 			return False
# 		else:
# 			self.release()

 	def abc(self):
 		self.icon = 'theme/action_settings.png'
 		with self.canvas:
 			Color(.3,.8,.3,.5)
 			Rectangle(size=self.size, pos=self.pos)

# 	def release(self):
# 		self.canvas.after.clear()
# 		App.get_running_app().change_screen(self.screen)
		

