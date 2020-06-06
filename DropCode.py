### imports ###
import kivy
import time
import sched
import threading
import smbus
import picamera

# this is a tests 
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

 ### Configuration of the Main window ###
from kivy.config import Config
from kivy.core.window import Window
Config.set('graphics', 'position', 'custom')    
Config.set('graphics', 'left' , 0)              
Config.set('graphics', 'top', 0)                
Window.fullscreen = 'auto'                      
kivy.require('1.11.1')

### Initializing Globals ###
main_height = 0
main_interval = 0
main_drops = 0
main_weight = 0
drops_left = 0

### flags ###
start = 0
first_drop = True

### Camera Setup ###
camera= picamera.PiCamera()
camera.resolution = (1280, 960)
camera.framerate = 15 # 0-15
camera.brightness = 60
camera.contrast = 60
#camera.start_preview(fullscreen=False, window =(100,50,1000,1000))

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
<HomeScreen>:

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
    duration:duration
    
    FloatLayout:
    
        Label:
            text:'Tap Mode' 
            font_size: 40
            size_hint:(1,.2)
            pos_hint: {'center_x':.5,'top':1}

        Button:
            id: duration
            choice: '0'                     
            flag: '0'
            
            text:'Experiment Duration:'
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.75,'top':.6}
                                   
            on_press:
                root.manager.get_screen('tap_screen').duration.flag = '1' 
                root.manager.current = 'numpad'                   


        Label:
            text: 'Time Remaining: '
            font_size: 25
            size_hint:(.669,.1)
            pos_hint:{'center_x':.25,'top':.2}
            
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
            pos_hint:{'center_x':.75,'top': .8}
            
            on_press:
                if(root.manager.get_screen('tap_screen').start.flag == '0'):root.manager.get_screen('tap_screen').start.flag = '1'; root.manager.get_screen('tap_screen').start.text = 'STOP'
                elif(root.manager.get_screen('tap_screen').start.flag == '1'):root.manager.get_screen('tap_screen').start.flag = '0';root.manager.get_screen('tap_screen').start.text = 'START'

        Button:
            text: 'Data'
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.6,'top':.35}

            on_press:
                root.manager.current = 'data'

        Button:
            text: 'Home'
            font_size: 25
            size_hint: (.2,.15)
            pos_hint:{'center_x':.9,'top':.35}

            on_press:
                root.manager.current = 'home'

            
            
            
            
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
                    elif((root.manager.get_screen('drop_screen').label2.flag) == '1'):root.manager.get_screen('drop_screen').label2.text = entry.text + ' second interval' ; root.manager.get_screen('drop_screen').label2.choice = entry.text
                    
                    # Drop Mode Drop Number Button
                    elif((root.manager.get_screen('drop_screen').label3.flag) == '1'):root.manager.get_screen('drop_screen').label3.text = entry.text + ' drops' ; root.manager.get_screen('drop_screen').label3.choice = entry.text
                    
                    # Drop Mode Weight Button
                    elif((root.manager.get_screen('drop_screen').label4.flag) == '1'):root.manager.get_screen('drop_screen').label4.text = entry.text + ' grams' ; root.manager.get_screen('drop_screen').label4.choice = entry.text
                    
                    #Tap Mode Duration Button
                    elif((root.manager.get_screen('tap_screen').duration.flag)=='1'):root.manager.get_screen('tap_screen').duration.text = entry.text + ' Second Experiment'; root.manager.get_screen('tap_screen').duration.choice = entry.text

                    #
                    if((root.manager.get_screen('tap_screen').duration.flag)=='1'): root.manager.current = 'tap_screen'
                    elif((root.manager.get_screen('tap_screen').duration.flag)=='0'): root.manager.current = 'drop_screen'
                    
                    #clear flags after so you dont add number value to another box
                    root.manager.get_screen('drop_screen').label1.flag = '0'
                    root.manager.get_screen('drop_screen').label2.flag = '0'
                    root.manager.get_screen('drop_screen').label3.flag = '0'
                    root.manager.get_screen('drop_screen').label4.flag = '0'
                    root.manager.get_screen('tap_screen').duration.flag = '0'

                    #instantiate the variable for user input
                    entry.text = ''

