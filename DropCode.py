### imports ###
import kivy
import time
import sched
import threading
import smbus
import picamera

### Kivy Imports ###
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

### Motor Imports ###
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

### Configuration of the Main Window ###
from kivy.config import Config
from kivy.core.window import Window
Config.set('graphics', 'position', 'custom')    
Config.set('graphics', 'left' , 0)              
Config.set('graphics', 'top', 0)                
Window.fullscreen = 'auto'                      
kivy.require('1.11.1')

### Initializing Globals ###
#drop globals #
main_height = 0
main_interval = 0
main_drops = 0
main_weight = 0
drops_left = 0
#Tap Globals#
Tap_Interval = 0
Tap_Force = 0
Tap_Ammount = 0
Taps_Left = 0
# sensor globals #
Time_Running = 0
List_Of_Values = []
TimeArray = []
Sensor_Duration = 5
bus = smbus.SMBus()
Sensor_Address = 0x04
Sensor_Time_Interval = .025

### flags ###
start = 0
first_drop = True
first_tap = True

### Camera Setup ###
camera= picamera.PiCamera()
camera.resolution = (1280, 960)
camera.framerate = 15 # 0-15
camera.brightness = 60
camera.contrast = 60
#camera.start_preview(fullscreen=False, window =(100,50,1000,1000))
# ^^ x,y,width,height, (w/h = ratio)

### Clock Timer ###
# sets interval for start_stop (flag-check loop)
# schedules drops for Drop Mode
scheduler = sched.scheduler(time.time, time.sleep)



############################### GUI Build #########################################################
# Builder is essentialy the .kv file without the extension

