### imports ######
import kivy
import time
import sched
import threading
import random
import picamera


#### THIS CODE BASICALLY GETS RID OF ALL FUNCTIONALLITY SO THAT YOU CAN REDESIGN HOW IT LOOKS AND PROCESSES #########
#### ALL FUNCTIONALLITY HAS BEEN TAKEN OUT AND REPLACED WITH PRINT STATEMENTS, THAT IS IN THE DropCode.py FILE ##########

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
Window.fullscreen = 'auto'                     # sets the screen to fill the area marked by top and left in a rectangle
kivy.require('1.11.1')
# Config.set('graphics', 'width', '700')
# Config.set('graphics', 'height', '200')


### Initializing globals ###
main_height = 0
main_interval = 0
main_drops = 0
main_weight = 0
drops_left = 0
exp_time = 0

camera= picamera.PiCamera()
camera.resolution = (1200, 1200)
camera.framerate = 15 #15 is max
camera.brightness = 75
camera.contrast = 0

### flags ###
start = 0
first_drop = True
lifted = False

# timing globals
scheduler = sched.scheduler(time.time, time.sleep)  # keeps track of times for _____


############################### GUI build #########################################################
# Builder is essentialy the .kv file without the extension
#root.manager.current = '' means go to that page
Builder.load_string("""

<CustButton@Button>:
    font_size: 32

#soft tap page
<SoftTap>:
    start:start
    duration:duration

    FloatLayout:                            #in descending order as seen in GUI
        Label:
            text:'Drop Test Device'         # text on the label
            size_hint:(1,.1)                # width and height of label relative to the master wdiget, FloatLayout
            pos_hint:{'top':1}              # sets widget to the top relative to the master widget, FloatLayout

        Button:
            id: duration                    # gives button/label/widget a uniue id that can be referenced using on_press
            text:'Experiment Time: '
            choice: '0'                     #variable the end user types in
            flag: '0'                       #flag to tell what state the button is in
            font_size: 25
            size_hint:(1,.3)
            pos_hint:{'top':.9,'right':1}

            on_press:
                root.manager.get_screen('soft_tap').duration.flag = '1'  #set button_duration flag to 1
                root.manager.current = 'numpad'                          # open up the numpad page


        Label:
            text: 'Time Remaining: '
            font_size: 25
            size_hint:(.669,.1)
            pos_hint:{'top':.5,'left_x':.5}

        Button:
            id:start
            text: 'START'
            font_size:25
            size_hint:(.33,.29)
            pos_hint:{'top':.595,'right': 1}
            flag: '0'

            #if not started, displays start, if started display stop
            #0 means not started
            #1 means started
            on_press:
                if(root.manager.get_screen('soft_tap').start.flag == '0'):root.manager.get_screen('soft_tap').start.flag = '1'; root.manager.get_screen('soft_tap').start.text = 'STOP'
                elif(root.manager.get_screen('soft_tap').start.flag == '1'):root.manager.get_screen('soft_tap').start.flag = '0';root.manager.get_screen('soft_tap').start.text = 'START'

        Button:
            text: 'Force Data: '
            font_size: 25
            size_hint:(.33,.3)
            pos_hint:{'bottom':1}

            on_press: root.manager.current = 'force'                   # go to force page

        Button:
            text: 'Home Page'
            font_size: 25
            size_hint: (.669,.3)
            pos_hint: {'bottom':1 , 'right': 1}

            on_press: root.manager.current = 'home'

#screen when it boots
<HomeScreen>:
    label1: label1
    BoxLayout:
        padding:5
        orientation: "vertical"

        #Hard drop button
        CustButton:
            id: label1
            text:'HARD DROP MODE'

            on_press: root.manager.current = 'menu'

        #soft drop button
        CustButton:
            text: 'SOFT TAP MODE'

            on_press: root.manager.current = 'soft_tap'
# num pad page
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

            size_hint:(1,.3)
            pos_hint:{'top':1}


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
                text:'A/C'#resets calculator
                on_press: entry.text = ''
            CustButton:
                text:'0'
                on_press: entry.text += self.text

            CustButton:
                text:'ENTER'#changes depending on which flag is enabled (which button you clicked to get there)


                on_press:
                    # checks which flag is enabled to tell which label to add the number to
                    if((root.manager.get_screen('menu').label1.flag) == '1'):root.manager.get_screen('menu').label1.text = entry.text + ' cm' ; root.manager.get_screen('menu').label1.choice = entry.text
                    elif((root.manager.get_screen('menu').label2.flag) == '1'):root.manager.get_screen('menu').label2.text = entry.text + ' Second Intervals' ; root.manager.get_screen('menu').label2.choice = entry.text
                    elif((root.manager.get_screen('menu').label3.flag) == '1'):root.manager.get_screen('menu').label3.text = entry.text + ' Drops' ; root.manager.get_screen('menu').label3.choice = entry.text
                    elif((root.manager.get_screen('menu').label4.flag) == '1'):root.manager.get_screen('menu').label4.text = entry.text + ' grams' ; root.manager.get_screen('menu').label4.choice = entry.text
                    elif((root.manager.get_screen('soft_tap').duration.flag)=='1'):root.manager.get_screen('soft_tap').duration.text = entry.text + ' Second Experiment'; root.manager.get_screen('soft_tap').duration.choice = entry.text

                    #clear flags after so you dont add number value to another box
                    root.manager.get_screen('menu').label1.flag = '0'
                    root.manager.get_screen('menu').label2.flag = '0'
                    root.manager.get_screen('menu').label3.flag = '0'
                    root.manager.get_screen('menu').label4.flag = '0'

                    #_____________
                    if((root.manager.get_screen('soft_tap').duration.flag)=='1'): root.manager.current = 'soft_tap'
                    elif((root.manager.get_screen('soft_tap').duration.flag)=='0'): root.manager.current = 'menu'

                    root.manager.get_screen('soft_tap').duration.flag = '0' #to distinguish between soft and hard modes
                    entry.text = ''

<MenuScreen>:                               #hard drop page
    label1: label1                          #height label
    label2: label2                          #interval label
    label3: label3                          #Drop number
    label4: label4                          #Weight Label
    label5: label5                          #Start Label
    drop:   drop

    FloatLayout:                            #in descending order as seen in GUI
        Label:
            text:'Drop Test Machine'
            size_hint:(1,.1)
            pos_hint:{'top':1}

        Button:
            id: label1

            text:'Height: '
            choice:'0'
            flag: '0'

            font_size: 25
            size_hint:(.33,.3)
            pos_hint:{'top':.9}


            on_press:
                root.manager.get_screen('menu').label1.flag = '1'           #send to numpad
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

        #Label:
            #text: 'Time Until Drop: '
            #font_size: 15
            #size_hint:(.33,.1)
            #pos_hint:{'top':.5,'center_x':.5}

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
            choice: '0'
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

#force data screen
<ForceData>:
    forcelabel:forcelabel

    FloatLayout:

        Label:
            size_hint:(1,.8)
            pos_hint:{'top':1,'left_x':.5}
            #Color:
             #   rgb: 1, 1, 0

            id:forcelabel
            text: ''
            flag: '0'

        Button:
            size_hint:(1,.1)
            pos_hint:{'bottom':1}

            text:'Return to Menu'
            on_press: root.manager.current = 'home'

        Button:
            size_hint:(1,.1)
            pos_hint:{'top':.2,'center_x':.5}

            text: 'Clear ALL Data'
            on_press:
                root.manager.get_screen('force').forcelabel.text = ''
                root.manager.get_screen('force').forcelabel.flag = '1'

""")

