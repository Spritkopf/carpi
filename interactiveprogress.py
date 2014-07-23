from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

Builder.load_string('''
<InteractiveProgress>:
    size_hint_y: None
    progress: progress
    ProgressBar:
    	id: progress
        size_hint_y: None
        width: root.width
        y: root.height/2 - root.offset
        max: 100
        value: 75
        opacity: .6
	''')

class InteractiveProgress(Widget):
	offset = NumericProperty()
	def __init__(self,**args):
		super(InteractiveProgress,self).__init__(**args)

	def on_touch_down(self, touch):
		if super(InteractiveProgress, self).on_touch_down(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			self.progress.value = touch.spos[0]*100 
			App.get_running_app().root.player.seek(touch.spos[0])
			return True

	def on_touch_up(self, touch):
		if super(InteractiveProgress, self).on_touch_up(touch):
			return True
		if not self.collide_point(touch.x, touch.y):
			return False
		else:
			return True