Builder.load_string("""

# Main App Window
<CustButton@Button>:
    font_size: 32

#Boot Screen
<HomeScreen>
    FloatLayout:
        
        Label:
            text:'Automated TBI for C. elagans'
            font_size: 60
            size_hint : (1,.25)
            pos_hint : {'top':.95,'center_x':.5}

        Button:
            text:'Drop Mode'
            size_hint : (.5,.15)
            pos_hint : {'top':.75,'center_x':.5}

            on_press:
                root.manager.current = 'drop_screen'
                
        Button:
            text: 'Tap Mode'
            size_hint : (.5,.15)
            pos_hint : {'top':.55,'center_x':.5}
            
            on_press:
                root.manager.current = 'tap_screen'
          
        Button:
            
            text: 'Data'
            size_hint : (.5,.15)
            pos_hint : {'top':.35,'center_x':.5}
            
            on_press:
                root.manager.current = 'data'
            
#Tap Mode Screen
<TapScreen>:
    start:start
    interval:interval
    ammount:ammount
    force:force
    tapback:tapback
    taptimer:taptimer
    tapleft:tapleft
    
    FloatLayout:
    
        Label:
            text:'Tap Mode' 
            font_size: 40
            size_hint:(1,.2)
            pos_hint: {'center_x':.5,'top':1}

        Button:
            id: interval
            choice: '0'                     
            flag: '0'
            
            text:'Tap Interval:'
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.9,'top':.6}
                                   
            on_press:
                root.manager.get_screen('tap_screen').interval.flag = '1' 
                root.manager.current = 'numpad'
                
        Button:
            id: ammount
            choice:'0'
            flag:'0'
            
            text:'Tap Ammount:'
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.65,'top':.6}
            
            on_press:
                root.manager.get_screen('tap_screen').ammount.flag = '1' 
                root.manager.current = 'numpad'
            
        Button:
            id:force
            choice:'0'
            flag:'0'
            
            text:'Force Threshold:'
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.9,'top':.8}
            
            on_press:
                root.manager.get_screen('tap_screen').force.flag = '1' 
                root.manager.current = 'numpad'

        Label:
            id: tapleft
            
            text: 'Taps Remaining: '
            font_size: 25
            size_hint:(.669,.1)
            pos_hint:{'center_x':.35,'top':.2}
            
        Label:
            id:taptimer
            
            text: 'Next Tap: '
            font_size: 25
            size_hint:(.669,.1)
            pos_hint:{'center_x':.15,'top':.2}
            
        Button:
            text: 'placeholder for camera preview'
            size_hint:(.5,.6)
            pos_hint:{'center_x':.25,'top':.8}

        Button:
            id:start
            flag: '0'
            
            text: 'START'
            font_size:25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.65,'top': .8}
            
            on_press:
                if(root.manager.get_screen('tap_screen').start.flag == '0'):root.manager.get_screen('tap_screen').start.flag = '1'; root.manager.get_screen('tap_screen').start.text = 'STOP'
                elif(root.manager.get_screen('tap_screen').start.flag == '1'):root.manager.get_screen('tap_screen').start.flag = '0';root.manager.get_screen('tap_screen').start.text = 'START'

        Button:
            id: tapback
            flag:'0'
            
            text: 'Data'
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.65,'top':.35}

            on_press:
                root.manager.current = 'data'
                root.manager.get_screen('tap_screen').tapback.flag = '1'

        Button:
            text: 'Home'
            font_size: 25
            size_hint: (.2,.15)
            pos_hint:{'center_x':.9,'top':.35}

            on_press:
                root.manager.current = 'home'
                
#Drop Screen
<DropScreen>:
    label1: label1                          #height
    label2: label2                          #interval
    label3: label3                          #Drops
    label4: label4                          #Weight
    label5: label5                          #Start
    drop:   drop
    dropback:dropback
    
    FloatLayout:
        Label:
            text:'Drop Mode'
            font_size : 40
            size_hint:(1,.2)
            pos_hint: {'center_x':.5,'top':1} 

        Button:
            id: label1
            choice:'0'
            flag: '0'

            text:'Height: '
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.65,'top':.6}

            on_press:
                root.manager.get_screen('drop_screen').label1.flag = '1'
                root.manager.current = 'numpad'

        Button:
            id: label2
            choice: '0'
            flag: '0'

            text:'Interval: '
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.9,'top':.4}

            on_press:
                root.manager.get_screen('drop_screen').label2.flag = '1'
                root.manager.current = 'numpad'

        Button:
            id:label3
            choice: '0'
            flag: '0'

            text:'Drops: '
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.65,'top':.4}

            on_press:
                root.manager.get_screen('drop_screen').label3.flag = '1'
                root.manager.current = 'numpad'

        Label:
            id:drop
            
            text: 'Drops Remaining: '
            font_size: 20
            size_hint:(.2,.15)
            pos_hint:{'center_x':.1,'top':.2}

        Label:
            text: 'Next Drop: '
            font_size: 20
            size_hint:(.2,.15)
            pos_hint:{'center_x':.3,'top':.2}

        Button:
            id:label5
            flag: '0'
            
            text: 'START'
            font_size:25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.775,'top':.8}
            
            on_press:
                if(root.manager.get_screen('drop_screen').label5.flag == '0'):root.manager.get_screen('drop_screen').label5.flag = '1'; root.manager.get_screen('drop_screen').label5.text = 'STOP'
                elif(root.manager.get_screen('drop_screen').label5.flag == '1'):root.manager.get_screen('drop_screen').label5.flag = '0';root.manager.get_screen('drop_screen').label5.text = 'START'

        Button:
            id: dropback
            flag: '0'
            
            text: 'Data '
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.65,'top':.2}

            on_press:
                root.manager.current = 'data'
                root.manager.get_screen('drop_screen').dropback.flag = '1'

        Button:
            id:label4
            choice: '0'
            flag: '0'
            
            text: 'Weight: '
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.9,'top':.6}
            
            on_press:
                root.manager.get_screen('drop_screen').label4.flag = '1'
                root.manager.current = 'numpad'

        Button:
            text: 'Home'
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.9,'top':.2}
            
            on_press:
                root.manager.current = 'home'
        
        Button:
            text: 'placeholder for camera preview'
            size_hint:(.5,.6)
            pos_hint:{'center_x':.25,'top':.8}
            
   
   
# NumPad (User Entry) Page
<NumScreen>:

    BoxLayout:
        id: update_value
        
        padding:5
        spacing:5
        display: entry
        orientation:"vertical"
        
        TextInput:
            id: entry
            
            font_size: 40
            multiline: False
            size_hint:(1,.3)
            pos_hint:{'top':1}

        # Dont need position or sizing as Grid Layout maps it #
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
                text:'A/C'
                on_press: entry.text = ''
            CustButton:
                text:'0'
                on_press: entry.text += self.text

            CustButton:
                text:'ENTER'#changes depending on which flag is enabled (which button you clicked to get there)


                on_press:
                    # checks which flag is enabled to tell which label to add the number to
                    
                    #Drop Mode Height Button
                    if((root.manager.get_screen('drop_screen').label1.flag) == '1'):root.manager.get_screen('drop_screen').label1.text = entry.text + ' cm' ; root.manager.get_screen('drop_screen').label1.choice = entry.text
                    
                    #Drop Mode Interval Button
                    elif((root.manager.get_screen('drop_screen').label2.flag) == '1'):root.manager.get_screen('drop_screen').label2.text = entry.text + ' second intervals' ; root.manager.get_screen('drop_screen').label2.choice = entry.text
                    
                    # Drop Mode Drop Number Button
                    elif((root.manager.get_screen('drop_screen').label3.flag) == '1'):root.manager.get_screen('drop_screen').label3.text = entry.text + ' drops' ; root.manager.get_screen('drop_screen').label3.choice = entry.text
                    
                    # Drop Mode Weight Button
                    elif((root.manager.get_screen('drop_screen').label4.flag) == '1'):root.manager.get_screen('drop_screen').label4.text = entry.text + ' grams' ; root.manager.get_screen('drop_screen').label4.choice = entry.text
                    
                    #Tap Mode interval Button
                    elif((root.manager.get_screen('tap_screen').interval.flag)=='1'):root.manager.get_screen('tap_screen').interval.text = entry.text + ' Second Intervals'; root.manager.get_screen('tap_screen').interval.choice = entry.text
                    
                    # Tap Mode Tap Ammount Button
                    elif((root.manager.get_screen('tap_screen').ammount.flag)=='1'):root.manager.get_screen('tap_screen').ammount.text = entry.text + ' Taps'; root.manager.get_screen('tap_screen').ammount.choice = entry.text
                   
                    # Tap Mode Threshold Button
                    elif((root.manager.get_screen('tap_screen').force.flag)=='1'):root.manager.get_screen('tap_screen').force.text = entry.text + ' PSI Threshold'; root.manager.get_screen('tap_screen').force.choice = entry.text
                   
                    # getting to last page
                    if((root.manager.get_screen('tap_screen').interval.flag)=='1'): root.manager.current = 'tap_screen'
                    elif((root.manager.get_screen('tap_screen').force.flag)=='1'): root.manager.current = 'tap_screen'
                    elif((root.manager.get_screen('tap_screen').ammount.flag)=='1'): root.manager.current = 'tap_screen'
                    else: root.manager.current = 'drop_screen'
                    
                    #clear flags after so you dont add number value to another box
                    root.manager.get_screen('drop_screen').label1.flag = '0'
                    root.manager.get_screen('drop_screen').label2.flag = '0'
                    root.manager.get_screen('drop_screen').label3.flag = '0'
                    root.manager.get_screen('drop_screen').label4.flag = '0'
                    root.manager.get_screen('tap_screen').interval.flag = '0'
                    root.manager.get_screen('tap_screen').force.flag = '0'
                    root.manager.get_screen('tap_screen').ammount.flag = '0'

                    #instantiate the variable for user input
                    entry.text = ''

#Data Screen
<DataScreen>:
    datalabel:datalabel

    FloatLayout:

        Label:
            id:datalabel
            flag: '0'
            
            text: ''
            size_hint:(1,.6)
            pos_hint:{'top':1,'left_x':.5}

        Button:
            text:'Return to Menu'
            size_hint:(.5,.1)
            pos_hint:{'center_x':.75,"top":.1}
            
            on_press:
                root.manager.current = 'home'
                root.manager.get_screen('drop_screen').dropback.flag == '0'
                root.manager.get_screen('tap_screen').tapback.flag == '0'

        Button:
            text: 'Clear ALL Data'
            size_hint:(.5,.1)
            pos_hint:{'top':.2,'center_x':.25}
            
            on_press:
                root.manager.get_screen('data').datalabel.text = ''
                root.manager.get_screen('data').datalabel.flag = '1'
                
        Button:
            text: 'Export Data'
            size_hint:(.5,.1)
            pos_hint:{'top':.2,'center_x':.75}
            
        Button:
            text: 'Previous Page'
            size_hint:(.5,.1)
            pos_hint:{'top':.1,'center_x':.25}
            
            on_press:
                if(root.manager.get_screen('drop_screen').dropback.flag == '1'):root.manager.current = 'drop_screen'
                elif(root.manager.get_screen('tap_screen').tapback.flag == '1'):root.manager.current = 'tap_screen'
                else: root.manager.current = 'home'
                root.manager.get_screen('drop_screen').dropback.flag = '0'
                root.manager.get_screen('tap_screen').tapback.flag = '0'
                
            
""")
############################ Back End Functions and Scheduling ################################