############################################################
class NumScreen(Screen):
    pass


class ForceData(Screen):
    pass

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
        global main_weight
        global drops_left
        global start

        # sets height, interval, and drops to what the user has chosen via the numpad
        main_height = int(sm.get_screen('menu').label1.choice)
        main_interval = int(sm.get_screen('menu').label2.choice)
        main_drops = int(sm.get_screen('menu').label3.choice)
        main_weight = int(sm.get_screen('menu').label4.choice)


        # uses start flag to tell when to start and set the flag to 1
        # update dislpay values
        if(start == 0):  # uses start flag to grab drops left for countdown
            drops_left = main_drops
            start = 1
        # Call the start of the lifting routine if start has been pressed

        # update display values, give user feedback
        sm.get_screen('menu').drop.text = str(drops_left) + ' Drops Remaining'

        print(main_height)
        print(main_interval)
        print(main_drops)

        # GLOBAL UPDATE AND MANAGE DROPS
    def start_stop(self):  # periodicaly                       (DO I NEED THIS )

        global drops_left
        global first_drop

        if (sm.get_screen('force').forcelabel.flag == '1'):
            sm.get_screen('force').forcelabel.flag = '0'
            print("cleared log file")
            with open("Sensor_Log.txt", "r+") as DeleteValues:
                DeleteValues.truncate(0)

        if(sm.get_screen('soft_tap').start.flag == '1'):
            print("running soft drops")
            Events.cam_record(self)
            Events.Read_Sensor_Soft(self)
            Events.cam_stop()
            #throw to another function that handles soft drops
            #root.manager.get_screen('soft_tap').duration.choice




        if((sm.get_screen('menu').label5.flag == '1') and (first_drop == True)):

            MenuScreen.global_update(self)
            Events.manage_drops(self)

        elif(sm.get_screen('menu').label5.flag == '0'):
            pass  # proably clear all or somthing like that here

