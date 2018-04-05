IoT Solution with Up Square Grove Dev Kit
In this development, we connect Up Square Grove board to the Google Cloud Platform. Use the python scripts created to send data for rotary, light and temperature & humidity sensors to the Pub/Sub every two seconds. The Cloud Function Pub/Sub trigger picks up the message data that only contain sensor data and forward them to the Stackdriver Storage. From the Stackdriver page, we can create charts to show sensor data on graphs based on sensor data and time.

For LCD, button, and led modules, only data will be sent to PubSub.
Components

Up Square Grove IoT Dev Kit
Google Cloud 	Platform
Set Up Hardware (Step by Step)
   Install the Grove Pi+* board
On the UP²* board, locate the small white arrow. This indicates connector 1 on the board.
 
Line up pin 1 on the Grove Pi+ board with connector 1 on the UP² board, and carefully press down so that the pins on the Grove Pi+ board slide neatly into the connectors.
 
   Connect the Micro USB Cable to the UP²* Board
On the UP² board, locate the USB 3.0 Micro B port. The micro USB cable plugs into the left side of this port.
 
Plug the micro USB cable into the left side of the USB port on the UP² board.
 
Connect the micro USB cable to your host computer.
  
   Connect the Ethernet Cable to the UP²* Board 
Plug the Ethernet cable into the UP² board.
Note: The Ethernet cable must be plugged in before powering on your board in order for your board to get an IP address.

Plug the other end of the Ethernet cable into your router.
   Two ways to Access the Command Line on the Board
       Access the board using keyboard, mouse and monitor

Connect usb keyboard to the usb port on the board.
Connect the usb mouse to the usb port on board.
Connect the monitor to HDMI connection on the board
       Access the board using Minicom for serial connection
To find out which device port can be used for serial connection, please execute the dmesg command on your linux laptop right after your board is connected to your laptop via micro USB cable. Take a look at the last few lines of the dmesg log to find out which serial port can be used to connect the 

       $ dmesg

       [14441.553189] usb 1-6: Product: IoTplatform
       [14441.553196] usb 1-6: Manufacturer: Intel
       [14441.553204] usb 1-6: SerialNumber: 012345678
       [14441.555454] cdc_acm 1-6:1.0: ttyACM0: USB ACM device

Based on the above logs, the port to use is /dev/ttyACM0. This port is going to be used for serial connection to access the command line on the board from your computer.

Once your board is connected to your laptop via micro USB cable and the device port is determined, we can run the minicom setup (e.g. on Ubuntu): 

    $ sudo minicom -s
        we will now be presented with the following menu:
    +--------------------------------------------------------------------+                                                                                                                                                       
              +-----[configuration]------+                                     
            | Filenames and paths      |                                     
            | File transfer protocols  |                                     
            | Serial port setup        |                                     
            | Modem and dialing        |                                     
            | Save setup as dfl        |
            | Save setup as..          |
            | Exit                     |
            | Exit from Minicom        |
            +--------------------------+
 
Through which you can navigate using up/down keys. For our case, we will only need to setup Serial port setup so select that submenu. You will get the following menu:
       +-----------------------------------------------------------------------+
    | A -    Serial Device      : /dev/ttyACM0                              |
    | B - Lockfile Location     : /var/lock                                 |
    | C -   Callin Program      :                                           |
    | D -  Callout Program      :                                           |
    | E -    Bps/Par/Bits       : 115200 8N1                                |
    | F - Hardware Flow Control : Yes                                       |
    | G - Software Flow Control : No                                        |
    |                                                                       |
    |    Change which setting?                                              |
    +--------------------------------------------------------------------+
 
Now we can go back to the main menu by selecting Exit and pressing Enter. Optionally, you can save these settings as default for future use by selecting Save setup as dfl. When we exited the menu, the minicom terminal will open with our settings. Now when we power on the board we should see it booting:
   Power up your board
Plug the UP² board to its power supply and plug the power supply into an electrical outlet.
Note: If you need to turn off your board, you can do so by pressing the small white button next to the blue LED, or you can simply unplug the power cable.

Set Up Software for the Up Square Board
   Boot up the Ubuntu OS
After the board is powered and boot up, you should see the login screen below.


Enter “upsquared” for both login and password. Hit enter to continue. The screen below is an actual example of a successful login.





   OS Upgrade for the Up Square Board (Optional)

The Up Square Grove board comes pre-installed with Ubuntu 16.04 with only the command line is available. However, you can upgrade to latest version by running the the command “sudo apt update && sudo apt full-upgrade” on the board.

For graphical user interface version, you can to download OS image at https://downloads.up-community.org/download/up-squared-iot-grove-development-kit-ubuntu-16-04-server-image/. This documentation doesn’t cover the installation of  the graphical user version. Other than this, you should work fine moving on. 	 

	
   Firmware Upgrade for the Up Square Board (Optional)

