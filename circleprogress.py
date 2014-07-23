from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.app import App


#Builder.load_string('''
Builder.load_string('''
<CircleProgress>:
    size_hint: (None,None)
    radius: 30
    line_color: (0,0,0)
    fill_color: (.5,.7,.5)
    text_color: (0,0,0,1)
    value: .38
    font_size: '14sp'
    canvas:
        Color:
        	rgb: root.line_color
        Line:
        	circle: (self.x+root.radius,self.y+root.radius,root.radius)
            width: 1
            close: True

        Color:
        	rgb: root.fill_color
        Ellipse:
            pos: self.pos
            size: (2*root.radius, 2*root.radius)
            angle_start: 0
            angle_end: 360*root.value
            segments: 360
    Label:
        size: (60,30)
        text_size: self.size
        text: str(int(root.value*100)) + '%'
        color: root.text_color
        font_name: './fonts/RobotoCondensed-Regular.ttf'
        font_size: root.font_size
        pos: (root.x+root.radius-self.width/2,root.y+root.radius-self.height/2)
        valign: 'middle'
        halign: 'center'

''')

class CircleProgress(Widget):

	def __init__(self,**args):
		super(CircleProgress,self).__init__(**args)