#Drop Screen
<DropScreen>:
    label1: label1                          #height
    label2: label2                          #interval
    label3: label3                          #Drops
    label4: label4                          #Weight
    label5: label5                          #Start
    drop:   drop
    
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
            text: 'Data '
            font_size: 25
            size_hint:(.2,.15)
            pos_hint:{'center_x':.65,'top':.2}

            on_press:
                root.manager.current = 'data'

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
            on_press: root.manager.current = 'home'

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
            
            #on_press:
                #root.manager.current = 'LAST SCREEN'
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
    
    # updates user input values
    def global_update(self):
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
            
        # checks for tap mode start and runs tap mode
        if(sm.get_screen('tap_screen').start.flag == '1'):
            # global update here (update values needed for soft drops)
            # instead of below, send to a manage_soft_drops thing
            print("running soft drops")
            Events.cam_record(self)
            Events.Read_Sensor_Soft(self)
            events.cam_stop(self)
            print("ran soft drops")
            
        #checks for drop mode start, updates values, then runs drop mode
        if((sm.get_screen('drop_screen').label5.flag == '1') and (first_drop == True)):
            print("running hard drops")
            MenuScreen.global_update(self)
            Events.manage_drops(self)
            print("ran hard drops")
            
        #checks if drop mode has been activated, if not re run the loop
        elif(sm.get_screen('drop_screen').label5.flag == '0'):
            pass
        # elif to check if sotf taps has been checked