You also can upgrade the firmware for the Up Square Board. The procedure to do a firmware update is available at the link https://wiki.up-community.org/Bios_Update.


Set up the IoT Projects

   Pre-requisite

Before setting up the project, an account with Google is needed to log into the Google Cloud Platform. Please register an account with Google if you don’t have it. Once an account is created successfully, log into the Google Cloud Platform and create a public and private key pair, a Pub/Sub topic, a Pub/Sub subscription, a device registry, a device.

Generate RSA Public and Private keys

Log into a box that can run shell scrips and use the commands below to create the private and self-signed public key and put the the keys in the folder “PemFiles”.

mkdir PemFiles
cd PemFiles
openssl req -x509 -newkey rsa:2048 -keyout rsa_private.pem -nodes -out rsa_cert.pem -subj "/CN=unused"

Create a Topic
1) Go to the Google Cloud Pub/Sub topics page in the GCP Console.
2) Click Create a topic.
3) Enter a unique Name for your topic.

Create a Subscription
1) Go to the Google Cloud Pub/Sub Subscriptions page in the GCP Console
2) Click New subscription.
3) Type a name for the subscription. Check the Pull box on the delivery type.
4) Click Create.

Create a Device Registry
1) Go to the Device registries page in GCP Console.
2) At the top of the page, click Create device registry.
3) Enter a Registry ID and select a cloud region.

Select both MQTT and HTTP protocols that devices in this registry will use to connect to Cloud IoT Core.

4) Select a Telemetry topic or create a new one. All device telemetry (the event data sent from devices to the cloud) will be published to the Cloud Pub/Sub topic you specify in this field.

Selecting the Device state topic or create a new one is optional. You can leave this one out.

Click Create to continue.


Create a Device
1) On the Registry Details page, click Add device.
2) Enter my-device for the Device ID.
3) Select Allow for Device communication.
4) On the Authentication section, click Add and select public key format RS256_X509. Copy the data from the public key file rsa_cert.pem in the PemFiles folder and paste onto the Public key value box.
5) Click Add to complete.

   Install middleware libraries for Up Square Board

After successfully logged into the Up Square board, you need to install the middle ware mraa and upm library packages so that we can write scripts to do certain tasks like turning on/off the leds, writing text to LCD, querying the sensors for data, and etc. Run the commands below:

sudo add-apt-repository ppa:mraa/mraa
sudo apt-get update
sudo apt-get install libmraa1 libmraa-dev libmraa-java python-mraa python3-mraa node-mraa mraa-tools swig
sudo apt-get install libupm-dev libupm-java python-upm python3-upm node-upm upm-examples


   Add Permissions to Access Devices on Up Square Grove Board

In /etc/rc.local file add the commands below:
chown -R root:gpio /sys/class/gpio 
chmod -R ug+rw /sys/class/gpio
chown -R root:leds /sys/class/leds
chmod -R ug+rw /sys/class/leds


In /etc/udev/rules.d folder, create files with names 99-leds.rules, 99-i2c.rules, 99-spi.rules and 99-gpio.rules. If any file already exist, leave it there. Copy the below contents to these files as instructed below.

In file 99-leds.rules, add
SUBSYSTEM=="leds", KERNEL=="upboard:*", ACTION=="add|change", RUN+="/usr/bin/find /sys$devpath -type f -exec /bin/chmod g+u {} + -exec /"

In file 99-i2c.rules, add
SUBSYSTEM=="i2c-dev", GROUP="i2c", MODE="0775"
SUBSYSTEM=="i2c-*", GROUP="i2c", MODE="0775"

In file 99-spi.rules, add
SUBSYSTEM=="spidev", GROUP="spi", MODE="0775"

In file 99-gpio.rules, add
SUBSYSTEM=="gpio", PROGRAM="/bin/sh -c '/bin/chown -R root:gpio /sys/devices/platform/INT3452:*/gpio'" 
SUBSYSTEM=="gpio", PROGRAM="/bin/sh -c '/bin/chmod -R 777 /sys/devices/platform/INT3452:*/gpio'"


   Set up IOT python scripts on the Up Square Board 
     
1. On Up Square Board, run commands below to download the iot script
    cd ~
    git clone https://github.com/khanhhale/UpSquaredGroveIotDevKit.git
2. Run “cd UpSquaredGroveIotDevKit”. 
3. In the sub folder PemFiles, please replace the private and public files with the ones you created in the guide section Generate RSA Public and Private keys off page 12. Now you’re ready to run the scripts inside.
            
	 	
    Create Stackdriver Account