class Events(Screen):# EVENTSFOR DROPS (lower, raise, read sensor)

    def cam_record(self):
        global drops_left
        print('starting recording')
        camera.annotate_text = "experiment # {}".format(drops_left)
        camera.start_preview(fullscreen=False, window =(100,50,1000,1000))
        camera.start_recording('/home/pi/Desktop/Drop # {}.h264'.format(drops_left)) 
            
    def cam_stop(self):
        camera.stop_recording()  

    def manage_drops(self):  # CONTROL
        # is this the first drop?(yes)-> lift and drop
        #                       (NO )-> schedule disengage,  engage->lift (idle)
        global drops_left
        global first_drop
        global main_interval
        global start
        ##################################### MAIN ACTION LOOP ##############################





        if(first_drop): #& IN HARD DROP OR SOFT DROP (differentiiate how they work)
            first_drop = False  # no longer first drop
            print("First Drop")
            Events.toggle_hold_out(self)
            Events.lift(self)
            Events.toggle_hold_in(self)
            Events.Read_Sensor_Hard(self)
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
            Events.cam_record(self)
            Events.toggle_hold_out(self)
            Events.lift(self)
            Events.toggle_hold_in(self)
            Events.Read_Sensor_Hard(self)
            Events.lower(self)
            Events.cam_stop(self)


            # schedule next drop
            Clock.schedule_once(Events.manage_drops, main_interval)
            pass

        elif(drops_left == 0):  # reset to before start was pressed
            print("Drops Complete")
            sm.get_screen('menu').label5.flag = '0'
            sm.get_screen('menu').label5.text = 'Done / Start'
            start = 0
            first_drop = True

            #make x number of labels for table
                #drop #chpice = create labels
            #SEND TO THE TABLE
            #CLEAR THE FILE
            with open("Sensor_Log.txt", "r+") as UploadValues:

                f = UploadValues.readlines()#SEND VALUES TO THE TABLE
                count = 0
                #data_label = Label(text = 'new data label')

                for line in f:
                    count +=1
                    #TRY AND RE WRITE WITH EAITHER A FULL TABLE OR BY ADDING LABELS

                    sm.get_screen('force').forcelabel.text += str(line) + "\n"
                    print("adding line {} to forcelabel".format(count))
                    #print("Drop {}: {}".format(count,line.strip())) #########################
                    #^^replace that with send to table or something
                    #sm.add_widget(ForceData(name='force'))
                count = 0
                #UploadValues.truncate(0) #clearing file

    def Read_Sensor_Hard(self):
        DURATION = 5 # IN Seconds
        Time_Running = 0
        List_Of_Values = []
        TimeArray = []

        print("reading")

        while True:
            #print("Force = {} PSI, TimeStamp = {} seconds".format(Sensor_Force_Value,Time_Running))
            List_Of_Values.append(random.randint(0,700)) ## sensoir value
            TimeArray.append(Time_Running)
            time.sleep(.025) #<-- increments at rates of .025 seconds, could do something with timestamp and frameindex
            Time_Running = round(Time_Running +.025, 3)

            if (Time_Running > DURATION): # <-- this will be replaced with (if motors still running/if start still pressed) but testing for now

                print("Highest Force = {}".format(max(List_Of_Values)))
                #sm.get_screen('force').forcelabel.text = str(max(List_Of_Values)) #<--sens one value to label

                print("writing value to log")
                with open("Sensor_Log.txt", "a") as WriteValues:
                    WriteValues.write(("Drop # = {} | Force Value = {} psi| Height = {} cm| Weight = {} grams| TimeStamp = {} seconds| Interval = {} seconds\n").format((main_drops - drops_left), str(max(List_Of_Values )), main_height, main_weight, TimeArray[List_Of_Values.index(max(List_Of_Values))], main_interval))
                    #values written to txt file, each new line = new drop
                List_Of_Values.clear()
                TimeArray.clear()
                print("wrote value to log")
                break

    def Read_Sensor_Soft(self):

        DURATION = int(sm.get_screen('soft_tap').duration.choice) # IN Seconds
        Time_Running = 0
        List_Of_Values = []
        TimeArray = []
        print('Duration = {} seconds'.format(DURATION))
        print("reading")

        while True:
            #print("Force = {} PSI, TimeStamp = {} seconds".format(Sensor_Force_Value,Time_Running))
            List_Of_Values.append(random.randint(0,700)) ## sensoir value
            TimeArray.append(Time_Running)
            for value in List_Of_Values:
                if value < 600:
                    del TimeArray[List_Of_Values.index(value)]
                    #TimeArray.remove([List_Of_Values.index(value)])
                    List_Of_Values.remove(value)
            time.sleep(.025) #<-- increments at rates of .025 seconds, could do something with timestamp and frameindex
            Time_Running = round(Time_Running +.025, 3)

            if (Time_Running > DURATION): # <-- this will be replaced with (if motors still running/if start still pressed) but testing for now

                #sm.get_screen('force').forcelabel.text = str(max(List_Of_Values)) #<--sens one value to label
                    #TimeArray[List_Of_Values.index(value)
                print("writing value to log")
                with open("Sensor_Log.txt", "a") as WriteValues:
                    for value in List_Of_Values:
                        WriteValues.write("Force Value = {} psi| TimeStamp = {} seconds\n".format(str(value), str(TimeArray[List_Of_Values.index(value)])))
                    #values written to txt file, each new line = new drop

                with open("Sensor_Log.txt", "r+") as UploadValues:
                    f = UploadValues.readlines()#SEND VALUES TO THE TABLE
                    count = 0
                    for line in f:
                        count +=1
                        sm.get_screen('force').forcelabel.text += str(line) + "\n"
                        print("adding line {} to forcelabel".format(count))
                    count = 0

                List_Of_Values.clear()
                TimeArray.clear()
                print("wrote value to log")
                sm.get_screen('soft_tap').start.flag = '0'
                sm.get_screen('soft_tap').start.text = 'Done/Start'
                break

    def toggle_hold_out(self):  # Hold
        print('holding out')

    def toggle_hold_in(self):
        print("holding in")

        pass


        pass#needed? or put in toggle hold out

    def lift(self):  # LIFT
        global main_height  # conversion value here (i just put the conversion on the functions lift and lower 1 foot = 1000 steps
        print('lifting ' + str(main_height) + ' CM')
        #check release and double
        pass

    def lower(self):  # LOWER
        global main_height  # conversion value here, possibly but i just put them in the lift and lower calls
        print('lowering ' + str(main_height) + ' CM')
        pass

    pass

#kivy screen logic and variable names
sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(SoftTap(name='soft_tap'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(NumScreen(name='numpad'))
sm.add_widget(ForceData(name='force'))

sm.add_widget(Events(name='event'))  # this may be a dont care (events)



class TestApp(App):

    def build(self):
        # drives update mechanic off of menu start_stop

        Clock.schedule_interval(MenuScreen.start_stop, 1)
        return sm


if __name__ == '__main__':
    GUI = TestApp()
    GUI.run()
