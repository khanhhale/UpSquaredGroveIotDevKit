https://downloads.up-community.org/download/up-squared-iot-grove-development-kit-ubuntu-16-04-server-image/


Note: this image is based on Ubuntu 16.04 Server. The Graphical User Interface is not pre-installed, but only the command line is available.

INSTALLATION

USB/CD/DVD BOOTABLE DEVICE SETUP

———————————————————————
Steps:

1. Insert blank USB device to be flashed with image and Clonezilla.

2. Download Tuxboot to flash Clonezilla image
(https://tuxboot.org/download/)

3. Run tool, check “Predownloaded 7zs” and select image file:
clonezilla-live-2.5.2-31-amd64-flasher-upboard-final.zip

4. Select USB device disk unit and press OK.

5. Extract USB device when finished.

UP^2 INSTALLATION: UBUNTU 16.04.3 SERVER
——————————————————————————–
Steps:

1. Insert bootable USB on blank UP^2 device.

2. Power on the board, Clonezilla splash screen should appear after a
few seconds.

3. After successful flashing, board will be powered off.

login using 
log-in: upsquared
password: upsquared


sudo cmake .. -DCMAKE_CXX_COMPILER=/usr/bin/g++ -DCMAKE_CC_COMPILER=/usr/bin/gcc
sudo rm -rf build; mkdir build; cd build
sudo make
sudo make install
sudo ln -s /usr/lib/python2.7/site-packages/* /usr/lib/python2.7/dist-packages

login

khanhl@khanhl-glaptop:~$ sudo minicom -s
[sudo] password for khanhl: 


Welcome to minicom 2.7.1

OPTIONS: I18n 
Compiled on Aug 13 2017, 15:25:34.
Port /dev/ttyACM0, 09:52:22

Press CTRL-A Z for help on special keys

3 LTS ubuntu ttyGS0                     

ubuntu login: upsquared
Password: upsquared
Last login: Fri Mar  9 11:41:38 EST 2018 on tty1
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.10.0-9-upboard x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

184 packages can be updated.
87 updates are security updates.


upsquared@ubuntu:~$


Install the firmware driver for up core wifi chip
To enable the up core wifi chip on ubuntu after adding our ppa and installing the up kernel as stated in the previous section, install the package

sudo apt install firmware-ampak-ap6214a
Install Intel graphic driver
Follow the instruction on the Intel graphics update tool page

https://01.org/linuxgraphics/downloads/update-tool
You can also install Intel graphics firmware from

https://01.org/linuxgraphics/downloads/firmware
Enable the HAT functionality from userspace
To be able to use the GPIO, PWM, SPI, I2C and uart functionality with a normal user we created a ubuntu package that set the correct permission.

NOTE: this could create security problem, do only if you know what are you doing

After adding our PPA you can install it with:

sudo apt install upboard-extras
after that you need to add the user that need to access the HAT functionality to the corresponding groups:

for example this command permit to the current user to access to the gpio functionality

sudo usermod -a -G gpio ${USER} or for user in upsquared root; do sudo usermod -a -G gpio "$user"; done
leds

sudo usermod -a -G leds ${USER} or for user in upsquared root; do sudo usermod -a -G leds "$user"; done
spi

sudo usermod -a -G spi ${USER} or for user in upsquared root; do sudo usermod -a -G spi "$user"; done
i2c

sudo usermod -a -G i2c ${USER} or for user in upsquared root; do sudo usermod -a -G i2c "$user"; done
uart

sudo usermod -a -G dialout ${USER}  or for user in upsquared root; do sudo usermod -a -G dialout "$user"; done

to apply the permission changes after issuing the previous command a reboot is needed

sudo reboot
Instruction for Legacy Ubuntu Version (only for up board)
Ubuntu 14.04 LTS (Trusty Tahr)
Install the latest Trusty release
From a terminal, add the UP board PPA
sudo add-apt-repository ppa:ubilinux/up
Update the package database:
sudo apt update
Install the upboard kernel package
sudo apt install linux-upboard-lts-xenial
Remove the other kernel ima


turn on leads
First, create a group and add the user that needs access to the GPIOs to it (this is for the current user; replace $USER with an explicit username if you want).

sudo groupadd gpio 
sudo usermod -a -G gpio $USER
Second, add the following lines to /etc/rc.local (you will have to edit it as root, using sudo vi or whatever).

chown -R root:gpio /sys/class/gpio 
chmod -R ug+rw /sys/class/gpio
Third, create a new udev rule in a file, say /etc/udev/rules.d/80-gpio-noroot.rules (you will have to edit it as root again):

# /etc/udev/rules.d/80-gpio-noroot.rules 
# Corrects sys GPIO permissions on the Joule so non-root users in the gpio group can manipulate bits
# Change group to gpio 
SUBSYSTEM=="gpio", PROGRAM="/bin/sh -c '/bin/chown -R root:gpio /sys/devices/platform/INT34D1:*/gpio'" 
# Change user permissions to ensure user and group have read/write permissions 
SUBSYSTEM=="gpio", PROGRAM="/bin/sh -c '/bin/chmod -R ug+rw /sys/devices/platform/INT34D1:*/gpio'"
Fourth, reboot or restart udev using

add to /etc/udev/rules.d/99-i2c.rules
SUBSYSTEM=="i2c-*", GROUP="i2c", MODE="0660"


sudo udevadm trigger --subsystem-match=gpio
And finally test:

mmraa-gpio set 1 1
mraa-gpio set 100 1 
mraa-gpio set 100 0

detect bus
mraa-i2c

service udev restart
and
udevadm control --reload-rules


Initial Software Setup
# Install some additional software packages
sudo apt-get update
sudo apt-get install -y git python-smbus
# Download the GrovePi software, complete with Python script modifications for UP
git clone -b up-board https://github.com/emutex/GrovePi.git

BIOS Setup
The GrovePi+ supports a maximum I2C bus speed of 100kHz. By default, the UP board uses 400kHz, but this can be changed easily in the BIOS as follows:

Power up (or reboot) the UP board
Press the 'Del' key on the keyboard during boot-up to enter the BIOS configuration menu
If prompted for a password, just press 'Enter'
Press the 'right-arrow' key to move to the Advanced tab.
Select the 'HAP Configuration' menu, then press 'Enter'
Select the 'I2C #2 Speed' menu, then press 'Enter'
Select the '100KHz' option, then press 'Enter'
Press 'F4', then select 'Yes' and press 'Enter' to save the settings and exit
Boot to ubilinux
Blink an LED
Connect a Grove LED to the connector labelled D4 on the GrovePi+
Run the following script
python GrovePi/Software/Python/grove_led_blink.py
The LED should now blink slowly. Press Ctrl-C to stop the script

Read temperature and humidity
Connect the Grove Temperature and Humidity Sensor (blue colour) to the connector labelled D4 on the GrovePi+
Run the following script
python GrovePi/Software/Python/grove_dht_pro.py



after successful login above, you need to install the middle ware mraa for to program the board to do certain task like turning on/off the leds, query the sensors, and etc...

Here is a PPA for installing on ubuntu: https://launchpad.net/~mraa/+archive/ubuntu/mraa

sudo add-apt-repository ppa:mraa/mraa
sudo apt-get update
sudo apt-get install libmraa1 libmraa-dev libmraa-java python-mraa python3-mraa node-mraa mraa-tools swig



-------------------------------------------------------
upsquared@ubuntu:~$ sudo add-apt-repository ppa:mraa/mraa
 mraa
 More info: https://launchpad.net/~mraa/+archive/ubuntu/mraa
Press [ENTER] to continue or ctrl-c to cancel adding it

gpg: keyring `/tmp/tmply4df8ve/secring.gpg' created
gpg: keyring `/tmp/tmply4df8ve/pubring.gpg' created
gpg: requesting key 39B88DE4 from hkp server keyserver.ubuntu.com
gpg: /tmp/tmply4df8ve/trustdb.gpg: trustdb created
gpg: key 39B88DE4: public key "Launchpad PPA for mraa" imported
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)
OK
upsquared@ubuntu:~$ sudo apt-get update
Get:1 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB]
Hit:2 http://us.archive.ubuntu.com/ubuntu xenial InRelease                
Get:3 http://us.archive.ubuntu.com/ubuntu xenial-updates InRelease [102 kB]
Hit:4 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial InRelease
Get:5 http://us.archive.ubuntu.com/ubuntu xenial-backports InRelease [102 kB]  
Hit:6 http://ppa.launchpad.net/ubilinux/up/ubuntu xenial InRelease             
Get:7 http://security.ubuntu.com/ubuntu xenial-security/main amd64 Packages [464 kB]
Get:8 http://us.archive.ubuntu.com/ubuntu xenial-updates/main amd64 Packages [742 kB]
Get:9 http://security.ubuntu.com/ubuntu xenial-security/main i386 Packages [418 kB]
Get:10 http://us.archive.ubuntu.com/ubuntu xenial-updates/main i386 Packages [689 kB]
Get:11 http://security.ubuntu.com/ubuntu xenial-security/main Translation-en [200 kB]
Get:12 http://us.archive.ubuntu.com/ubuntu xenial-updates/main Translation-en [308 kB]
Get:13 http://security.ubuntu.com/ubuntu xenial-security/universe amd64 Packages [323 kB]
Get:14 http://us.archive.ubuntu.com/ubuntu xenial-updates/universe amd64 Packages [601 kB]
Get:15 http://security.ubuntu.com/ubuntu xenial-security/universe i386 Packages [282 kB]
Get:16 http://us.archive.ubuntu.com/ubuntu xenial-updates/universe i386 Packages [557 kB]
Get:17 http://security.ubuntu.com/ubuntu xenial-security/universe Translation-en [121 kB]
Get:18 http://security.ubuntu.com/ubuntu xenial-security/multiverse amd64 Packages [3,208 B]
Get:19 http://security.ubuntu.com/ubuntu xenial-security/multiverse i386 Packages [3,376 B]
Get:20 http://us.archive.ubuntu.com/ubuntu xenial-updates/universe Translation-en [243 kB]
Get:21 http://us.archive.ubuntu.com/ubuntu xenial-updates/multiverse amd64 Packages [16.2 kB]
Get:22 http://us.archive.ubuntu.com/ubuntu xenial-updates/multiverse i386 Packages [15.3 kB]
Get:23 http://us.archive.ubuntu.com/ubuntu xenial-backports/universe amd64 Packages [7,084 B]
Get:24 http://us.archive.ubuntu.com/ubuntu xenial-backports/universe i386 Packages [7,060 B]
Fetched 5,306 kB in 2s (1,919 kB/s)                    
Reading package lists... Done
n-mraa python3-mraa node-mraa mraa-tools libmraa1 libmraa-dev libmraa-java pytho 
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following packages will be upgraded:
  libmraa-dev libmraa-java libmraa1 mraa-tools node-mraa python-mraa
  python3-mraa