class NumScreen(Screen):
    pass


class DataScreen(Screen):
    pass

class TapScreen(Screen):
    pass


class HomeScreen(Screen):
    pass

class DropScreen(Screen):
    
    # updates input values for Tap Mode
    def Tap_global_update(self):
        global Tap_Interval
        global Tap_Force
        global Tap_Ammount 
        global Taps_Left 
        
        Tap_Interval = int(sm.get_screen('tap_screen').interval.choice)
        Tap_Force = int(sm.get_screen('tap_screen').force.choice)
        Tap_Ammount = int(sm.get_screen('tap_screen').ammount.choice)
        
        Taps_Left = Tap_Ammount
        sm.get_screen('tap_screen').tapleft.text = str(Taps_Left) + ' Drops Remaining'
        
        print(Tap_Interval)
        print(Tap_Ammount)
        print(Tap_Force)
        
        # ADD TIME REMAINING AND TAPS REMAINING TO SCREEN ################
        
    # updates input values for Drop Mode
    def Drop_global_update(self):
        global main_height
        global main_interval
        global main_drops
        global main_weight
        global drops_left
        global start

        # sets height, interval, weight, and drops variables to what the user has chosen
        main_height = int(sm.get_screen('drop_screen').label1.choice)
        main_interval = int(sm.get_screen('drop_screen').label2.choice)
        main_drops = int(sm.get_screen('drop_screen').label3.choice)
        main_weight = int(sm.get_screen('drop_screen').label4.choice)
        
        # update drop number and start lifting routine
        if(start == 0):
            drops_left = main_drops
            start = 1

        # update display values, give user feedback
        sm.get_screen('drop_screen').drop.text = str(drops_left) + ' Drops Remaining'

        print(main_height)
        print(main_interval)
        print(main_drops)

        #loop that runs in the background to check for flags
    def start_stop(self):
        global drops_left
        global first_drop
        
        #clears data 
        if (sm.get_screen('data').datalabel.flag == '1'):
            #throw the rest of this in a loop that first asks a pop up
            sm.get_screen('data').datalabel.flag = '0'
            with open("Sensor_Log.txt", "r+") as DeleteValues:
                DeleteValues.truncate(0)
            print("cleared log file")
            
        # checks for tap mode start, updates values, and runs tap mode
        if((sm.get_screen('tap_screen').start.flag == '1') and (first_tap == True)):
            print("running soft drops")
            DropScreen.Tap_global_update(self)
            Events.manage_taps(self)
            print("ran soft drops")
            
        #checks for drop mode start, updates values, then runs drop mode
        if((sm.get_screen('drop_screen').label5.flag == '1') and (first_drop == True)):
            print("running hard drops")
            DropScreen.Drop_global_update(self)
            Events.manage_drops(self)
            print("ran hard drops")
            
        #checks if drop mode has been activated, if not re run the loop
        elif(sm.get_screen('drop_screen').label5.flag == '0'):
            pass
        # elif to check if sotf taps has been checked, if not re run
        elif(sm.get_screen('tap_screen').start.flag == '0'):
            pass