Go to the Google Cloud Platform Console by clicking the following button:
Go to the GCP Console
Select the project you want to enable for Stackdriver in the drop-down menu at the top of the page. Alternatively, create a new GCP Console project to enable.
In the GCP Console navigation menu, select Stackdriver > Monitoring to go to the Stackdriver Monitoring Console. You should see the following dialog, with your project's name inserted:


If you do not see this dialog and instead see the Stackdriver home page for your project, then your project has already been enabled for Stackdriver and you are finished.
Select Create a new Stackdriver account and click Continue. You see the following dialog:

Verify that the project in the text box—your-project-000—is the one you want to enable. Alternatively, select another project by clicking the Close icon in the text box and then using the drop-down project menu.
Optional: You can also get to the Create a Stackdriver Account page by selecting Create Stackdriver account from the account drop-down menu at the top of the Stackdriver Monitoring Console.
When the correct project is selected, click Create Account in the Create a Stackdriver account page.
In the Add Google Cloud Platform projects page, click Continue. To add GCP projects later, see Monitoring multiple projects.
In the Add AWS accounts page, click Done. To add AWS accounts later, see Add an AWS account to a Stackdriver account.
You are given instructions for setting up the Stackdriver Monitoring agent on your VM instances.
You are asked to select an option for email reporting. You can change this setting in Account Settings page in the Stackdriver Monitoring Console.
You see a page that says Gathering Information. When this operation completes, click Launch Monitoring.
You see the Stackdriver Monitoring home page for your project.
    Setting up the Pub/Sub triggers function
1) Open the Cloud Function page in the GCP Console
2) Create Pub/Sub triggers function and update the index.js and package.json with the two files in the cloud functions folder.

3) Update the projectId and metricType variables with your own values.
4) Click save to deploy the Pubsub triggers function.

Send Light Sensor Data to GCP
Follow all set-up instructions above
Run “cd ~/UpSquaredGroveIotDevKit” on command line of the Up Square board
On the Grove board of the Up Square Grove Dev Kit, plug the female connector of the light sensor module into A0 male connector as shown in red circle below.

In the index.js file of the cloud functions on GCP change the value of the metricType variable as shown below: 
                                 const metricType = "custom.googleapis.com/cloudiot/lightsensors"
                       Then click on save button to save changes.
Run the command below after you replace the values on the right hand side right after the colon for the parameters project_id, registry_id, message_type, private_key_file, public_key_file and cloud_region with yours.
                                                                                                                                                                        sudo python lightsensor.py --project_id=cloud-iot-testing --registry_id=cloud-iot-registry --device_id=device-1 --message_type=event --algorithm=RS256 --private_key_file=/home/upsquared/ups_grove/PemFiles/rsa_private.pem --public_key_file=/home/upsquared/ups_grove/PemFiles/rsa_cert.pem --cloud_region=us-central1 --message_type=event --message_data_type=data_string

Send Rotary Sensor Data to GCP
Follow all set-up instructions above
Run “cd ~/UpSquaredGroveIotDevKiRun” on command line of the Up Square
On the Grove board of the Up Square Grove Dev Kit, plug the female connector of the rotary sensor module into A0 male connector as shown in red circle below.
	
In the index.js file of the cloud functions on GCP, change the value of the metricType variable as below: 
                     const metricType = "custom.googleapis.com/cloudiot/rotarysensors";
            Then click on save button to save changes.
Run the command below after you replace the values on the right hand side right after the colon for the parameters project_id, registry_id, message_type, private_key_file, public_key_file and cloud_region with yours.
                                                                                                                                                                        sudo python rotarysensor.py --project_id=cloud-iot-testing --registry_id=cloud-iot-registry --device_id=device-1 --message_type=event --algorithm=RS256 --private_key_file=/home/upsquared/ups_grove/PemFiles/rsa_private.pem --public_key_file=/home/upsquared/ups_grove/PemFiles/rsa_cert.pem --cloud_region=us-central1 --message_type=event --message_data_type=data_string

Send Temperature & Humidity Data to GCP
Follow all set-up instructions above
Run “cd ~/UpSquaredGroveIotDevKit” on command line of the Up Square board
On the Grove board of the Up Square Grove Dev Kit, plug the female connector of the rotary sensor module into i2c-2 male connector as shown in red circle below.

In the index.js file of the cloud functions on GCP, change the value of the metricType variable as shown below: 
                                const metricType = "custom.googleapis.com/cloudiot/thsensors";
                       Then click on save button to save changes.
