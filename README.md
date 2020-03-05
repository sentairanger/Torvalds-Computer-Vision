# Torvalds-Computer-Vision

## Overview of the project

This was originally a project I did based on the tutorial by Danny Staple in the Magpi magazine issue 90. [Here](https://magpi.raspberrypi.org/articles/add-navigation-to-a-low-cost-robot) is a link for more information. However I must make this clear that I decided to change things here as well as correcting some of the errors in his code. Yes there were a few errors I had to correct and I also used different processses to get things running. This later evolved into an object detection robot after successfully installing Openvino on my Pi 3B+ and purchasing the Intel NCS2. So what this project shows is how you can use deep learning and AI to add more functionality to your projects. Not to mention this shows how my project evolved with the skills I obtained in the Edge AI fundamentals course thanks to Udacity.

### Needed Items

To get things started I had my Raspberry Pi Robot which uses the Devastator Tank Mobile Platform from DFRobot. I had a Pi Zero W as well as a generic USB power supply, 6 AA batteries and two HDD LEDs and LED bezels for eyes. For the motor controller I used the one included with the CamJam Edukit 3. I had a Pi Camera mounted on a 3D printed mount. To get things started I had to install OpenCV using the instructions from the link above. However, that did change with the installation of Openvino on the Pi.

### Getting everything running

Note: the Pi Camera must be enabled using `sudo raspi-config` or go to Preferences > Raspberry Pi Configuration > Interfaces. Under the Interfaces menu, click on Enable on the Camera section. After everything was set up I connected a monitor and bluetooth keyboard/mouse controller to get the code running. Every time I ran any code I had to invoke the `export LD_PRELOAD=/usr/lib/arm-linux_gnueabihf/libatomic.so` variable because otherwise it would not run. Now if you compiled OpenCV this would not be needed. Also note that if you are going to install the headless version of OpenCV make sure you only install it on CLI environment not a GUI one. I did that and it kept giving me issues until I uninstalled and replaced it with the correct version. So here is what each piece of code does and how to run it. I will add more to this as time goes by:

* `contours.py` takes three images of what it sees and outputs them as `with-contours.jpg`, `masked.jpg` and `original.jpg`. The masked image is in black and white and masks the color that it sees. The contours image is the image that draws a green line on the color itself. The `contours_big.jpg` and `masked_big.jpg` images are examples you can reference. To run it, type `python3 contours.py` or `python contours.py ` if you are running a virtual environment. If you did not compile OpenCV and you used Danny Staple's instructions from the link provided please export the LD_PRELOAD variable first.

![Masked photo](https://github.com/sentairanger/Torvalds-Computer-Vision/blob/master/masked_big.png)

![Contour photo](https://github.com/sentairanger/Torvalds-Computer-Vision/blob/master/contours_big.png)

* `devastator_nav.py` import the `get_saturated_colors` and the `camera_setup` functions to set things up. The robot takes constant images to see what color it gets from the `found_color` variable and if it sees yellow, the robot turns left. If it sees blue, it turns right. Otherwise, it just keeps moving forward. To run it, type `python3 devastator_nav.py` or `python devastator_nav.py` if you are using a virtual environment. Also, make sure your floor is of a neutral color and that you have white walls for a background for it to work effectively. Also, good lighting helps. Also, please make sure that both `contours.py` and `devastator_nav.py` are in the same directory or it won't work. 

* `devastator_detection.py` and `devastator_detection_triple.py` are similar, except the latter uses red from the color wheel. To run either, follow the same instructions as with the `devastator_nav.py` code. What happens with the first code is that when it sees yellow it turns left and when it sees blue it turns right. This is just like the previous code I mentioned. However, if it doesn't see either, it does not move. So consider this a color detection robot. To run this experiment I used red, blue and yellow foam balls attached to dowels to get the robot to see the color. In the second code, when it sees red it moves forward. I reference the color wheel to find the ranges of red. As before, make sure that `contours.py` is in the same directory as these two programs. 


### Video Demo

I added a video demo to the repo, but you will have to click on it to see it due to its file size. I added another video and a GIF of the robot running with the NCS2.

### Note on running this with other hardware

If you are running this with any other hardware, make sure you adjust accordingly. Example, if you use an L298N as opposed to the motor controller from CamJam Edukit 3, make sure you change the import to `from gpiozero import Robot` and then set the Robot equal to `Robot(left=(pin1, pin2), right=(pin3, pin4))` where pin1 through pin4 are the pin numbers you choose. If your controller board as its own python library please make reference of it. Otherwise, just use the Robot module from gpiozero. Also if you prefer to use another Pi make sure to give it proper power. If you plan to use a UBEC (Universal Battery Eliminator Circuit), be sure to connect things properly otherwise it will not work. 

### Expanding to other colors
Let me give you an example on how to modify the code to use other colors besides red, blue and yellow. Let's say I want to add green and I want the robot to move right and then left. I would add these lines after line 22 of `devastator_detection_triple.py`. 

```python
elif 90 < found_color[0] < 150:
    print("green")
    devastator_robot.right()
    sleep(1)
    devastator_robot.left()
    sleep(1)
```
This can also be done in `devastator_nav.py` and `devastator_detection.py`. To explain, `found_color[0]` picks the first part of the array, since OpenCV formats colors in BGR format. A distance sensor can also be added to the robot to make it into an obstacle avoidance robot, but this time avoiding certain colors. 

### Using an Intel NCS2 with the robot

After my successful tests using color detection, after much thought I decided to integrate deep learning and AI into my project as I should have done since the beginning. I first followed the [Pyimagesearch](https://www.pyimagesearch.com/2019/04/08/openvino-opencv-and-movidius-ncs-on-the-raspberry-pi/) guide to install Openvino on my Pi 3B+ and also purchased the Intel Neural compute stick 2 for this project. 

I used the Pi 3B+ because compiling Openvino and OpenCV took less time and I did not want to wait so long to compile it with the Pi Zero W. I did ask and yes you can install Openvino on the Pi Zero W despite it being an ARMv6 board. I also used a 5V 3A USB power bank to run the robot as I needed enough power to run the motors, the Pi and the Pi Camera. I connected the CamJam Edukit 3 motor controller board like before and I also attached the Pi Camera in the MIPI CSI port. I also mounted it on the same 3D printed camera mount. However, I used a piece of plasticard to mount the Pi on the camera mount. Then, I connected the HDD LED eyes. One LED connects to ground and the 3.3V pin. The second pin connects to Pin 25 and ground as well. You can use any LED you want, and any GPIO pin you want as long as you modify the pin numbering. The program uses MobileNetSSD object detection. And through several classes, if it sees the person class, the robot moves forward. However, this will be improved as object detection is very sensitive here and did cause my robot to stop and go and stop and go. So there will be improvements to add better accuracy. Before running the code I had to make sure to source the Openvino environment by running `source ~/openvino/bin/setupvars.sh`. Since I had installed `virtualenv` via `$ sudo pip install virtualenv` I created my environment using the command `virtualenv -p python3 venv` which creates a python3 environment named venv. I then ran `source venv/bin/activate` to turn on the environment. Now, to run the code you must type the following `python openvino_real_time_object_detection_robot.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel`. If you are not in a virtual environment change python to python3. This can be modified to have the robot move left if it sees a cat and right if it sees a chair. The result can be seen in the GIF and the video demo listed on the Repo.

Here's a rundown of the arguments that must be run for it to work:

* `--prototxt`: This is the prototext that must be used with the program. In this case I'm using the `MobileNetSSD_deploy.prototxt'.
* `--model`: This the model that is required. In this case, I'm using the `MobileNetSSD_deploy.caffemodel` model.

Optional arguments include:
* `--confidence`: This is the confidence threshold. It is set to 0.2 by default.
* `--movidius`: This is a boolean variable to determine if the Movidius NCS2 will be used. It is set to zero by default.

I have included the `.caffemodel` and `.prototxt` files to make things easier for future users. 

To run this on your own, make sure you have your own robot built and you can modify it however you want. The principle functionality will stay the same. Make sure that you install OpenVino on whatever Pi you use and that you have the Intel NCS2 as well. Also, make sure you have a python environment to protect your main system python. So here are the steps to take:

* Assemble robot and add Intel NC2 to a USB port on the Pi. Any robot will be able to work with this as long as it has a motor controller, 2 or more motors, a power supply for the pi, a power supply for the motors and a chassis. You can use any robot you want as long as you are able to mount the Pi Camera. Also, I recommend using a Pi 3, Pi 3B+, or a Pi 3A+. You can use a Pi 4 if you want but make sure you supply enough power to it and that it has sufficient cooling. 
* Make sure that Raspbian is installed on your Pi. You can download the image [here](https://www.raspberrypi.org/downloads/)
* Optional, but recommended. Go to Menu > Preferences > Raspberry Pi Configuration > Interfaces > VNC and click on enabled. Make sure you have Real VNC installed on another machine. Click [here](https://www.realvnc.com/en/connect/download/viewer/)
to learn more about installing VNC viewer on your machine. 
* Download this code via `git clone https://github.com/sentairanger/Torvalds-Computer-Vision.git`
* Use the link from Pyimagesearch I have provided to install the prerequisites and to install OpenVino
* Optional, but recommended: install virtualenv via `sudo pip install virtualenv`. Set up your environment by typing `virtualenv -p python3 venv`. This sets up a python3 environment named venv. Then type `source venv/bin/activate` to activate the environment.
* Activate the OpenVino environment by typing `source ~openvino/bin/setupvars.sh` or `source /opt/intel/openvino/bin/setupvars.sh` depending on where you installed OpenVino.
* `cd` into the directory where you cloned the code by typing `cd Torvalds-Computer-Vision`
* Type `python openvino_real_time_object_detection_robot.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel` and it should run. 

![Demo with NCS2](https://media.giphy.com/media/PiQqUq8LnXZvkRtDn7/giphy.gif)

### Optional: Adding Openvino to Your bashrc File
Optionally, you can have Openvino run when you first open your terminal on the Pi. This can also be added on your Linux Machine. To do this type `vi ~/.bashrc` to edit the bashrc file using Vim or `nano ~/.bashrc` to use the nano editor instead. Go to the very end of the file and add `source ~/openvino/bin/setupvars.sh`. Save the file using `:wq` on Vim or if you are using nano type `Ctrl+X` then type `y` to confirm. Then type `source ~/.bashrc` and Openvino will be initialized. 

### Using RealVNC with the robot along with the Intel NCS2

When using the NCS2 it is possible to run this untethered from an HDMI cable and that should be the preferred solution. To do this, go into Menu > Preferences > Raspberry Pi Configuration > Interfaces > VNC > Enable or type `sudo raspi-config` and make sure to enable VNC in the interfaces menu. Then, go to another device (such as your smart phone) and install VNC Viewer via this [link](https://www.realvnc.com/en/connect/download/viewer/). Once installed, look at your Pi's IP address using `ifconfig` and then use that address to log in remotely. This allows you to see what the robot is seeing, especially if you are doing object detection. And this is also helpful if you are setting up that security robot so you can see what is going on. 

### Acknowledgements

* Danny Staple, whose articles were very helpful. You can go [here](https://orionrobots.co.uk/) for more information on his projects.
* The Raspberry Pi Organization, specifically the MagiPi staff for having Danny post on their magazine.
* Adrian from Pyimagesearch who made it possible for me to learn computer Vision, install Openvino and also for having such amazing tutorials that helped my project move along.