7 upgraded, 0 newly installed, 0 to remove and 103 not upgraded.
Need to get 516 kB of archives.
After this operation, 81.9 kB of additional disk space will be used.
Get:1 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 libmraa-java amd64 1.9.0-1 [56.6 kB]
Get:2 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 node-mraa amd64 1.9.0-1 [247 kB]
Get:3 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 libmraa-dev amd64 1.9.0-1 [27.8 kB]
Get:4 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 libmraa1 amd64 1.9.0-1 [63.6 kB]
Get:5 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 mraa-tools amd64 1.9.0-1 [9,950 B]
Get:6 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 python-mraa amd64 1.9.0-1 [59.0 kB]
Get:7 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 python3-mraa amd64 1.9.0-1 [51.4 kB]
Fetched 516 kB in 4s (127 kB/s)                     
(Reading database ... 70904 files and directories currently installed.)
Preparing to unpack .../libmraa-java_1.9.0-1_amd64.deb ...
Unpacking libmraa-java (1.9.0-1) over (1.8.0-1) ...
Preparing to unpack .../node-mraa_1.9.0-1_amd64.deb ...
Unpacking node-mraa (1.9.0-1) over (1.8.0-1) ...
Preparing to unpack .../libmraa-dev_1.9.0-1_amd64.deb ...
Unpacking libmraa-dev (1.9.0-1) over (1.8.0-1) ...
Preparing to unpack .../libmraa1_1.9.0-1_amd64.deb ...
Unpacking libmraa1 (1.9.0-1) over (1.8.0-1) ...
Preparing to unpack .../mraa-tools_1.9.0-1_amd64.deb ...
Unpacking mraa-tools (1.9.0-1) over (1.8.0-1) ...
Preparing to unpack .../python-mraa_1.9.0-1_amd64.deb ...
Unpacking python-mraa (1.9.0-1) over (1.8.0-1) ...
Preparing to unpack .../python3-mraa_1.9.0-1_amd64.deb ...
Unpacking python3-mraa (1.9.0-1) over (1.8.0-1) ...
Processing triggers for libc-bin (2.23-0ubuntu10) ...
Setting up libmraa1 (1.9.0-1) ...
Setting up libmraa-java (1.9.0-1) ...
Setting up node-mraa (1.9.0-1) ...
Setting up libmraa-dev (1.9.0-1) ...
Setting up mraa-tools (1.9.0-1) ...
Setting up python-mraa (1.9.0-1) ...
Setting up python3-mraa (1.9.0-1) ...
Processing triggers 
--------------------------------------------------------

