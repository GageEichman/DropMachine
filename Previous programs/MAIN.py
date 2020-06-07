import kivy
kivy.require('1.11.1') # replace with your current kivy version !


#imports kivy (1.11.1)

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import os

class InputPage(GridLayout):
    def __inti__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        
        self.add_widget(Label(text = "NUM PAD!!!!!!!!!!!"))
        

class TOP_page(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 2
        
        #time interval row
        self.add_widget(Label(text = "Time interval: "))
        self.time_int = TextInput(multiline = False)
        self.add_widget(self.time_int)        
        self.update_time = Button(text = "update time interval")#binds button to method update
        #button change screen
        #self.update_time.bind(on_press = self.getpage)#on press      (current stopage 9/12)
        
        self.add_widget(self.update_time) #finalize widget

                
    
        #drop height row  
        self.add_widget(Label(text = "Drop Height: "))
        self.drop_height = TextInput(multiline = False)
        self.add_widget(self.drop_height)      
        self.update_height = Button(text = "update drop height")#binds button to method update
    
        self.add_widget(self.update_height) #finalize widget
        
        #METHODS
        #def getpage(*args):
           # sys_instance.screen_manager.current = "update"
            
        
        
        
        
class GUI(App):
    def build(self):
        #return TOP_page()
        self.screen_manager = ScreenManager()
        
        #page 1 ( default display) REMEMBER CASE!!!!!
        self.Top_p = TOP_page()
        screen = Screen(name="TOP")
        screen.add_widget(self.Top_p)
        self.screen_manager.add_widget(screen)
        
        #page 2 ( input screen / num pad)
        self.input_page = InputPage()
        screen = Screen(name = "update")
        screen.add_widget(self.input_page)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager                   


if __name__ == '__main__':
    sys_instance = GUI()
    sys_instance.run()
