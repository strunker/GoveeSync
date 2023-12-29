# GoveeSync
This code will allow you to use Govee internal UDP api to control your device as well as sync what is on the screen. <strong>You need to install the below libs before running</strong>:<br>
pip install wmi<br>
pip install pywin32

# Constants
Update the device IP of the device you want to control on line 21.

# No Frills Screen Sync Script

If you don't want to get into the different functions and you just want something simple you can run and have work, just run GameSync2023.py file.<br>
<ol>
<li>Replace line 10 with your device IP, for example: DeviceIP = "192.168.0.1"</li>
<li>Open cmd prompt then simply run with - python c:\PathToFile\GameSync2023.py</li>
<li>You can simply do Ctrl + C to exit when you want to end the light sync.</li>
</ol>

# Full Featured Code With Many Supported Commands - All of the below commands are implemented within GameSync.py

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
<strong>Do note: in this mode the code will attempt to lock onto the window that is in focus.<br><br>There is a box size constant you can mess around with if you want to and see if you get better results.<br><br>This mode essentially works by creating a square in the center of the app's window. We sample a pixel at each of the four corners of the square, get the color values, then average those 4 color values together. That averaged out value is then sent to the Govee lights over UDP api.</strong><br>
<br>
GameTime()

# Testing / Searching for devices - This is optional if you want to search for available Govee LAN api devices on your network. 
Download UDPReceiver.py and UDPSender.py
<ol>
<li>Start CMD prompt, navigate to the folder where you downloaded the above files. Then type: python UDPReceiver.py<br>This should start a UDP multicast listener on port 4002</li>
<li>Once the listener is started open another CMD prompt. Navigate to the folder, and type: python UDPSender.py<br>This should output any Govee devices found to the shell.</li>
</ol>


