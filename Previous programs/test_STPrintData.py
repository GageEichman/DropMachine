import sys
import os
import time
import subprocess
from tkinter import *
import tkinter.font
#import pyautogui

testtxt = input("would you like to take force data? Yes=1 No=0 ")
txt = int(testtxt)

if (txt==1):
    os.system('python pps-singletact.py -v &>> STSenseData.txt')
    pyautogui.hotkey('alt','tab')
    pyautogui.hotkey('enter')
    
    #command = ['ls', '-l']
    #p = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #text = p.stdout.read()
    #retcode = p.wait()
    #test_text= string(text)
    #print (test_text)
    
    ' '.join(sys.argv[1:])
    
else:
    print("End of program")

    

