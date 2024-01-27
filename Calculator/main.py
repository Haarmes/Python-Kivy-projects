import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line

class MainWidget(BoxLayout):
    calculation_result = StringProperty("")
    current_display = StringProperty("0")
    current_mode = "firstNumber"
    current_operand = StringProperty("")
    current_numbers = StringProperty("")
    equal_pressed_last = False
    square_root = False
    last_operation = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def reset_calculator(self):
        self.calculation_result = ""
        self.current_display = "0"
        self.current_mode = "firstNumber"
        self.current_operand = ""
        self.current_numbers = ""
        self.equal_pressed_last = False
        self.square_root = False
        self.last_operation = ""

    def number_push(self, number):
        print(number)

        if self.equal_pressed_last == True:
            self.current_numbers += "+"
            self.current_display += "+"
            self.equal_pressed_last = False
        self.current_numbers += str(number)
        self.last_operation += str(number)
        if self.current_display == "0":
            self.current_display = str(number)
        else:
            self.current_display += str(number)


    def operand_push(self, operand):
        print(operand)
        if self.current_display == "0":
            self.current_display = ""
        self.last_operation = operand
        if self.equal_pressed_last == True:
            if operand == "square root":
                self.square_root = True
                self.current_numbers += ""
                self.current_display = "√" + self.current_display
                self.calculate()
            elif operand == "π":
                self.current_numbers += str(math.pi)
                self.current_display += operand
            else:
                self.current_numbers += operand
                self.current_display += operand
            self.equal_pressed_last = False
        else:
            if operand == "square root":
                self.square_root = True
                self.current_numbers += ""
                self.current_display = "√" + self.current_display
                self.calculate()
            elif operand == "π":
            
                self.current_numbers += str(math.pi)
                self.current_display += operand
            else:
                self.current_numbers += operand
                self.current_display += operand
        print(self.current_numbers)
        
    def backspace(self):
        self.current_numbers = self.current_numbers[:-1]
        self.current_display = self.current_display[:-1]

    def calculate(self):
        print(self.current_numbers)
        if self.equal_pressed_last == True:
            self.current_numbers = self.calculation_result
            if self.last_operation == "square root":
                self.current_display = "√" + self.calculation_result
                result = eval(str(math.sqrt(float(self.calculation_result))))
            else:
                self.current_display = self.current_numbers + self.last_operation
                result = eval(self.current_numbers + self.last_operation)
        else:
            result = eval(self.current_numbers)
        self.equal_pressed_last = True
        if self.square_root == True:
            result = math.sqrt(result)
            self.square_root = False
        self.calculation_result = str(result)
        print(result)


     
class CalculatorApp(App):
    pass


CalculatorApp().run()