install upm
sudo add-apt-repository ppa:mraa/mraa
sudo apt-get update
sudo apt-get install libupm-dev libupm-java python-upm python3-upm node-upm upm-examples

upsquared@ubuntu:~/ups_grove$ sudo add-apt-repository ppa:mraa/mraa
[sudo] password for upsquared: 
 mraa
 More info: https://launchpad.net/~mraa/+archive/ubuntu/mraa
Press [ENTER] to continue or ctrl-c to cancel adding it

gpg: keyring `/tmp/tmpdfmchmqn/secring.gpg' created
gpg: keyring `/tmp/tmpdfmchmqn/pubring.gpg' created
gpg: requesting key 39B88DE4 from hkp server keyserver.ubuntu.com
gpg: /tmp/tmpdfmchmqn/trustdb.gpg: trustdb created
gpg: key 39B88DE4: public key "Launchpad PPA for mraa" imported
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)
OK
upsquared@ubuntu:~/ups_grove$ sudo apt-get update
Get:1 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB]
Hit:2 http://us.archive.ubuntu.com/ubuntu xenial InRelease                
Get:3 http://us.archive.ubuntu.com/ubuntu xenial-updates InRelease [102 kB]
Hit:4 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial InRelease
Get:5 http://us.archive.ubuntu.com/ubuntu xenial-backports InRelease [102 kB]  
Hit:6 http://ppa.launchpad.net/ubilinux/up/ubuntu xenial InRelease             
Get:7 http://security.ubuntu.com/ubuntu xenial-security/main amd64 Packages [464 kB]
Get:8 http://us.archive.ubuntu.com/ubuntu xenial-updates/main amd64 Packages [742 kB]
Get:9 http://security.ubuntu.com/ubuntu xenial-security/main i386 Packages [418 kB]
Get:10 http://us.archive.ubuntu.com/ubuntu xenial-updates/main i386 Packages [689 kB]
Get:11 http://us.archive.ubuntu.com/ubuntu xenial-updates/universe amd64 Packages [602 kB]
Get:12 http://us.archive.ubuntu.com/ubuntu xenial-updates/universe i386 Packages [557 kB]
Fetched 3,778 kB in 2s (1,658 kB/s)                                            
Reading package lists... Done
-upm python3-upm node-upm upm-examples-get install libupm-dev libupm-java python 
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following additional packages will be installed:
  libupm1
