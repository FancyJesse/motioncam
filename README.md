MotionCam
========================================================================
[![status](https://img.shields.io/badge/Project%20Status-work--in--progress-green.svg)](#)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=jesus_andrade45%40yahoo%2ecom&lc=US&item_name=GitHub%20Projects&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

A quick project written in Python that utilizes a Raspberry-Pi and Camera to detect motion.
In short, it constantly captures images and compares the pixels' RGB values to identify motion. 
Once motion is detected, it logs the event and captures the image.
If consecutive images are captured, a video recording will occur.
User defines thresholds and other settings via **config.py**.


Prerequisites
------------------------------------------------------------------------
Raspberry-Pi with Camera Module

Python3


Installation
------------------------------------------------------------------------
Before the installation, be sure to update & upgrade your current packages
```
$ apt-get update && apt-get upgrade
```

Also be sure you have python-picamera library installed
```
$ apt-get install python-picamera
```

To download the MotionCam project use the following:

git
```
$ git clone https://github.com/FancyJesse/motioncam
```


Usage
------------------------------------------------------------------------
Before executing the program, review and adjust any settings with **config.py**

To execute the program, simply call **motioncam.py**
```
$ python3 ./motioncam.py
```

Ideally you will want the program to run in the background, enter the following command for this:
```
$ screen -d -m -S [screen-name] [application-to-run] 
```

View a list of screens currently running:
```
$ screen -ls
```

To reattach the screen use:
```
$ screen -r [screen-name]
```

The program will continue running until the storage limit, defined within **config.py**, is reached. 

You can view the captured images and logs found in the directories defined within **config.py** as well.


Release History
------------------------------------------------------------------------
* 0.3.2
	* Updated log directory check

* 0.3.1
	* Adjusted a few files

* 0.3.0
    * Initial Release


License
------------------------------------------------------------------------
See the file "LICENSE" for license information.


Authors
------------------------------------------------------------------------
idle-user
