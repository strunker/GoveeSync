# pywin32 must be installed
# pip install wmi

import win32gui
import win32process
import win32pdhutil
import wmi
import time
import socket
import json
import math
import threading
from ctypes import *
import ctypes.wintypes

#Globals, you should not change these, leave them as is.
appChange = True
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Constants, you should change these.
GoveeDeviceIP = '10.1.1.43' 
boxSize = 50


def GoveeInternalControl(Command,brightness=0,color=None,Loop=False,UDP_IP=GoveeDeviceIP,UDP_PORT=4003):
    lastColor = None
    global sock
    global stopLoop

    def SendCommand(message,UDP_IP,UDP_PORT):
        jsonResult = json.dumps(message)
        # print("Sending: {}".format(Command))
        sock.sendto(bytes(jsonResult, "utf-8"), (UDP_IP, UDP_PORT))

    try:
        if Command == "On":
            message = {
                "msg":{
                    "cmd":"turn",
                    "data":{
                        "value":1,
                    }    
                }
            }
        elif Command == "Off":
            message = {
                "msg":{
                    "cmd":"turn",
                    "data":{
                        "value":0,
                    }    
                }
            }            
        elif Command == "Color":      
                message = {
                    "msg":{
                        "cmd":"colorwc",
                        "data":{
                            "color":{"r":color[0],"g":color[1],"b":color[2]},
                            "colorTemInKelvin":0
                        }    
                    }
                }         
        elif Command == "BrightLevel":
            message = {
                "msg":{
                    "cmd":"brightness",
                    "data":{
                        "value":brightness,
                    }    
                }
            }  
        else:
            raise ValueError("Bad Command: {}".format(Command))

        if Loop == False:
                print("\nGovee Internal Control: {}".format(Command))
        
        SendCommand(message,UDP_IP,UDP_PORT)        
    except Exception as E:
        print("\nGovee Internal Control Error: {}".format(str(E)))

def DetectFocusChange():
    global appChange
    currentPID = ""
    while(1):
        time.sleep(1.5)
        whndl = win32gui.GetForegroundWindow()
        tempPID = (win32process.GetWindowThreadProcessId(whndl))[1]
        if currentPID != tempPID:
            print("\nDetected Window Change: {}".format(tempPID))
            currentPID = tempPID
            appChange = True

def GameTime():
    global appChange
    global boxSize
    lastColor = None
    pid = ""

    def GetColors(handle,upperLeft,lowerLeft,upperRight,lowerRight):
        try:
            def rgbint2rgbtuple(RGBint,skew,):        
                red =  RGBint & 255
                green = (RGBint >> 8) & 255
                blue = (RGBint >> 16) & 255
                return (red * skew,green * skew,blue *skew)

            pixels = [rgbint2rgbtuple(win32gui.GetPixel(handle,upperLeft[0],upperLeft[1]),1),
                      rgbint2rgbtuple(win32gui.GetPixel(handle,lowerLeft[0],lowerLeft[1]),1),
                      rgbint2rgbtuple(win32gui.GetPixel(handle,upperRight[0],upperRight[1]),1),
                      rgbint2rgbtuple(win32gui.GetPixel(handle,lowerRight[0],lowerRight[1]),1)] 
            red = 0
            green = 0
            blue = 0
            for pixel in pixels:
                red += pixel[0]**2
                green += pixel[1]**2
                blue += pixel[2]**2
            return int(math.sqrt(red/len(pixels))),int(math.sqrt(green/len(pixels))),int(math.sqrt(blue/len(pixels)))
        except Exception as E:
            # time.sleep(10)
            return "Get Colors Error: {}".format(str(E))

    try:
        GoveeInternalControl("On") 
        GoveeInternalControl("BrightLevel",brightness=100)
        while(1):
            if appChange == True:
                handle = None
                whndl = None
                whndl = win32gui.GetForegroundWindow()
                pid =(win32process.GetWindowThreadProcessId(whndl))[1]                
                handle = win32gui.GetWindowDC(whndl)       
                txt = win32gui.GetWindowText(whndl)    
                rect = ctypes.wintypes.RECT()
                DWMWA_EXTENDED_FRAME_BOUNDS = 9
                ctypes.windll.dwmapi.DwmGetWindowAttribute(
                    ctypes.wintypes.HWND(whndl),
                    ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
                    ctypes.byref(rect),
                    ctypes.sizeof(rect)
                    )
                size = (rect.right - rect.left, rect.bottom - rect.top)                
                windowWidth = size[0]
                windowHeight = size[1]
                centerWidth = int(windowWidth / 2)
                centerHeight = int(windowHeight / 2)
                upperLeft = (centerWidth-boxSize,centerHeight-boxSize)
                lowerLeft = (centerWidth-boxSize,centerHeight+boxSize)
                upperRight = (centerWidth+boxSize,centerHeight-boxSize)
                lowerRight = (centerWidth+boxSize,centerHeight+boxSize)
                print("\nFound New Focused Window:\nPid: {}\nWidth: {}\nHeight: {}\nupperLeft: {}\nlowerLeft: {}\nupperRight: {}\nlowerRight: {}".format(pid,windowWidth,windowHeight,upperLeft,lowerLeft,upperRight,lowerRight))     
                appChange = False

            pixelColor = GetColors(handle,upperLeft,lowerLeft,upperRight,lowerRight)
            if pixelColor == lastColor:
                continue
            elif "Error" in pixelColor:
                print("\nError In Loop: {}".format(pixelColor))
            else:
                lastColor = pixelColor       
                GoveeInternalControl("Color",color=pixelColor,Loop=True)
        GoveeInternalControl("Off")
        return "Done"
    except Exception as E:
        print("\nGame Time Loop Error: {}".format(str(E)))
        GoveeInternalControl("Off")
        return "Error"

GoveeInternalControl("Off")

appFocusThread = threading.Thread(name="AppThread",target=DetectFocusChange)
appFocusThread.start() 

GameTime()
# GoveeInternalControl("On")
# time.sleep(2)
# GoveeInternalControl("BrightLevel",100) #1-100% expressed as an integer
# time.sleep(2)
# GoveeInternalControl("Color",color=(255,0,0)) 
# time.sleep(2)
# GoveeInternalControl("BrightLevel",50) #1-100% expressed as an integer
# time.sleep(2)
# GoveeInternalControl("Color",color=(0,255,0))
# time.sleep(2)
# GoveeInternalControl("BrightLevel",10) #1-100% expressed as an integer
# time.sleep(2)
# GoveeInternalControl("Off")