The following NEW packages will be installed:
  libupm-java node-upm python-upm python3-upm
The following packages will be upgraded:
  libupm-dev libupm1 upm-examples
3 upgraded, 4 newly installed, 0 to remove and 99 not upgraded.
Need to get 31.7 MB of archives.
After this operation, 215 MB of additional disk space will be used.
Do you want to continue? [Y/n] y
Get:1 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 libupm-dev amd64 1.6.0-1 [363 kB]
Get:2 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 libupm1 amd64 1.6.0-1 [635 kB]
Get:3 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 libupm-java amd64 1.6.0-1 [2,874 kB]
Get:4 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 node-upm amd64 1.6.0-1 [20.3 MB]
Get:5 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 python-upm amd64 1.6.0-1 [3,652 kB]
Get:6 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 python3-upm amd64 1.6.0-1 [3,631 kB]
Get:7 http://ppa.launchpad.net/mraa/mraa/ubuntu xenial/main amd64 upm-examples all 1.6.0-1 [207 kB]
Fetched 31.7 MB in 2min 9s (245 kB/s)                                          
(Reading database ... 72233 files and directories currently installed.)
Preparing to unpack .../libupm-dev_1.6.0-1_amd64.deb ...
Unpacking libupm-dev (1.6.0-1) over (1.5.0-1.1) ...
Preparing to unpack .../libupm1_1.6.0-1_amd64.deb ...
Unpacking libupm1 (1.6.0-1) over (1.5.0-1.1) ...
Selecting previously unselected package libupm-java.
Preparing to unpack .../libupm-java_1.6.0-1_amd64.deb ...
Unpacking libupm-java (1.6.0-1) ...
Selecting previously unselected package node-upm.
Preparing to unpack .../node-upm_1.6.0-1_amd64.deb ...
Unpacking node-upm (1.6.0-1) ...
Selecting previously unselected package python-upm.
Preparing to unpack .../python-upm_1.6.0-1_amd64.deb ...
Unpacking python-upm (1.6.0-1) ...
Selecting previously unselected package python3-upm.
Preparing to unpack .../python3-upm_1.6.0-1_amd64.deb ...
Unpacking python3-upm (1.6.0-1) ...
Preparing to unpack .../upm-examples_1.6.0-1_all.deb ...
Unpacking upm-examples (1.6.0-1) over (1.5.0-1.1) ...
Processing triggers for libc-bin (2.23-0ubuntu10) ...
Setting up libupm1 (1.6.0-1) ...
Setting up libupm-dev (1.6.0-1) ...
Setting up libupm-java (1.6.0-1) ...
Setting up node-upm (1.6.0-1) ...
Setting up python-upm (1.6.0-1) ...
Setting up python3-upm (1.6.0-1) ...
Setting up upm-examples (1.6.0-1) ...
Processing triggers for libc-bin (2.23-0ubuntu10) ...



