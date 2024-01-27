from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, Clock
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse
from kivy.graphics.context_instructions import Color



class WidgetsExample(GridLayout):
    my_text = StringProperty("Hello!")
    my_counter = 0
    counter_enabled = BooleanProperty(False)
    text_input_str = StringProperty("")
    # slider_value_txt = StringProperty("0")


    def on_switch_active(self, widget):
        print("Switch:", str(widget.active))

    def on_button_click(self):
        print("Button clicked!")
        if self.counter_enabled == True:
            self.my_counter += 1
            self.my_text = str(self.my_counter)


    def on_toggle_button_state(self, toggle_button):
        print("toggled: " + toggle_button.state)
     
        if toggle_button.state == "normal":
            toggle_button.text = "Off"
            self.counter_enabled = False
        else:
            toggle_button.text = "On"
            self.counter_enabled = True

    def on_text_validate(self, widget):
        self.text_input_str = widget.text

    # def on_slider_value(self, widget):
        # print("value:", str(int(widget.value)))
        # self.slider_value_txt = str(int(widget.value))

class StackLayoutExample(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "rl-bt"
        size = dp(100)
        for i in range(0,100):
            b = Button(text=str(i+1), size_hint = (None,None), size=(size, size))
            self.add_widget(b)

class GridLayoutExample(GridLayout):
    pass

class AnchorLayoutExample(AnchorLayout):
    pass

class BoxLayoutExample(BoxLayout):
    pass
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#        self.orientation = "vertical"
#        b1 = Button(text="A")
#        b2 = Button(text="B")
#        b3 = Button(text="C")
#        self.add_widget(b1)
#        self.add_widget(b2)
#        self.add_widget(b3)
    
class MainWidget(Widget):
    pass

class TheLabApp(App):
    pass

class CanvasExample4(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Line(points=(100,100,400,500), width=2)
            Color(0,1,0)
            Line(circle=(400,200,80), width=2)
            Line(rectangle=(700,500,150, 100), width=5)
            self.rect = Rectangle(pos=(700,200), size=(150,100))

    def on_button_a_click(self):
        inc = dp(10)
        x, y = self.rect.pos
        w, h = self.rect.size
        if x < self.width-w-inc:
            x += inc
        if x + w > self.width:
            x = self.width-w
    
        self.rect.pos = (x,y)

class CanvasExample5(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_size = dp(50)
        self.vx = dp(3)
        self.vy = dp(3)
        with self.canvas:
            self.ball = Ellipse(pos=self.center, size=(self.ball_size, self.ball_size))
        Clock.schedule_interval(self.update,1/60)

    def on_size(self, *args):
        print("on size :", str(self.width) + ", " + str(self.height))
        self.ball.pos = (self.center_x-self.ball_size/2, self.center_y-self.ball_size/2)

    def update(self, dt):
        print("update")
        x, y = self.ball.pos

        x += self.vx
        

        if x < self.width - self.ball_size and x > 0:
            self.ball.pos = (x, y)
        else:
            self.vx = -self.vx
        y += self.vy

        if y < self.height - self.ball_size and y > 0:
            self.ball.pos = (x, y)
        else:
            self.vy = -self.vy
       

class CanvasExample6(Widget):
    pass

class CanvasExample7(BoxLayout):
    pass

TheLabApp().run()