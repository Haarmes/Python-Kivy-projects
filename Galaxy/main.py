from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)


    V_NB_LINES = 7
    V_LINES_SPACING = .1
    vertical_lines = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #print("INIT W:" + str(self.width) + " H:" + str(self.height))
        self.init_vertical_lines()


    def on_parent(self, widget, parent):
        pass
        #print("On Parent W:" + str(self.width) + " H:" + str(self.height))

    def on_size(self, *args):
        print("On Size W:" + str(self.width) + " H:" + str(self.height))
        #self.perspective_point_x = self.width/2
        #self.perspective_point_y = self.width * 0.75
        self.update_vertical_line()

    def on_perspective_point_x(self, widget, value):
        pass
        #print("PX:", str(value))

    def on_perspective_point_y(self, widget, value):
        pass
        #print("PY:", str(value))

    def init_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            #self.line = Line(points=[100, 0, 100, 100])
            for i in range(0 ,self.V_NB_LINES):
                self.vertical_lines.append(Line())


    def update_vertical_line(self):
        central_line_x = int(self.width/2)
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES/2)
        #self.line.points = [center_x, 0 , center_x, 100]
        for i in range(0 ,self.V_NB_LINES):
            line_x = int(central_line_x + offset*spacing)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1


    def transform(self, x, y):
        #return self.transform_2D(x, y)
        return self.transform_perspective(x, y)

    def transform_2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self,x,y):
        tr_y = y *  self.perspective_point_y / self.height
        if tr_y > self.perspective_point_y:
            tr_y = self.perspective_point_y
        return int(x), int(tr_y)


class GalaxyApp(App):
    pass


GalaxyApp().run()