Look for usb drive on this system

upsquared@ubuntu:~$ dmesg
[    0.000000] Linux version 4.10.0-9-upboard (root@ubilinux-build) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.5) ) #11~16.04.1 SMP Wed Oct 25 17:10:46 IST 2017 (Ubuntu 4.10.0-9.11~16.04.1-upboard 4.10.0)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-4.10.0-9-upboard root=UUID=6343855a-e936-408e-9afb-f16960f684b1 ro
.
.
.
[  306.632292] usb 2-4: Manufacturer: Samsung
[  306.632293] usb 2-4: SerialNumber: 0330218010038154
[  306.805329] usb-storage 2-4:1.0: USB Mass Storage device detected
[  306.810742] scsi host2: usb-storage 2-4:1.0
[  306.810910] usbcore: registered new interface driver usb-storage
[  306.815055] usbcore: registered new interface driver uas
[  308.003461] scsi 2:0:0:0: Direct-Access     Samsung  Flash Drive DUO  1100 PQ: 0 ANSI: 6
[  308.004890] sd 2:0:0:0: Attached scsi generic sg0 type 0
[  308.005505] sd 2:0:0:0: [sda] 125337600 512-byte logical blocks: (64.2 GB/59.8 GiB)
[  308.005943] sd 2:0:0:0: [sda] Write Protect is off
[  308.005945] sd 2:0:0:0: [sda] Mode Sense: 43 00 00 00
[  308.006374] sd 2:0:0:0: [sda] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
[  308.010187]  sda: sda1
[  308.012023] sd 2:0:0:0: [sda] Attached SCSI removable disk
[  347.494139] perf: interrupt took too long (3176 > 3165), lowering kernel.perf_event_max_sample_rate to 62750

See the third to last line shows that the drive is sda, so we will use /dev/sda1 as usb device.

Create a new folder to mount the usb device to.
mkdir /media/usbdrive

mount the device to /media/usbdrive folder
sudo mount '/dev/sda1' /media/usbdrive

verify that folder is mounted with the content of the usb drive
sudo ls -lrt  /media/usbdrive folder

when it does it should have something as below:

upsquared@ubuntu:~$ sudo mount '/dev/sda1' /media/usbdrive                                                                                                                                                                                    
upsquared@ubuntu:~$ sudo ls -lrt /media/usbdrive
total 32
drwxr-xr-x 5 root root 32768 Mar 16 21:09 ups_grove


copy the content of the usb drive to user home folder 
cp /media/usbdrive/ups_grove ~/

do ls -lrt and you should see below

