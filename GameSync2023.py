from threading import Thread
import ctypes
from ctypes import *
import ctypes.wintypes
import json
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
import sys,os
DeviceIP = "10.1.1.43" #INSERT YOUR DEVICE IP

def GoveeLocalControl(Command,brightness=0,color=None,Loop=False,UDP_IP='',UDP_PORT=4003,printStatus=True,errorCount=0):
    lastColor = None
    global sock

    def SendCommand(message,individualIP,UDP_PORT):
        jsonResult = json.dumps(message)
        print("Sending: {} to {}".format(Command,individualIP))
        sock.sendto(bytes(jsonResult, "utf-8"), (individualIP, UDP_PORT))

    try:
        if Command == "Color":      
                message = {
                    "msg":{
                        "cmd":"colorwc",
                        "data":{
                            "color":{"r":color[0],"g":color[1],"b":color[2]},
                            "colorTemInKelvin":0
                        }    
                    }
                }    
        elif Command == "On":
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

        #To print or not to print
        if Loop == False and printStatus == True:
            print("Govee Internal Control: {}".format(Command)) 
        
        #Send command from above
        SendCommand(message,UDP_IP,UDP_PORT)
    except Exception as E:        
        errorCount += 1
        if errorCount > 3:
            print("Govee Internal Control Error Recursion Exit: {}".format(str(E)))
            return
        else:
            print("Govee Internal Control Error: {}".format(str(E)))
            return GoveeLocalControl(Command,brightness=0,color=None,Loop=False,UDP_IP='',UDP_PORT=4003,printStatus=True,errorCount=errorCount)


def main(DeviceIP):
    global boxSize
    global sock
    errorNotified = False
    lastColor = None
    handle = None
    whndl = None
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    print("Using Screen Dimensions: {} {}".format(screen_width,screen_height))
    middle_x = screen_width // 2
    middle_y = screen_height // 2

    # Get the device context for the entire screen
    screen_dc = user32.GetDC(None)

    # Create a compatible device context
    mem_dc = gdi32.CreateCompatibleDC(screen_dc)

    # Create a bitmap compatible with the screen device context
    bmp = gdi32.CreateCompatibleBitmap(screen_dc, 1, 1)

    # Select the bitmap object into the compatible device context
    gdi32.SelectObject(mem_dc, bmp)

    # Define the value of SRCCOPY manually
    SRCCOPY = 0xCC0020    


   
    try:
        print("Game Time Function: Turning Lights On")       
        GoveeLocalControl(Command="On",UDP_IP=DeviceIP) 
        GoveeLocalControl(Command="BrightLevel",UDP_IP=DeviceIP,brightness=100)
        while(1):            
            # Copy the pixel color from the screen to the bitmap
            gdi32.BitBlt(mem_dc, 0, 0, 1, 1, screen_dc, middle_x, middle_y, SRCCOPY)

            # Retrieve the color value of the pixel
            pixel_color = gdi32.GetPixel(mem_dc, 0, 0)

            # Extract the individual color components (red, green, blue)
            red = pixel_color & 0xFF
            green = (pixel_color >> 8) & 0xFF
            blue = (pixel_color >> 16) & 0xFF
            pixelColor = (red,green,blue)   

            try:    
                #Send colors
                if pixelColor == lastColor:
                    # print("Same Color")
                    continue
                elif "Error" in pixelColor:
                    if errorNotified == False:
                        print("Error In Colors Loop: {}".format(pixelColor))
                    errorNotified = True
                    time.sleep(5)
                    continue
                else:
                    # print(pixelColor)
                    lastColor = pixelColor
                    errorNotified = False

                    message = {
                                "msg":{
                                    "cmd":"colorwc",
                                    "data":{
                                        "color":{"r":red,"g":green,"b":blue},
                                        "colorTemInKelvin":0
                                    }    
                                }
                            }                        
                    # print("Sending: {}".format(Command))
                    sock.sendto(bytes(json.dumps(message), "utf-8"), (DeviceIP, 4003))             
            except Exception as E:
                print("Govee Game Time Inner Loop Error: {}".format(str(E)))
        #If for some reason we break from loop and we return from this thread, we want to power down lights.
        print("Game Time Function: Turning Lights Off. Thread Is Dead.") 
        gdi32.DeleteDC(mem_dc)
        gdi32.DeleteDC(screen_dc)
        GoveeLocalControl(Command="Off",UDP_IP=DeviceIP)
        raise NameError("NormalReturn")
    except Exception as E:
        if "NormalReturn" in str(E):
            print("Game Time Function: Turning Lights Off. Thread Is Dead.")
            return "NormalExit"
        else:
            print("Govee Game Time Loop Error: {}".format(str(E)))
            GoveeLocalControl(Command="Off",UDP_IP=DeviceIP)
            return "Error"        

try:
    print("Press Ctrl + C To Quit (Lights Should Turn Off)\n\n")
    main(DeviceIP)
except KeyboardInterrupt:
    GoveeLocalControl(Command="Off",UDP_IP=DeviceIP) 
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)