# Events that run the machine (camera record, sensor reading, motor movement)
class Events(Screen):
    
    #records until cam_stop is called
    def cam_record(self):
        global drops_left
        
        print('starting recording')
        camera.annotate_text = "experiment # {}".format(drops_left)
        camera.start_preview(fullscreen=False, window =(0,145,960,720))
        camera.start_recording('/home/pi/Desktop/Drop # {}.h264'.format(drops_left)) 
    
    #stops recording
    def cam_stop(self):
        camera.stop_recording()
        print('stopped recording')
        
    #control loop for Drop Mode
    def manage_drops(self):  
        global drops_left
        global first_drop
        global main_interval
        global start
        # have to have first drop and latter drops or it would run forever
        
        ##################################### MAIN ACTION LOOP FOR DROP MODE ##############################
        
        #if this is the first drop, do drop process and then call this event again
        if(first_drop):
            first_drop = False
            print("First Drop")
            
            # drop process
            Events.cam_record(self)
            Events.toggle_hold_out(self)
            Events.lift(self)
            Events.toggle_hold_in(self)
            Events.Read_Sensor_Hard(self)
            Events.lower(self)
            Events.cam_stop(self)

            # drops left update
            drops_left = drops_left-1
            sm.get_screen('drop_screen').drop.text = str(drops_left) + ' Drops Remaining'
            print('drops left ' + str(drops_left))
            print('first drop done\n')
            
            #schedule this function again and get out of this if statement
            Clock.schedule_once(Events.manage_drops, main_interval)
            pass

        #if after first drop and there are drops left, run drop protocol again and schedule this function again
        elif((first_drop == False) and (drops_left > 0)):
            print('starting ' +str(drops_left) + 'th drop')
            
            #drop process
            Events.cam_record(self)
            Events.toggle_hold_out(self)
            Events.lift(self)
            Events.toggle_hold_in(self)
            Events.Read_Sensor_Hard(self)
            Events.lower(self)
            Events.cam_stop(self)
            print('drop complete!')
            
            #drops left update
            drops_left = drops_left-1
            print('drops left = ' + str(drops_left))
            sm.get_screen('drop_screen').drop.text = str(drops_left) + ' Drops Remaining'


            #schedule next drop and get out of if statement
            Clock.schedule_once(Events.manage_drops, main_interval)
            pass

        #if there are no more drops, stop process
        elif(drops_left == 0):
            print("Drops Complete")
            sm.get_screen('drop_screen').label5.flag = '0'
            sm.get_screen('drop_screen').label5.text = 'Done / Start'
            start = 0
            first_drop = True
            # make an upload values event that uploads to label as well as data file
            
            # adds data to data screen preview
            with open("Sensor_Log.txt", "r+") as UploadValues:
                f = UploadValues.readlines()
                count = 0
                for line in f:
                    count +=1

                    sm.get_screen('data').datalabel.text += str(line) + "\n"
                    print("adding line {} to datalabel".format(count))
                count = 0
                
    #INSTEAD OF READ SENSOR SOFT AND HARD, MAKE READ SENSOR AND STOP READ SENSOR
                
    #sensor read for drop mode
    def Read_Sensor_Hard(self):
        # setting up variables. (sensor duration effects how long the sensor reads for)
        DURATION = 5 # IN Seconds
        Time_Running = 0
        List_Of_Values = []
        TimeArray = []
        bus = smbus.SMBus(1)
        Sensor_Address = 0x04
        INTERVAL = .025
        print("reading")
        
        # loops for DURATION seconds, reading every INTERVAL seconds
        while True:
            All_Data = bus.read_i2c_block_data(Sensor_Address,0x00,6)
            Sensor_Force_Value = (All_Data[4] << 8 | All_Data[5]) - 255
            List_Of_Values.append(Sensor_Force_Value)
            TimeArray.append(Time_Running)
            time.sleep(INTERVAL) #timestamp/frameindex?
            Time_Running = round(Time_Running + INTERVAL, 3)

            if (Time_Running > DURATION):
                
                TimeStamp= TimeArray[List_Of_Values.index(max(List_Of_Values))]
                print("Highest Force = {}".format(max(List_Of_Values)))
                print("writing value to log")
                
                #writes data values to a log file, each line = new drop
                with open("Sensor_Log.txt", "a") as WriteValues:
                    WriteValues.write(("Drop # = {} | Force Value = {} PSI| Height = {} CM| Weight = {} GRAMS| TimeStamp = {} SECONDS| Interval = {} SECONDS\n").format((main_drops - drops_left), str(max(List_Of_Values )), main_height, main_weight, TimeStamp, main_interval))
                List_Of_Values.clear()
                TimeArray.clear()
                print("wrote value to log")
                break
            
    #honestly just get rid of this because you misunderstood
    #sensor read for tap mode
    def Read_Sensor_Soft(self):
        DURATION = int(sm.get_screen('tap_screen').duration.choice) # IN Seconds
        Time_Running = 0
        List_Of_Values = []
        TimeArray = []

        bus = smbus.SMBus(1)
        Sensor_Address = 0x04

        print('Duration = {} seconds'.format(DURATION))
        print("reading")
        while True:
            All_Data = bus.read_i2c_block_data(Sensor_Address,0x00,6)
            Sensor_Force_Value = (All_Data[4] << 8 | All_Data[5]) - 255
            #print("Force = {} PSI, TimeStamp = {} seconds".format(Sensor_Force_Value,Time_Running))
            List_Of_Values.append(Sensor_Force_Value)
            TimeArray.append(Time_Running)
            for value in List_Of_Values:
                if value <= 10: #############TOLERANCE,,, IF SOFTER SET VALUE THRESHOLD LOWER
                    del TimeArray[List_Of_Values.index(value)]
                    #TimeArray.remove([List_Of_Values.index(value)])
                    List_Of_Values.remove(value)

            time.sleep(.025) #<-- increments at rates of .025 seconds, could do something with timestamp and frameindex
            Time_Running = round(Time_Running +.025, 3)

            if (Time_Running > DURATION): # <-- this will be replaced with (if motors still running/if start still pressed) but testing for now

                print("Highest Force = {}".format(max(List_Of_Values)))
                #sm.get_screen('data').datalabel.text = str(max(List_Of_Values)) #<--sens one value to label

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
                        sm.get_screen('data').datalabel.text += str(line) + "\n"
                        print("adding line {} to datalabel".format(count))
                    count = 0

                List_Of_Values.clear()
                TimeArray.clear()
                print("wrote value to log")
                sm.get_screen('tap_screen').start.flag = '0'
                sm.get_screen('tap_screen').start.text = 'Done/Start'
                break

    #Push micro actuator out
    def toggle_hold_out(self):
        print('holding out')

        kit.motor1.throttle = -1.0     #engage outward
        time.sleep(1.5)
        kit.motor1.throttle = 0       #current related
        
        #pass
        
    #pull micro actuator in
    def toggle_hold_in(self):
        print("holding in")
        
        kit.motor1.throttle = 1.0     #engage inward
        time.sleep(1.5)
        kit.motor1.throttle = 0

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