upsquared@ubuntu:~/ups_grove$ pwd
/home/upsquared/ups_grove
upsquared@ubuntu:~/ups_grove$ ls -lrt
total 128
-rwxr-xr-x 1 upsquared upsquared  2438 Mar 19 13:17 Main.py
-rwxr-xr-x 1 upsquared upsquared  1623 Mar 19 13:17 Utility.pyc
-rwxr-xr-x 1 upsquared upsquared  2432 Mar 19 13:17 sensor.py
-rwxr-xr-x 1 upsquared upsquared 20087 Mar 19 13:17 CloudApis.pyc
-rwxr-xr-x 1 upsquared upsquared  2212 Mar 19 13:17 pwm.py
-rwxr-xr-x 1 upsquared upsquared  1255 Mar 19 13:17 Installation
-rwxr-xr-x 1 upsquared upsquared  2319 Mar 19 13:17 Gpio.py
-rwxr-xr-x 1 upsquared upsquared  2438 Mar 19 13:17 Blink.py
-rwxr-xr-x 1 upsquared upsquared  1562 Mar 19 13:17 Utility.py
-rwxr-xr-x 1 upsquared upsquared  5799 Mar 19 13:17 ServiceApi.pyc
-rwxr-xr-x 1 upsquared upsquared  4944 Mar 19 13:17 ServiceApi.py
-rwxr-xr-x 1 upsquared upsquared  2114 Mar 19 13:17 lcd.py
-rwxr-xr-x 1 upsquared upsquared  2082 Mar 19 13:17 debugSerial.py
-rwxr-xr-x 1 upsquared upsquared 11358 Mar 19 13:17 LICENSE
-rwxr-xr-x 1 upsquared upsquared     0 Mar 19 13:17 __init__.py
-rwxr-xr-x 1 upsquared upsquared   502 Mar 19 13:17 doc
-rwxr-xr-x 1 upsquared upsquared 21418 Mar 19 13:17 CloudApis.py
drwxr-xr-x 2 upsquared upsquared  4096 Mar 19 13:17 log
drwxr-xr-x 2 upsquared upsquared  4096 Mar 19 13:17 PemFiles
drwxr-xr-x 2 upsquared upsquared  4096 Mar 19 13:17 files

cd into the folder 
cd /home/upsquared/ups_grove

INSTALLATION
pip install --upgrade pip
sudo apt-get intall python-tk python-qt4 libi2c-dev python-serial
sudo pip install google-cloud oauth2client apiclient google-api-python-client cryptography requests python-dateutil

mraa-gpio list
list all pins

check pin
ls -lrt /sys/lass/gpio

turn on pin 31
sudo mraa-gpio set 0 1


Using the subplatform API
Using the subplatform API is relatively simple, simply add '512', the platform offset, to any IO calls.

Example:

D3 becomes GPIO 512 + 3 = 515
A2 becomes pin 512 + 2 = 514
Keep in mind that the I2C ports on the GrovePi shield are merely a level shifted extension of the carrier board's I2C bus, hence I2C sensors do not require an offset.

The API works from UPM or mraa in any of the supported languages and is compiled with mraa by default. Multiple subplatforms are not yet supported.

scan and find address of i2c bus
sudo i2cdetect -y 1.

install i2c tool
apt-get install i2c-tools

check
i2cdetect -F 1


I want to use the GrovePi+ on my new UP Squared Board. But I could not find the i2c address of the board(0x04 ) with commands from "i2cdetect -y -r 0" to "i2cdetect -y -r 7".

Then I found the wiki up-community.org/wiki/GrovePi said that I had to set I2C speed to 100K. But I could not find 'I2C #2 Speed' in my new UPA1AM18 BIOS. What should I do now? I am looking forward to your help. Thanks.

change premission
sudo chmod -R 777 /sys/class/gpio

