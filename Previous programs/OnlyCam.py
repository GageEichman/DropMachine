### imports ######
import picamera
#import keyboard

import kivy
import time
import sched
import threading

from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.graphics import Color

 ### configuration of the main window ###
from kivy.config import Config
from kivy.core.window import Window
Config.set('graphics', 'position', 'custom')    # allows for custom manipulation of window
Config.set('graphics', 'left' , 0)              # sets left most window boundary to the far left of screen
Config.set('graphics', 'top', 0)                # sets top most window boundary ro very top of screen
Window.fullscreen = 'auto'                      # sets the screen to fill the area marked by top and left in a rectangle
kivy.require('1.11.1')
# Config.set('graphics', 'width', '700')
# Config.set('graphics', 'height', '200')

drops_left = 3

camera= picamera.PiCamera()
camera.resolution = (1200, 1200)
camera.framerate = 15 #15 is max
camera.brightness = 75
camera.contrast = 0
#camera.start_preview(fullscreen=False, window =(100,50,1000,1000))

scheduler = sched.scheduler(time.time, time.sleep)


############################### GUI build #########################################################
# Builder is essentialy the .kv file without the extension
#root.manager.current = '' means go to that page
Builder.load_string("""

<CustButton@Button>:
    font_size: 32
    
<CustomPopup>:
    #pop1:pop1
    
    
    title: 'Warning!'
    size_hint: .5, .5
    auto_dismiss: False
    GridLayout:
        cols: 1
        Label:
            size_hint: .9, .9
            halign: 'center'
            valign: 'middle'
            text: 'This will delete all data, are you sure?'
            text_size: self.width, None
        Button:
            text: 'Yes, Im Sure'
            on_release:
                root.manager.get_screen('home').label2.flag == '1'
                root.dismiss()
                
            
#screen when it boots
<HomeScreen>:

    label1:label1
    label2:label2
    BoxLayout:
           
        padding:5
        orientation: "vertical"


        #Hard drop button
        CustButton:
            id:label1
            flag:'0'
            
            text:'5 sec record'
            font_size: 25
            size_hint:(.33,.3)
            pos_hint:{'bottom':.5,'right':1}
            
            on_press:
                if(root.manager.get_screen('home').label1.flag == '0'):root.manager.get_screen('home').label1.flag = '1'; root.manager.get_screen('home').label1.text = '5 sec record'
                #elif(root.manager.get_screen('home').label1.flag == '1'):root.manager.get_screen('home').label1.flag = '0'; root.manager.get_screen('home').label1.text = 'Start Recording'

        #soft drop button
        CustButton:
            id:label2
            flag:'0'
            
            text: 'Delete'
            font_size: 25
            size_hint:(.33,.3)
            pos_hint:{'top':.5,'right':1}
            
            on_press:
                root.open_popup()
                
                #if(root.manager.get_screen('home').label2.flag == '0'):root.manager.get_screen('home').label2.flag = '1';
                




""")

############################################################


class HomeScreen(Screen):
        
    def open_popup(self):
        the_popup = CustomPopup()
        the_popup.open()
        
    def start_stop(self):
        global drops_left
        
        if (sm.get_screen('home').label1.flag == '1'):
            while True:
                global drops_left
                HomeScreen.cam_record(self)
                print('doing other parts of loop')
                time.sleep(2)
                print('doing some more things')
                time.sleep(2)
                HomeScreen.cam_stop(self)
                print('finished all things')
                drops_left -= 1 
                print(drops_left)
                time.sleep(1)
        
                if drops_left <= 0:
                    sm.get_screen('home').label1.flag = '0'
                    break

        if (sm.get_screen('home').label2.flag == '1'):
            #delete data
            print('deleted')
            sm.get_screen('home').label2.flag = '0'

    def cam_record(self):
        global drops_left
        print('starting recording')
        camera.annotate_text = "experiment # {}".format(drops_left)
        camera.start_preview(fullscreen=False, window =(100,50,1000,1000))
        camera.start_recording('/home/pi/Desktop/Drop # {}.h264'.format(drops_left)) 
            
    def cam_stop(self):
        camera.stop_recording()    
    
    pass
class CustomPopup(Popup):
    pass

#kivy screen logic and variable names
sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))


class TestApp(App):

    def build(self):
        
        Clock.schedule_interval(HomeScreen.start_stop, 1)
        return sm


if __name__ == '__main__':
    GUI = TestApp()
    GUI.run()
