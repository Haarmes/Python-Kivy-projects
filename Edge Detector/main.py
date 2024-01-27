from kivy.app import App    
from urllib.request import urlopen, urljoin
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle
from kivy.cache import Cache
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.slider import Slider
import cv2 as cv
import numpy as np
import os


class MainWidget(BoxLayout):
    max_arvo = NumericProperty(500)
    black_box_active = False
    black_box_size = ListProperty([0,0])
    blur_value = 1
    canny_value = 0
    canny2_value = 0
    gray_scale_image = False
    canny_image = False
    image_displayed = StringProperty("C:\\Users\\SeveriR\\Koodailu\\Kivy\\Edge Detector\\file_for_kivy.png")
    img = cv.imread("C:\\Users\\SeveriR\\Koodailu\\Kivy\\Edge Detector\\images\\Flamingo.jpg")
    print(type(img))
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(img, (blur_value,blur_value), cv.BORDER_DEFAULT)

    if canny_image == True:
        canny = cv.Canny(blur,canny_value,canny2_value)
        cv.imwrite("C:\\Users\\SeveriR\\Koodailu\\Kivy\\Edge Detector\\file_for_kivy.png", canny)
    else:
        cv.imwrite("C:\\Users\\SeveriR\\Koodailu\\Kivy\\Edge Detector\\file_for_kivy.png", blur)


    def __init__(self, **kwargs):   
        super().__init__(**kwargs)

    def get_images(self):
        array_of_pictures = os.listdir("C:\\Users\\SeveriR\\Koodailu\Kivy\\Edge Detector\\images")
        print(array_of_pictures)
        self.ids.stack_id.clear_widgets(children= None)
        for picture in array_of_pictures:
            print("found picture:", picture)
            temp_button = Button(text = picture, size_hint = (0.9, None), height= 30)
            temp_button.bind(on_press=self.change_image)
            self.ids.stack_id.add_widget(temp_button)
    
    def go_fullscreen_image(self):
        global full_image
        self.black_box_active = True
        full_image = Image(source="C:\\Users\\SeveriR\\Koodailu\\Kivy\\Edge Detector\\file_for_kivy.png",size_hint=(None,None), size= Window.size)
        cancel_fullscreen_button = Button(text ="Exit") 
        cancel_fullscreen_button.bind(on_press=self.exit_fullscreen) 
        Window.bind(on_resize=self.resize_fullscreen_image)
        self.black_box_size = Window.size
        self.ids.anchor_id.add_widget(full_image)   
        self.ids.anchor2_id.add_widget(cancel_fullscreen_button)       
    
    def exit_fullscreen(self, value):
        self.ids.anchor_id.clear_widgets(children=None)
        self.ids.anchor2_id.clear_widgets(children=None)
        self.black_box_size = [0,0]
        self.black_box_active = False

    def resize_fullscreen_image(self,*args ):
        full_image.size = Window.size
        if self.black_box_active:
            self.black_box_size = Window.size
        print(self.black_box_size)


    def on_enter(self, value):
        print(value)  
        print(value.text)  
        image_save_path = "C:\\Users\\SeveriR\\Koodailu\\Kivy\\Edge Detector\\Saved\\" + value.text + ".jpg"
        print(image_save_path)
        print(type(image_save_path))    
        if self.canny_image == True:
            cv.imwrite(image_save_path, self.canny)
        else:
            cv.imwrite(image_save_path, self.blur)
        self.ids.anchor_id.clear_widgets(children= None)

    def text_input_make(self):
        textinput = TextInput(text = "filename", multiline=False)
        textinput.bind(on_text_validate=self.on_enter)
        self.ids.anchor_id.add_widget(textinput) 

    def update_kivy_image(self):
        Cache.remove('kv.image')
        Cache.remove('kv.texture')
        self.image_displayed = ""
        self.image_displayed = "C:\\Users\\SeveriR\\Koodailu\\Kivy\\Edge Detector\\file_for_kivy.png"
        

    def change_image(self, value):
        self.img = cv.imread("C:\\Users\\SeveriR\\Koodailu\\Kivy\\Edge Detector\\images\\" + value.text)
        self.write_image_again()


    def write_image_again(self):
        if self.gray_scale_image == True:
            self.gray_image = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
            self.blur = cv.GaussianBlur(self.gray_image, (self.blur_value,self.blur_value), cv.BORDER_DEFAULT)
        else:
            self.blur = cv.GaussianBlur(self.img, (self.blur_value,self.blur_value), cv.BORDER_DEFAULT)
        if self.canny_image == True:
            self.canny = cv.Canny(self.blur,self.canny_value,self.canny2_value)
            cv.imwrite("C:\\Users\\SeveriR\\Koodailu\\Kivy\\Edge Detector\\file_for_kivy.png", self.canny)
        else:
            cv.imwrite("C:\\Users\\SeveriR\\Koodailu\\Kivy\\Edge Detector\\file_for_kivy.png", self.blur)

        self.update_kivy_image()

    def change_blur_value(self, value):
        self.blur_value = int(value)
        print(value)
        self.write_image_again()

    def change_grayscale(self, value):
        print(value)
        self.gray_scale_image = value
        self.write_image_again()

    def change_canny(self, value):
        self.canny_image = value
        self.write_image_again()

    def change_canny_value(self, value):
        self.canny_value = int(value)
        print(value)
        self.write_image_again()

    def change_canny2_value(self, value):
        self.canny2_value = int(value)
        print(value)
        self.write_image_again()


class EdgeApp(App):
    pass

EdgeApp().run()

