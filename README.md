# instrumentIO
I should have documented my use of pyvisa better the first time around.
<pre>
I remembered how easy using pyvisa was, but i forgot all the difficulties of setting it up when I left and came back to it. Had some interesting ideas, and projects, but the life got busier. Well, no time like the present to document my process in using this library with real instruments, with cryptic notes in source code. No damn it, we're going to write good docs! but first we're going to brain dump some notes.

Zeroth:
official docuentation:
https://pyvisa.readthedocs.io/en/1.8/getting.html

I followed those instructions, and it still did not work right. 
I can assume Im on linux. If not, maybe do a wellness check.
<br>
Check your group permissions with:
`
$groups
fossboss adm dialout cdrom sudo audio video plugdev games users input render netdev lpadmin gpio i2c spi
`
If you are not already a member of plugdev, and dialout, add yourself to these groups now.
`
$sudo usermod -aG plugdev $USER
$sudo usermod -aG dialout $USER
`
<br>
maybe install this linux system package:
`sudo apt-get install python3-pyvisa
`
Totaly install these pip packages....
pip install some dependencies:

(Recommend using a virtual enviornment: thought I am guilty of forgoing this)
on some systems, you might get a message that tells you python package management is externaly managed.
its basicly a polite warning telling you to set up a Virtual Enviornment right now, but youre not going to listen.
Instead, your going to disable that warning temporarily like this:
`
locate -i externally-managed
cd /path/to/externaly-managed-file/
mv EXTERNALLY-MANAGED tmp_EXTERNALLY-MANAGED
sudo mv EXTERNALLY-MANAGED tmp_EXTERNALLY-MANAGED
`
to find the path of the file locking your pip installations, move that file to a temp location, install a bunch of pip packages, then re-assert the thing locking up your ability to install packages. 
pip install pyvisa, zeroconf, psutil, pyusb



At the time of this writing i am unaware of a good automatic means to enstantiate devices. 
Pyvisa is pretty simple over TCP/IP, but USB proved to be more challenging. These instructions are for USB.

plug in your device, and run the command: $lsusb

`
$ lsusb
...
Bus 001 Device 003: ID 1ab1:6969 Rigol Technologies DS1xx4Z/MSO1xxZ series
Bus 001 Device 002: ID 2109:3431 VIA Labs, Inc. Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
`
Here we're interested in the vendor ID, and product ID of the instrument such that we can create udev rules for interfacing with the devices.
vendorID:1ab1
productID:6969
Example udev rule:


# Rigol DS1054
SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="1ab1", ATTRS{idProduct}=="6969", GROUP="m", MODE="0660"


`
 sudo udevadm control --reload-rules
 sudo udevadm trigger
`

but wait! where are udev files? and whats with the funny names they have?
Udev rules assign a precidence to the rules in /etc/udev/rules.d/
00-name.rules has a higher priority than 99-name.rules

The many nuances of writing udev rules is omited here, but is worth looking into for those interested...

You may also need other supporting softwares, I installed National Instruments libraries, which was a hasle of having to go to their website, register and download the things.
Then all I got was errors from deep within the libraries when trying to call thier code. 
Never the less, I will include their packages here. 

######### In Theory you can run pyvisa code now ###########

`
#!/usr/bin/env python3
import pyvisa
from time import sleep
def main():
    try:
        #rm = pyvisa.ResourceManager()  # Seems to do something, but cant write 
        rm = pyvisa.ResourceManager('@py')  # Use @py for pyvisa-py backend... works!
        #rm = pyvisa.ResourceManager('@ni')   #Error: 'IVIVisaLibrary' object has no attribute 'viParseRsrcEx'

        instruments = rm.list_resources()
        print(f"Available instruments: {instruments}")

....
`
# Connected instrument: USB0::6833::1230::DS1ZA253703047::0::INSTR
this says: the connection type is USB, vendorID,productID,Device,[IDK what 0 is],Instrument

what do you do when you have multiple devices? how do you know which device to send or recieve data from?
how do you know the commands list? lol. IDK that. I litteraly just got this working again.

Basic usage is that you connect to a resource, then read and write string commands. 
you may well see messages about firmware versions, or inappropriate string commands.
but they are also fairly easy to guess. .. oops I mean read the documentation. 





</pre>

