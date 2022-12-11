# GoveeSync
This code will allow you to use Govee internal UDP api to control your device as well as sync what is on the screen.

# Constants
Update the device IP of the device you want to control on line 19. Lines 20 and 21, for now sadly, need to hardcode the resolution of the game you are playing at. I tried to fix this by getting the window size, but it was not reliable. 

# Supported Commands

To turn the device on/off:<br>
GoveeInternalControl("On")<br>
GoveeInternalControl("Off")<br>
<br>
To set the brightness:<br>
GoveeInternalControl("BrightLevel",100) #1-100% expressed as an integer<br>
GoveeInternalControl("BrightLevel",50) #1-100% expressed as an integer<br>
GoveeInternalControl("BrightLevel",10) #1-100% expressed as an integer<br>
<br>
To change the color:<br>
GoveeInternalControl("Color",color=(0,255,0)) #Color expressed as a RGB tuple<br>
GoveeInternalControl("Color",color=(255,0,0)) #Color expressed as a RGB tuple<br>
<br>
To go into game mode where the screen will sync to the device:<br>
<strong>Do note: in this mode the code will attempt to lock onto the window that is in focus. Remember if you are playing a game you need to update the constants on line 20/21 with the resolution of the game you are playing, otherwise the color sync will not work as expected.<br><br>There is also a box size constant you can mess around with if you want to and see if you get better results.<br><br>This mode essentially works by creating a square in the center of the app's window. We sample a pixel at each of the four corners of the square, get the color values, then average those 4 color values together. that averaged out value is then sent to the Govee lights over UDP api.</strong><br>
<br>
GameTime()


