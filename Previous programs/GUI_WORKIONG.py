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
import kivy
import time
import sched
import threading

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper



from kivy.config import Config
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left' , 0)
Config.set('graphics', 'top', 0)
from kivy.core.window import Window
Window.fullscreen = 'auto'
from kivy.config import Config

 
 
kivy.require('1.11.1')
 
# Config.set('graphics', 'width', '700')
# Config.set('graphics', 'height', '200')
# GLOBALS
main_height = 0
main_interval = 0
main_drops = 0
drops_left = 0
exp_time = 0
soft_tap_done = False

# flags
start = 0
first_drop = True
lifted = False
# % builder is essentialy the .kv file without a .kv file
# timeing globals
scheduler = sched.scheduler(time.time, time.sleep)  # class
 
#######

 
##########################################################
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
    label1: label1
    BoxLayout:
        padding:5
        orientation: "vertical"
        CustButton:
            id: label1
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
                    if((root.manager.get_screen('menu').label1.flag) == '1'):root.manager.get_screen('menu').label1.text = entry.text + ' cm' ; root.manager.get_screen('menu').label1.choice = entry.text
                    elif((root.manager.get_screen('menu').label2.flag) == '1'):root.manager.get_screen('menu').label2.text = entry.text + ' MIN Intervals' ; root.manager.get_screen('menu').label2.choice = entry.text
                    elif((root.manager.get_screen('menu').label3.flag) == '1'):root.manager.get_screen('menu').label3.text = entry.text + ' Drops' ; root.manager.get_screen('menu').label3.choice = entry.text
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
    label5: label5
    drop:   drop
 
    FloatLayout:                            #in decending order as seen in GUI
        Label:
            text:'Project Lab 4 Christian and Joseph'
            size_hint:(1,.1)                #%(width, hight)
            pos_hint:{'top':1}              #%exact top
        Button:
            id: label1
 
            text:'Height: '
            choice:'0'
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
            choice: '0'
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
            choice: '0'
            flag: '0'
 
            font_size: 25
            size_hint:(.33,.3)
            pos_hint:{'top':.9,'center_x':.5}
 
            on_press:
                root.manager.get_screen('menu').label3.flag = '1'
                root.manager.current = 'numpad'
 
        Label:
            id:drop
            text: 'Drops Remaining: '
            font_size: 20
            size_hint:(.33,.1)
            pos_hint:{'top':.5}
 
        Label:
            text: 'Time Till Drop: '
            font_size: 15
            size_hint:(.33,.1)
            pos_hint:{'top':.5,'center_x':.5}
 
        Button:
            id:label5
            text: 'START'
            font_size:25
            size_hint:(.33,.29)
            pos_hint:{'top':.595,'right': 1}
            flag: '0'
            on_press:
                if(root.manager.get_screen('menu').label5.flag == '0'):root.manager.get_screen('menu').label5.flag = '1'; root.manager.get_screen('menu').label5.text = 'STOP'
                elif(root.manager.get_screen('menu').label5.flag == '1'):root.manager.get_screen('menu').label5.flag = '0';root.manager.get_screen('menu').label5.text = 'START'
 
 
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
############################################################
 
 
class SoftTap(Screen):
    pass
 
 
class HomeScreen(Screen):
    pass
 
 
class MenuScreen(Screen):
    # updates user input values
 
    def global_update(self):
        global main_height
        global main_interval
        global main_drops
        global drops_left
        global start
 
        main_height = int(sm.get_screen('menu').label1.choice)
        main_interval = int(sm.get_screen('menu').label2.choice)
        main_drops = int(sm.get_screen('menu').label3.choice)
 
        # update dislpay values
        if(start == 0):  # uses start flag to grab drops left for countdown
            drops_left = main_drops
            start = 1
            # Call the start of the lifting routine if start has been pressed
 
        # update dislpay values
        sm.get_screen('menu').drop.text = str(drops_left) + ' Drops Remaining'
 
        print(main_height)
        print(main_interval)
        print(main_drops)
 
    def start_stop(self):  # periodicaly                       (DO I NEED THIS )
 
        global drops_left
        global first_drop
 
        if((sm.get_screen('menu').label5.flag == '1') and (first_drop == True)):
 
            MenuScreen.global_update(self)
            Events.manage_drops(self)
 
        elif(sm.get_screen('menu').label5.flag == '0'):
            pass  # proably clear all or somthing like that here
 
 