# Events that run the machine (camera record, sensor reading, motor movement)
class Events(Screen):
    
    #control loop for tap mode
    def manage_taps(self):
        global Tap_Interval
        global Tap_Force
        global first_tap
        global main_height
        global Tap_Ammount 
        global Taps_Left 
        
        
        # arbitrary height currently, later set to a force value
        main_height = 5
        
        # if first tap, do process and then wait (tap interval) seconds
        # LATER, REPLACE WITH IF LOOP BASED ON IF IT HITS A FORCE NUMBER (IF IT HITS FORCE NUMBER, PULL BACK)
        if(first_tap):
            first_tap = False
            print("first tap")
            
            Events.cam_record(self)
            Events.toggle_hold_out(self)
            Events.lift(self)
            Events.Read_Sensor(self) # <-- for now, (figure out how to make it loop constantly later (start record, stuff, stop record)
            time.sleep(3)  #sleep to let sensor and camera catch up
            Events.lower(self)
            Events.lift(self)
            Events.Save_Data(self)
            time.sleep(3)  #sleep for an ammount to make cam record longer
            Events.cam_stop(self)
            
            Taps_Left = Taps_Left -1
            sm.get_screen('tap_screen').tapleft.text = str(Taps_Left) + ' taps Remaining'
            print('taps left ' + str(Taps_Left))
            
            Clock.schedule_once(Events.manage_taps, Tap_Interval)
            
        elif ((first_tap == False) and (Taps_Left > 0) ):
            print ('beginning next tap')
            Events.cam_record(self)
            Events.Read_Sensor(self)# <-- for now, (figure out how to make it loop constantly later (start record, stuff, stop record)
            time.sleep(3)  #sleep to let sensor and camera catch up
            Events.lower(self)
            Events.lift(self)
            Events.Save_Data(self)
            time.sleep(3)  #sleep for an ammount to make cam record longer
            Events.cam_stop(self)
            
            Taps_Left = Taps_Left-1
            sm.get_screen('tap_screen').tapleft.text = str(Taps_Left) + ' taps Remaining'
            print('taps left ' + str(Taps_Left))
            
            Clock.schedule_once(Events.manage_taps, Tap_Interval)
        
        elif(Taps_Left == 0):
            print("Taps Complete")
            
            sm.get_screen('tap_screen').start.flag = '0'
            sm.get_screen('tap_screen').start.text = 'Done / Start'
            first_tap = True
            camera.stop_preview()
            
            # adds data to data screen preview
            with open("Sensor_Log.txt", "r+") as UploadValues:
                f = UploadValues.readlines()
                count = 0
                for line in f:
                    count +=1

                    sm.get_screen('data').datalabel.text += str(line) + "\n"
                    print("adding line {} to datalabel".format(count))
                count = 0
            
    #control loop for Drop Mode
    def manage_drops(self):  
        global drops_left
        global first_drop
        global main_interval
        global main_drops
        global start
        
        #if this is the first drop, do drop process and then call this event again
        if(first_drop):
            drops_left = main_drops
            first_drop = False
            print("First Drop")
            
            # drop process
            Events.cam_record(self)
            Events.toggle_hold_out(self)
            Events.lift(self)
            Events.Read_Sensor(self)# <-- for now, (figure out how to make it loop constantly later (start record, stuff, stop record)
            time.sleep(3)  #sleep to let sensor and camera catch up
            Events.toggle_hold_in(self)
            Events.lower(self)
            Events.toggle_hold_out(self)
            Events.lift(self)
            Events.Save_Data(self)
            time.sleep(3)  #sleep to make cam record longer
            Events.cam_stop(self)

            # drops left update
            drops_left = drops_left-1
            sm.get_screen('drop_screen').drop.text = str(drops_left) + ' Drops Remaining'
            print('drops left ' + str(drops_left))
            print('first drop done\n')
            
            #schedule this function again (main_interval) seconds later
            Clock.schedule_once(Events.manage_drops, main_interval)
            pass

        #if after first drop and there are drops left, run drop protocol again and schedule this function again
        elif((first_drop == False) and (drops_left > 0)):
            print('starting ' +str(drops_left) + 'th drop')
            
            #drop process
            Events.cam_record(self)
            Events.Read_Sensor(self)# <-- for now, (figure out how to make it loop constantly later (start record, stuff, stop record)
            time.sleep(3)  #sleep to let sensor and camera catch up
            Events.toggle_hold_in(self)
            Events.lower(self)
            Events.toggle_hold_out(self)
            Events.lift(self)
            Events.Save_Data(self)
            time.sleep(3)  #sleep to make cam record longer
            Events.cam_stop(self)
            print('drop complete!')
            
            #drops left update
            drops_left = drops_left-1
            print('drops left = ' + str(drops_left))
            sm.get_screen('drop_screen').drop.text = str(drops_left) + ' Drops Remaining'


            #schedule next drop after (main interval) seconds
            Clock.schedule_once(Events.manage_drops, main_interval)
            pass

        #if there are no more drops, stop process
        elif(drops_left == 0):
            print("Drops Complete")
            sm.get_screen('drop_screen').label5.flag = '0'
            sm.get_screen('drop_screen').label5.text = 'Done / Start'
            start = 0
            first_drop = True
            camera.stop_preview()
            # adds data to data screen preview
            with open("Sensor_Log.txt", "r+") as UploadValues:
                f = UploadValues.readlines()
                count = 0
                for line in f:
                    count +=1

                    sm.get_screen('data').datalabel.text += str(line) + "\n"
                    print("adding line {} to datalabel".format(count))
                count = 0
    
    #records until cam_stop is called
    def cam_record(self):
        global drops_left
        global Taps_Left
        global start
        
        print('starting recording')
        #differentiate between taps and drops
        if (start == 1):
            camera.annotate_text = "Drop # {}".format(drops_left)
            camera.start_preview(fullscreen=False, window =(0,145,960,720))
            camera.start_recording('/home/pi/Desktop/Drop # {}.h264'.format(drops_left))
        else:
            camera.annotate_text = "Tap # {}".format(Taps_Left)
            camera.start_preview(fullscreen=False, window =(0,145,960,720))
            camera.start_recording('/home/pi/Desktop/Tap # {}.h264'.format(Taps_Left))
    
    #stops recording
    def cam_stop(self):
        camera.stop_recording()
        print('stopped recording')
                
    def Read_Sensor(self):
        # setting up variables. (sensor duration effects how long the sensor reads for)
        global Time_Running
        global List_Of_Values
        global TimeArray
        global Sensor_Duration
        global Sensor_Time_Interval
        global bus
        global Sensor_Address
        print("reading")
        
        # loops for DURATION seconds, reading every INTERVAL seconds
        while True:
            All_Data = bus.read_i2c_block_data(Sensor_Address,0x00,6)
            Sensor_Force_Value = (All_Data[4] << 8 | All_Data[5]) - 255
            List_Of_Values.append(Sensor_Force_Value)
            TimeArray.append(Time_Running)
            time.sleep(Sensor_Time_Interval) #timestamp/frameindex?
            Time_Running = round(Time_Running + Sensor_Time_Interval, 3)
            if (Time_Running > Sensor_Duration):
                print('has been read')
                break
    '''
    #figure out how to make these work as opposed to waiting to read sensor
    def Start_Sensor_Read(self):
        #vv in main control loop
        #Clock.schedule_interval(Events.Start_Sensor_Read(self), Sensor_Time_Interval)
        global Time_Running
        global List_Of_Values
        global TimeArray
        global bus
        global Sensor_Address
        global Sensor_Time_Interval
        
        All_Data = bus.read_i2c_block_data(Sensor_Address,0x00,6)
        Sensor_Force_Value = (All_Data[4] << 8 | All_Data[5]) - 255
        List_Of_Values.append(Sensor_Force_Value)
        TimeArray.append(Time_Running)
        Time_Running = round(Time_Running + Sensor_Time_Interval, 3)
        
    def Stop_Sensor_Read(self):
        Clock.unschedule(Events.Start_Sensor_Read)
     '''   
        
    def Save_Data(self):
        TimeStamp= TimeArray[List_Of_Values.index(max(List_Of_Values))]
        
        print("Highest Force = {}".format(max(List_Of_Values)))
        print("writing value to log")
    
         #writes data values to a log file, each line = new drop
        
        if(sm.get_screen('tap_screen').start.flag == '1'):
            with open("Sensor_Log.txt", "a") as WriteValues:
                WriteValues.write(("Tap Mode: Tap # = {} | Set Force Value = {} PSI| TimeStamp = {} SECONDS| Tap Interval = {} SECONDS\n").format(Taps_Left, Tap_Force, TimeStamp, Tap_Interval))
        
        if(sm.get_screen('drop_screen').label5.flag == '1'):
            with open("Sensor_Log.txt", "a") as WriteValues:
                WriteValues.write(("Drop Mode: Drop # = {} | Force Value = {} PSI| Height = {} CM| Weight = {} GRAMS| TimeStamp = {} SECONDS| Drop Interval = {} SECONDS\n").format(drops_left, str(max(List_Of_Values )), main_height, main_weight, TimeStamp, main_interval))
       
        List_Of_Values.clear()
        TimeArray.clear()
        Time_Running = 0
        print("wrote value to log")
        
    #Push micro actuator out
    def toggle_hold_out(self):
        print('holding out')

        kit.motor1.throttle = -1.0     #engage outward
        time.sleep(1.5)
        kit.motor1.throttle = 0       #current related
        time.sleep(2) #to get positioned correctly
        #pass
        
    #pull micro actuator in
    def toggle_hold_in(self):
        print("holding in")
        
        kit.motor1.throttle = 1.0     #engage inward
        time.sleep(1.5)
        kit.motor1.throttle = 0
        time.sleep(2) #to get positioned correctly

        pass
        pass#needed? or put in toggle hold out

    #lift large motor upwards, for height ammount
    def lift(self): 
        global main_height
        print('lifting ' + str(main_height))
    
        # 1 cm = 394 steps
        # for every step in height (main height = height * stepper conversion)
        for i in range(main_height*394):
            kit1.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)     #lift
        kit1.stepper1.release()  #so motor current dosnt spike

        #check release and double
        pass

    def lower(self):  # LOWER
        global main_height
        print('lowering ' + str(main_height))

        # 1 cm = 394 steps
        # *395 to ensure it bottoms out evenly
        for i in range(main_height*395):
            kit1.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)     #lower
        kit1.stepper1.release()

        pass

    pass

# UNCOMMENT THESE WHEN SENDING !!!

#motor addresses
'''
kit = MotorKit()
kit1= MotorKit(address=0x61)
'''

#kivy screen logic and variable names
sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(TapScreen(name='tap_screen'))
sm.add_widget(DropScreen(name='drop_screen'))
sm.add_widget(NumScreen(name='numpad'))
sm.add_widget(DataScreen(name='data'))

sm.add_widget(Events(name='event'))  # this may be a dont care (events)



class TestApp(App):

    def build(self):
        # drives flag-check mechanic off of start_stop

        Clock.schedule_interval(DropScreen.start_stop, 1)
        return sm


if __name__ == '__main__':
    GUI = TestApp()
    GUI.run()
