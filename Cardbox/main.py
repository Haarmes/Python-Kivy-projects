from kivy.app import App    
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color
from kivy.cache import Cache
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.slider import Slider
import numpy as np
import os
import random

class Pile():
    def __init__(self, pos) -> None:
        self.cards_in_pile = []
        self.allowed_cards = ""
        self.pos = pos

    def card_to_pile(self, card): #put card into this pile
        self.cards_in_pile.append(card)

    def card_from_pile(self): #move card from this pile
        return_card = self.cards_in_pile[0]
        self.cards_in_pile = self.cards_in_pile[1:]
        return return_card

    def pile_len(self): #Returns length of pile
        return len(self.cards_in_pile)


class Card():
    def __init__(self, position, number, card_suit) -> None:
        self.position = position
        self.number = number
        self.card_suit = card_suit

    def get_suit(self): #Returns suit of card
        return self.card_suit

    def get_card_number(self): #Returns number on card (A1,A2,C5 etc)
        return self.number

    def get_card_position(self): #Returns card position (X,Y)
        return self.position

    def set_card_position(self, position): #Saves new (X,Y) values for card
        self.position = position
        print("Card position set to", position)

class DragButton(DragBehavior, Button):
    pass


class MainWidget(BoxLayout):
    draw_three = StringProperty("normal")
    cards = Pile((0,0))
    letterlist = ["A","B","C","D"]
    cards_on_table = []
    moving_card_currently = False
    cards_going_table = []
    for letter in letterlist:
        if letter == "A":
            temp_suit = "heart"
        if letter == "B":
            temp_suit = "diamond"
        if letter == "C":
            temp_suit = "spade"
        if letter == "D":
            temp_suit = "club"
        for card in range(13):
            cards.card_to_pile(Card((0,0) ,str (letter + str(card + 1)), temp_suit))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def restart_table(self):
        self.ids.middle_table_id.clear_widgets()
        self.draw_three = "normal"
        self.cards = Pile((0,0))
        self.moving_card_currently = False
        self.cards_on_table = []
        for letter in self.letterlist:
            if letter == "A":
                temp_suit = "heart"
            if letter == "B":
                temp_suit = "diamond"
            if letter == "C":
                temp_suit = "spade"
            if letter == "D":
                temp_suit = "club"
            for card in range(13):
                self.cards.card_to_pile(Card((0,0) ,str (letter + str(card + 1)), temp_suit))

    def make_pile(self, kivy_object): 
        pass

    def add_pile(self): 
        pass
        

    def draw_top_card(self):
        if self.draw_three == "normal":
            if self.cards.pile_len() > 0:
                self.cards_going_table.append(self.cards.card_from_pile())
                self.update_visuals()
                
        else:
            if self.cards.pile_len() > 2:
                self.cards_going_table.append(self.cards.card_from_pile())
                self.cards_going_table.append(self.cards.card_from_pile())
                self.cards_going_table.append(self.cards.card_from_pile())
                self.update_visuals()

    def update_visuals(self):
        offset = 0
        for table_card in self.cards_going_table:

            if table_card.get_suit() == "heart" or table_card.get_suit() == "diamond":
                temp_color = (1,0,0)
            else:
                temp_color = (0,0,0)
            temp_button = DragButton(text=(table_card.get_card_number()),
                background_normal = "",
                halign = "left",
                background_color=(1,1,1,1),
                color= temp_color,
                size_hint = (None,None), 
                height = "200dp",
                width = "140dp",
                pos=(int(self.ids.card_deck_id.pos[0]+ 150 + offset),int(self.ids.card_deck_id.pos[1]-100)))
            temp_button.bind(on_press=self.table_card_press)
            temp_button.bind(on_touch_up=self.table_card_move_up)
            temp_button.bind(on_touch_move=self.table_card_drag)
            self.ids.middle_table_id.add_widget(temp_button)
            self.cards_on_table.append(table_card)
            offset += 20
        self.cards_going_table = []


    def shuffle_cards(self):
        random.shuffle(self.cards.cards_in_pile)
        print("Shuffled cards!")
        print(self.cards.pile_len())


    def table_card_press(self, value):
        for card in self.cards_on_table:
            if card.get_card_number() == value.text:
                pressed_card = card
        self.cards.card_to_pile(pressed_card)
        self.cards_on_table.remove(pressed_card)
        self.ids.middle_table_id.remove_widget(value)

    def table_card_move_up(self,value, touch):
        if self.moving_card_currently == True:
            print("card released")
            print(self.last_card_moved.text)
            for card in self.cards_on_table:
                if card.get_card_number() == self.last_card_moved.text:
                    card.set_card_position(self.last_card_moved.pos)
                    self.check_if_cards_stack(card, self.last_card_moved)
            self.moving_card_currently = False

    def table_card_drag(self,value, touch):
        if touch.grab_current is value:
            self.moving_card_currently = True
            self.last_card_moved = value

    
    def check_if_cards_stack(self, card_to_check, card_widget):
        card_to_check_x_y = card_to_check.get_card_position()
        for card in self.cards_on_table:
            if card.get_card_number() == card_to_check.get_card_number():
                continue
            card_x_y = card.get_card_position()
            if card_x_y[0] -50 < card_to_check_x_y[0] and card_x_y[0] +50 > card_to_check_x_y[0]:
                if card_x_y[1]-50 < card_to_check_x_y[1] and card_x_y[1] +50 > card_to_check_x_y[1]:
                    print("stacked!")
                    card_to_check.set_card_position((card_x_y[0], card_x_y[1]-30))
                    card_widget.pos = card_to_check.get_card_position()
            

    def table_card_release(self, value):
        print("huhuuuu")

    def table_deck_move(*args):
        print(args)
        print("Moving deck")

    def set_draw_three(self, value):
        print(value.state)
        if value.state == "down":
            self.draw_three = "down"
        else:
            self.draw_three = "normal"

class CardApp(App):
    def build(self):
        pass

CardApp().run()