class NumScreen(Screen):
    pass
 
 
class ForceData(Screen):
    pass
 
 
class Events(Screen):
 
    def manage_drops(self):  # CONTROL
        # is this the first drop?(yes)-> lift and drop
        #                       (NO )-> schedual disengage,  engage->lift (idel)
        global drops_left
        global first_drop
        global main_interval
        global start
 
        if(first_drop):
            first_drop = False  # no longer first drop
 
            Events.toggle_hold_out(self)
            Events.lift(self)
            Events.toggle_hold_in(self)
            Events.lower(self)
 
            # drop update
            drops_left = drops_left-1
            sm.get_screen('menu').drop.text = str(
                drops_left) + ' Drops Remaining'
 
            print('first drop done\n')
            Clock.schedule_once(Events.manage_drops, main_interval)
            pass
        elif((first_drop == False) and (drops_left > 0)):  # drops after first
            print('drops left ' + str(drops_left))
            drops_left = drops_left-1
            sm.get_screen('menu').drop.text = str(
                drops_left) + ' Drops Remaining'
            
            Events.toggle_hold_out(self) #the drop calls 
            Events.lift(self)
            Events.toggle_hold_in(self)
            Events.lower(self)
            
            
            # schedual next drop
            Clock.schedule_once(Events.manage_drops, main_interval)
            pass
        elif(drops_left == 0):  # reset to before start was pressed 
            
            #Events.Test(self) #was testing at the end of the countdown 
            
            sm.get_screen('menu').label5.flag = '0'
            sm.get_screen('menu').label5.text = 'Done / Start'
            start = 0
            first_drop = True
 
    def toggle_hold_out(self):  # Hold
        print('toggling hold')
        print('\n')
        
        kit.motor1.throttle = -1.0     #engage outward
        time.sleep(1.5)
        kit.motor1.throttle = 0       #this is current related
    
    def toggle_hold_in(self):
        kit.motor1.throttle = 1.0     #engage inward
        time.sleep(1.5)
        kit.motor1.throttle = 0
        
        pass
        
        
        pass
 
    def lift(self):  # LIFT
        global main_height  # conversion value here (i just put the conversion on the functions lift and lower 1 foot = 1000 steps
        print('lifting ' + str(main_height))
        
        for i in range(main_height*394):
            kit1.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)     #lift
        kit1.stepper1.release()  #so motor current dosnt spike
        
        pass
 
    def lower(self):  # LOWER
        global main_height  # conversion value here, possibly but i just put them in the lift and lower calls 
        print('lowering ' + str(main_height))
        
        for i in range(main_height*394): #i put this a lil higher then lift to ensure absolute zero because bump sensor didnt come in 
            kit1.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)     #lower
        kit1.stepper1.release()    

        pass
    
    
    def Test(self):# this is a test case you can call it lifts and lowers once its a good look at whats happening sequentialy
        global main_height
        
        #kit.motor1.throttle = -1.0     #engage
        #time.sleep(1.5)
        
        #for i in range(main_height*394):
            #kit1.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)     #lift
        #kit1.stepper1.release()  
            
        #kit.motor1.throttle = 1.0    #retract
        #time.sleep(1.5)
        #kit.motor1.throttle = 0
        ################
        
    
        for i in range(main_height*400):
            kit1.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)     #lower
        kit1.stepper1.release()    
      
        pass
    pass
 
kit = MotorKit()
kit1= MotorKit(address=0x61)

sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(SoftTap(name='soft_tap'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(NumScreen(name='numpad'))
sm.add_widget(ForceData(name='force'))
sm.add_widget(Events(name='event'))  # this may be a dont care (events)
 

 
class TestApp(App):
 
    def build(self):
        # drives update michanic off of menu start_stop
        
        Clock.schedule_interval(MenuScreen.start_stop, 1)
        return sm
 
 
if __name__ == '__main__':
    GUI = TestApp()
    # s = sm.get_screen('menu').label1.text
    GUI.run()