ls /sys/bus/pci/devices/*/i2c_designware.0/ | grep i2c
$ sudo apt install i2c-tools
$ sudo i2cdetect -y -r 4

sudo python i2cscanner.py
scan and find address of i2c bus
sudo i2cdetect -y 1.
0x37 x
0x3a x
0x4a
0x4b
0x50 x


for((i=1;i<=11;i++)); do sudo chmod 777 "/dev/i2c-$i"; done

write data to bus i2c
i2cset -y 0 0x40 0x03 0x11 
read from i2c
sudo i2cget -y 1 0x40 0x01 b


  I2CBUS is an integer or an I2C bus name
  ADDRESS is an integer (0x03 - 0x77)
  MODE is one of:
    b (read byte data, default)
    w (read word data)
    c (write byte/read byte)
    Append p for SMBus PEC

verify
i2cdump -y 1 0x3e b - works

add i2c-dev to enable third party module
/etc/modules

list modules
 lsmod | sort -k 1

To load a module, and any modules that it depends on, use modprobe:

modprobe st
To remove a loaded module, use rmmod:

rmmod st
To view information about a module, use modinfo:

modinfo st



Blacklisting Modules
For various reasons it may be desirable to stop a module from loading. In this case a module can be blacklisted in /etc/modprobe.d/blacklist

nano -w /etc/modprobe.d/blacklist
for example the line

blacklist e100
should be added to prevent the 'e100' module (one of many Ethernet modules) from loading.

Sometimes it is needed to update the drivers cache after editing the blacklist.conf file. To do this, run:

sudo update-initramfs -u

http://wiki.seeed.cc/Grove-TemptureAndHumidity_Sensor-High-Accuracy_AndMini-v1.0/

install setup tools for:
sudo python -m pip install --upgrade pip setuptools
sudo apt-get install python-numpy
sudo pip install RPi.GPIO

For blinking test
For blink.py, run the command below to make led blinking and send message to the cloud.
python blink.py --project_id=cloud-iot-testing-185623 --registry_id=cloud-iot-registry2 --device_id=device-3 --message_type=event --algorithm=RS256 --private_key_file=/home/upsquared/ups_grove/PemFiles/rsa_private.pem --public_key_file=/home/upsquared/ups_grove/PemFiles/rsa_cert.pem --credential=/home/upsquared/ups_grove/PemFiles/cloud-iot-testing-052b9ca41b45.json --cloud_region=us-central1 --message_type=event --message_data_type=data_string --message="user1 has led trigger set to heartbeat"


strace -ff -s 256 python Main.py --project_id=cloud-iot-testing-185623 --registry_id=cloud-iot-registry2 --device_id=device-3 --message_type=event --algorithm=RS256 --private_key_file=/home/upsquared/ups_grove/PemFiles/rsa_private.pem --public_key_file=/home/upsquared/ups_grove/PemFiles/rsa_cert.pem --credential=/home/upsquared/ups_grove/PemFiles/cloud-iot-testing-052b9ca41b45.json --cloud_region=us-central1 --message_type=event --message_data_type=data_string --message="sending upsquared data 3 for upsquared kit"




Copy the examples to 96Boards CE
Build the C/C++ examples:
$ gcc mraa_gpio.c -o gpio_c
$ g++ mraa_gpio.cpp -o gpio_c++
Execute the examples:
$ sudo ./gpio_c
$ sudo ./gpio_c++
$ sudo python mraa_gpio.py


i2cdump -y 1 0x29 b



firmware update
sudo apt-get install avrdude


bios update
download firmware 3.3
sudo apt update && sudo apt full-upgrade


mkdir build
cd build
cmake ..
make
make install
sudo apt install cmake
sudo apt-get install pkg-config

cd ~/upm/build
sudo apt install cmake



sudo python Main.py --project_id=cloud-iot-testing-185623 --registry_id=cloud-iot-registry2 --device_id=device-2 --message_type=event --algorithm=RS256 --private_key_file=/home/upsquared/ups_grove/PemFiles/rsa_private.pem --public_key_file=/home/upsquared/ups_grove/PemFiles/rsa_cert.pem --credential=/home/upsquared/ups_grove/PemFiles/cloud-iot-testing-052b9ca41b45.json --cloud_region=us-central1 --message_type=event --message_data_type=data_string



add to /etc/rc.local
chown -R root:gpio /sys/class/gpio 
chmod -R ug+rw /sys/class/gpio

chown -R root:leds /sys/class/leds
chmod -R ug+rw /sys/class/leds

add to ls -lrt /etc/udev/rules.d files
for file 99-leds.rules, add
SUBSYSTEM=="leds", KERNEL=="upboard:*", ACTION=="add|change", RUN+="/usr/bin/find /sys$devpath -type f -exec /bin/chmod g+u {} + -exec /"

99-i2c.rules
SUBSYSTEM=="i2c-dev", GROUP="i2c", MODE="0775"
SUBSYSTEM=="i2c-*", GROUP="i2c", MODE="0775"

99-spi.rules
SUBSYSTEM=="spidev", GROUP="spi", MODE="0775"

99-gpio.rules
SUBSYSTEM=="gpio", PROGRAM="/bin/sh -c '/bin/chown -R root:gpio /sys/devices/platform/INT3452:*/gpio'" 
SUBSYSTEM=="gpio", PROGRAM="/bin/sh -c '/bin/chmod -R 777 /sys/devices/platform/INT3452:*/gpio'"



