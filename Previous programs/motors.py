import kivy
kivy.require('1.11.1') 
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

from kivy.config import Config
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left' , 0)
Config.set('graphics', 'top', 0)
from kivy.core.window import Window
Window.fullscreen = 'auto'
# % builder is essentialy the .kv file without a .kv file
# GLOBALS


Builder.load_string("""

<CustButton@Button>:
    font_size: 32

<SoftTap>:
    
    FloatLayout:                            #in decending order as seen in GUI
        Label:
            text:'soft taps page' 
            font_size:50
            size_hint:(1,.1)                #%(width, hight)
            pos_hint:{'top':1}              #%exact top
        CustButton:
            text: 'return'
            size_hint: (1,.2)
            pos_hint:{'bottom':1}
            on_press:
                root.manager.current= 'home'


<HomeScreen>:

    BoxLayout:
        padding:5
        orientation: "vertical"
        CustButton:
            text:'HARD DROP MODE'
            on_press: root.manager.current = 'menu'

        CustButton:
            text: 'SOFT TAP MODE'
            on_press: root.manager.current = 'soft_tap'

<NumScreen>:

    BoxLayout:
        padding:5
        spacing:5
        id: update_value
        display: entry
       
        
        orientation:"vertical"
        TextInput:
            id: entry
            font_size: 40
            multiline: False

            size_hint:(1,.3)                #%(width, hight)
            pos_hint:{'top':1}              #%exact top

        
        GridLayout:
            id:state

            padding:5
            spacing:5
            cols:3
            CustButton:
                text:'7'
                on_press: entry.text += self.text 
            CustButton:
                text:'8'
                on_press: entry.text += self.text
            CustButton:
                text:'9'
                on_press: entry.text += self.text
            CustButton:
                text:'4'
                on_press: entry.text += self.text
            CustButton:
                text:'5'
                on_press: entry.text += self.text
            CustButton:
                text:'6'
                on_press: entry.text += self.text
            CustButton:
                text:'1'
                on_press: entry.text += self.text
            CustButton:
                text:'2'
                on_press: entry.text += self.text
            CustButton:
                text:'3'
                on_press: entry.text += self.text
            CustButton:
                text:'A/C'#######################################different
                on_press: entry.text = ''
            CustButton:
                text:'0'
                on_press: entry.text += self.text
            CustButton:
                text:'ENTER'######################################different

               
                on_press: 
                    if((root.manager.get_screen('menu').label1.flag) == '1'):root.manager.get_screen('menu').label1.text = entry.text + ' cm'  #flag check
                    elif((root.manager.get_screen('menu').label2.flag) == '1'):root.manager.get_screen('menu').label2.text = entry.text + ' MIN Intervals' 
                    elif((root.manager.get_screen('menu').label3.flag) == '1'):root.manager.get_screen('menu').label3.text = entry.text + ' Drops' 
                    elif((root.manager.get_screen('menu').label4.flag) == '1'):root.manager.get_screen('menu').label4.text = entry.text + ' grams' 

                    root.manager.get_screen('menu').label1.flag = '0'  #flag clear 
                    root.manager.get_screen('menu').label2.flag = '0'
                    root.manager.get_screen('menu').label3.flag = '0'
                    root.manager.get_screen('menu').label4.flag = '0'
                    root.manager.current = 'menu'
                    entry.text = ''
                                
<MenuScreen>:
    label1: label1
    label2: label2
    label3: label3    
    label4: label4
    
    FloatLayout:                            #in decending order as seen in GUI
        Label:
            text:'Project Lab 4 Christian and Joseph' 
            size_hint:(1,.1)                #%(width, hight)
            pos_hint:{'top':1}              #%exact top
        Button:
            id: label1

            text:'Height: '

            flag: '0'

            font_size: 25
            size_hint:(.33,.3)
            pos_hint:{'top':.9}             #10% from top
            on_press:  
                root.manager.get_screen('menu').label1.flag = '1'
                root.manager.current = 'numpad'
                

        Button:
            id: label2
            text:'INTERVAL: '

            flag: '0'

            font_size: 25
            size_hint:(.33,.3)
            pos_hint:{'top':.9,'right':1}

            on_press: 
                root.manager.get_screen('menu').label2.flag = '1'
                root.manager.current = 'numpad'

        Button:
            id:label3
            text:'Drops#: '

            flag: '0'

            font_size: 25
            size_hint:(.33,.3)
            pos_hint:{'top':.9,'center_x':.5}

            on_press: 
                root.manager.get_screen('menu').label3.flag = '1'
                root.manager.current = 'numpad'

        Label:
            text: 'Drops Remaining: '
            font_size: 15
            size_hint:(.5,.1)
            pos_hint:{'top':.5}

        Label:
            text: 'Time Till Drop: '
            font_size: 15
            size_hint:(.5,.1)
            pos_hint:{'top':.5,'right':1}

        Button:
            text: 'Force Data: '
            font_size: 25
            size_hint:(.33,.3)
            pos_hint:{'bottom':1}

            on_press: root.manager.current = 'force'
        
        Button: 
            id:label4
            text: 'Current Weight: ' 
            font_size: 25
            size_hint: (.33,.3)
            pos_hint: {'bottom': 1, 'center_x': .5}
            flag: '0'
            on_press: 
                root.manager.get_screen('menu').label4.flag = '1'
                root.manager.current = 'numpad'

        Button:
            text: 'Home Page'
            font_size: 25
            size_hint: (.33,.3)
            pos_hint: {'bottom':1 , 'right': 1}
            on_press: root.manager.current = 'home'
            
<ForceData>:
    BoxLayout:
        orientation:'vertical'
        Label:
            text: 'FORCE DATA HERE!!'
        Button: 
            text:'Return to Menu'
            on_press: root.manager.current = 'menu'

""")


class SoftTap(Screen):
    pass


class HomeScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


class NumScreen(Screen):
    pass


class ForceData(Screen):
    pass


sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(SoftTap(name='soft_tap'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(NumScreen(name='numpad'))
sm.add_widget(ForceData(name='force'))


class TestApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    GUI = TestApp()
    s = sm.get_screen('menu').label1.text  # yataaaaaaaa desu neeeeeeee
    print(s)
    print(5)

    GUI.run()

    # TestApp().run()