Run the command below after you replace the values on the right hand side right after the colon for the parameters project_id, registry_id, message_type, private_key_file, public_key_file and cloud_region with yours.
                                                                                                                                                                        sudo python thsensor.py --project_id=cloud-iot-testing --registry_id=cloud-iot-registry --device_id=device-1 --message_type=event --algorithm=RS256 --private_key_file=/home/upsquared/ups_grove/PemFiles/rsa_private.pem --public_key_file=/home/upsquared/ups_grove/PemFiles/rsa_cert.pem --cloud_region=us-central1 --message_type=event --message_data_type=data_string

After the command is executed, the text “Button on/off status: 1” is sent to Pub/Sub while button is pressed and “Button on/off status: 0” is sent while the button is not pressed.

Send button click data to Pub/Sub
Follow all set-up instructions above
Run “cd ~/UpSquaredGroveIotDevKit” on command line of the Up Square board
On the Grove board of the Up Square Grove Dev Kit, plug the female connector of the button module into D4 male connector as shown in red circle below.

Run the command below after you replace the values on the right hand side right after the colon for the parameters project_id, registry_id, message_type, private_key_file, public_key_file and cloud_region with yours.
                                                                                                                                                                        sudo python button.py --project_id=cloud-iot-testing --registry_id=cloud-iot-registry --device_id=device-1 --message_type=event --algorithm=RS256 --private_key_file=/home/upsquared/ups_grove/PemFiles/rsa_private.pem --public_key_file=/home/upsquared/ups_grove/PemFiles/rsa_cert.pem --cloud_region=us-central1 --message_type=event --message_data_type=data_string

After the command is executed, the text “led: on” is sent to Pub/Sub while light is on and “led: off” is sent while the light is off.

Send led data to Pub/Sub
Follow all set-up instructions above
Run “cd ~/UpSquaredGroveIotDevKit” on command line of the Up Square board
On the Grove board of the Up Square Grove Dev Kit, plug the female connector of the led module into D3 male connector as shown in red circle below.

Run the command below after you replace the values on the right hand side right after the colon for the parameters project_id, registry_id, message_type, private_key_file, public_key_file and cloud_region with yours.
                                                                                                                                                                        sudo python led.py --project_id=cloud-iot-testing --registry_id=cloud-iot-registry --device_id=device-1 --message_type=event --algorithm=RS256 --private_key_file=/home/upsquared/ups_grove/PemFiles/rsa_private.pem --public_key_file=/home/upsquared/ups_grove/PemFiles/rsa_cert.pem --cloud_region=us-central1 --message_type=event --message_data_type=data_string

After the command is executed, the text “led: on” is sent to Pub/Sub while light is on and “led: off” is sent while the light is off.

Change LCD Text and Send it to Pub/Sub
Follow all set-up instructions above
Run “cd ~/UpSquaredGroveIotDevKit” on command line of the Up Square board
On the Grove board of the Up Square Grove Dev Kit, plug the female connector of the lcd module into i2c-2 male connector as shown in red circle below.
                        

Run the command below after you replace the values on the right hand side right after the colon for the parameters project_id, registry_id, message_type, private_key_file, public_key_file and cloud_region with yours.
                                                                                                                                                                        sudo python lcd.py --project_id=cloud-iot-testing --registry_id=cloud-iot-registry --device_id=device-1 --message_type=event --algorithm=RS256 --private_key_file=/home/upsquared/ups_grove/PemFiles/rsa_private.pem --public_key_file=/home/upsquared/ups_grove/PemFiles/rsa_cert.pem --cloud_region=us-central1 --message_type=event --message_data_type=data_string

After the command is executed, the Welcome text should be sent to Pub/Sub and the LCD should display Welcome text as shown below:

 
Create Dashboard and Charts on the Stackdriver Page

Create Dashboard

Log into GCP, click on “Monitoring” under STACKDRIVER section. You’ll be redirected to Stackdriver page
On the Stackdriver page, go to Dashboards -> Create Dashboard and click.

Create Chart for Rotary Sensor data
Complete the section Create Dashboard above
On the Stackdriver page, click on “Add Chart” on the upper right corner. An overlay will pop up.
Type “Global” for Resource Type
Choose custom.googleapis.com/cloudiot/rotarysensors for Metrics
Choose project for Filter and click on save button to create the chart.



Create Chart for Temperature and Humidity

Complete the section Create Dashboard above
On the Stackdriver page, click on “Add Chart” on the upper right corner. An overlay will pop up.
Type “Global” for Resource Type
Choose custom.googleapis.com/cloudiot/thsensors for Metrics
Choose project for Filter and click on save button to create the chart.



Create Chart for Light Sensor Data

Complete the section Create Dashboard above
On the Stackdriver page, click on “Add Chart” on the upper right corner. An overlay will pop up.
Type “Global” for Resource Type
Choose custom.googleapis.com/cloudiot/lightsensors for Metrics
Choose project for Filter and click on save button to create the chart.







