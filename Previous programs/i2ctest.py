import random
import time
'''
import smbus
import time

bus = smbus.SMBus(1)
Sensor_Address = 0x04
#read byte data gives that byte
#read block data gives that array of values with that #
#read i2c block data gives the entire array from int1-int2
#msb = data[4,0,2] most significant bit of sensor data
#lsb = data[5,1,3] least significant bit of sensor data

#All_Data = bus.read_i2c_block_data(Sensor_Address,0x00,6)
#^-- reads all sensor data (capacitive sense, clock, etc) and throws it in an array up to 32 bits
#technically only reads bytes 128- 133 (0x00,6), byte 128 = 1, byte 129 =2 etc.

Sensor_Force_Value = (All_Data[4] << 8 | All_Data[5]) - 255
#^-- reads force value of sensor with no respect to time
# outputs digital signal in PSI
frameindex = All_Data[0] << 8 | All_Data[1]
timestamp = All_Data[2] << 8 | All_Data[3]
#^-- clock data from device (most efficient time to readout wtih loop)
'''
''' #clock read stuff?
timestamp = 1
duration = 0
while True:
    All_Data = bus.read_i2c_block_data(Sensor_Address,0x00,6)
    frameindex = All_Data[0] << 8 | All_Data[1]
    timestamp = All_Data[2] << 8 | All_Data[3]
    print(timestamp)
    time.sleep(.01)
    duration += .01
    if duration > 1:
        break
'''


# V--- loop for reading sensor value
'''
DURATION = float(input("")) # IN Seconds
Time_Running = 0
List_Of_Values = []

while True:
    All_Data = bus.read_i2c_block_data(Sensor_Address,0x00,6)
    Sensor_Force_Value = (All_Data[4] << 8 | All_Data[5]) - 255
    print("Force = {} PSI, TimeStamp = {} seconds".format(Sensor_Force_Value,Time_Running))
    List_Of_Values.append(Sensor_Force_Value)
    time.sleep(.025) #<-- increments at rates of .025 seconds, could do something with timestamp and frameindex
    Time_Running = round(Time_Running +.025, 3)


    if (Time_Running > DURATION): # <-- this will be replaced with (if motors still running/if start still pressed) but testing for now
        print("Highest Force = {} PSI".format(max(List_Of_Values)))
        break

'''
#normalize readings somehow (if number repeated more than x times over x seconds, subtract that # from all readings
#instead of making an artificial timestamp, use the sensors given timestamp (timestamp)
#instead of using an artificaila time index, use the sensors given frame index (frameindex)
'''
            bus = smbus.SMBus(1)
            Sensor_Address = 0x04
            All_Data = bus.read_i2c_block_data(Sensor_Address,0x00,6)
            Sensor_Force_Value = (All_Data[4] << 8 | All_Data[5]) - 255
            sm.get_screen('force').forcelabel.text = str(Sensor_Force_Value)

            ^^ reads the value in the drop code once and displays it to the force screen

'''
'''
    def Read_Sensor(self):
        # read force and send to screen
        #if motors running, start recordning.
        #if drop just commenced, stop recordning
        #save all drop info to a file
        #record back the highest dropvalue in a table
        #reset back to baseline

        Time_Running = 0
        List_Of_Values = []
        bus = smbus.SMBus(1)
        Sensor_Address = 0x04

        while True: #print all data to an array
            All_Data = bus.read_i2c_block_data(Sensor_Address,0x00,6)
            Sensor_Force_Value = (All_Data[4] << 8 | All_Data[5]) - 255
             #prints the most recent # to the thing
            print("Force = {} PSI, TimeStamp = {} seconds".format(Sensor_Force_Value,Time_Running)) ####### prints tp terminal
            List_Of_Values.append(Sensor_Force_Value)
            time.sleep(.025) #<-- increments at rates of .025 seconds, could do something with timestamp and frameindex
            Time_Running = round(Time_Running +.025, 3)

                if Time_Running > :
                    root.manager.get_screen('ForceData').label.text = str(max(List_Of_Values))
                    #copy array of values for that test
                    List_Of_Values = []
                    break
'''
'''
class Events():
    def Read_Sensor():
        DURATION = float(input("")) # IN Seconds
        Time_Running = 0
        List_Of_Values = []

        while True:
            All_Data = bus.read_i2c_block_data(Sensor_Address,0x00,6)
            Sensor_Force_Value = (All_Data[4] << 8 | All_Data[5]) - 255
            print("Force = {} PSI, TimeStamp = {} seconds".format(Sensor_Force_Value,Time_Running))
            List_Of_Values.append(Sensor_Force_Value)
            time.sleep(.025) #<-- increments at rates of .025 seconds, could do something with timestamp and frameindex
            Time_Running = round(Time_Running +.025, 3)


            if (Time_Running > DURATION): # <-- this will be replaced with (if motors still running/if start still pressed) but testing for now
                print("Highest Force = {} PSI".format(max(List_Of_Values)))
                break
Events.Read_Sensor()
'''
'''
def Read_Sensor():
    DURATION = 5 # IN Seconds
    Time_Running = 0
    List_Of_Values = []

    bus = smbus.SMBus(1)
    Sensor_Address = 0x04
    print("reading")
    while True:
        All_Data = bus.read_i2c_block_data(Sensor_Address,0x00,6)
        Sensor_Force_Value = (All_Data[4] << 8 | All_Data[5]) - 255
        print("Force = {} PSI, TimeStamp = {} seconds".format(Sensor_Force_Value,Time_Running))
        List_Of_Values.append(Sensor_Force_Value)
        time.sleep(.025) #<-- increments at rates of .025 seconds, could do something with timestamp and frameindex
        Time_Running = round(Time_Running +.025, 3)

        if (Time_Running > DURATION): # <-- this will be replaced with (if motors still running/if start still pressed) but testing for now
            print("Highest Force = {} PSI".format(max(List_Of_Values)))
            #sm.get_screen('force').forcelabel.text = str(Sensor_Force_Value)

            break

Read_Sensor()
'''
'''
arrayA= [0,1,89,3,7]
arrayb=[0,1,13,3,4]

print(arrayb[arrayA.index(max(arrayA))])
'''

def Read_Sensor():
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
            print(List_Of_Values)
            print(TimeArray)
            print("highest force = {}, time of drop = {} seconds into the test".format(max(List_Of_Values), TimeArray[List_Of_Values.index(max(List_Of_Values))]))
            break
Read_Sensor()
