# Torvalds-Computer-Vision

## Overview of the project

This is a project I did based on the tutorial by Danny Staple in the Magpi magazine issue 90. Here is a link for more information. https://magpi.raspberrypi.org/articles/add-navigation-to-a-low-cost-robot . However I must make this clear that I decided to change things here as well as correcting some of the errors in his code. Yes there were a few errors I had to correct and I also used different processses to get things running.

### Needed Items

To get things started I had my Raspberry Pi Robot which uses the Devastator Tank Mobile Platform from DFRobot. I had a Pi Zero W as well as a generic USB power supply, 6 AA batteries and two HDD LEDs and LED bezels for eyes. For the motor controller I used the one included with the CamJam Edukit 3. I had a Pi Camera mounted on a 3D printed mount. To get things started I had to install OpenCV using the instructions from the link above. 

### Getting everything running

Note: the Pi Camera must be enabled using `sudo raspi-config` or the Raspberry Pi Configuration menu. After everything was set up I connected a monitor and bluetooth keyboard/mouse controller to get the code running. Every time I ran any code I had to invoke the `export LD_PRELOAD=/usr/lib/arm-linux_gnueabihf/libatomic.so` variable because otherwise it would not run. Now if you compiled OpenCV this would not be needed. Also note that if you are going to install the headless version of OpenCV make sure you only install it on CLI environment not a GUI one. I did that and it kept giving me issues until I uninstalled and replaced it with the correct version. So here is what each piece of code does and how to run it. I will add more to this as time goes by:

* `contours.py` takes three images of what it sees and outputs them as `with-contours.jpg`, `masked.jpg` and `original.jpg`. The masked image is in black and white and masks the color that it sees. The contours image is the image that draws a green line on the color itself. The `contours_big.jpg` and `masked_big.jpg` images are examples you can reference. To run it, type `python3 contours.py` or `python contours.py ` if you are running a virtual environment. If you did not compile OpenCV and you used Danny Staple's instructions from the link provided please export the LD_PRELOAD variable first.

![Masked photo](https://github.com/sentairanger/Torvalds-Computer-Vision/blob/master/masked_big.png)

![Contour photo](https://github.com/sentairanger/Torvalds-Computer-Vision/blob/master/contours_big.png)

* `devastator_nav.py` import the `get_saturated_colors` and the `camera_setup` functions to set things up. The robot takes constant images to see what color it gets from the `found_color` variable and if it sees yellow, the robot turns left. If it sees blue, it turns right. Otherwise, it just keeps moving forward. To run it, type `python3 devastator_nav.py` or `python devastator_nav.py` if you are using a virtual environment. Also, make sure your floor is of a neutral color and that you have white walls for a background for it to work effectively. Also, good lighting helps.

* `devastator_detection.py` and `devastator_detection_triple.py` are similar, except the latter uses red from the color wheel. To run either, follow the same instructions as with the `devastator_nav.py` code. What happens with the first code is that when it sees yellow it turns left and when it sees blue it turns right. This is just like the previous code I mentioned. However, if it doesn't see either, it does not move. So consider this a color detection robot. To run this experiment I used red, blue and yellow foam balls attached to dowels to get the robot to see the color. In the second code, when it sees red it moves forward. I reference the color wheel to find the ranges of red.


### Video Demo

I added a video demo to the repo, but you will have to click on it to see it due to its file size.
### Note on running this with other hardware

If you are running this with any other hardware, make sure you adjust accordingly. Example, if you use an L298N as opposed to the motor controller from CamJam Edukit 3, make sure you change the import to `from gpiozero import Robot` and then set the Robot equal to `Robot(left=(pin1, pin2), right=(pin3, pin4))` where pin1 through pin4 are the pin numbers you choose. Also if you prefer to use another Pi make sure to give it proper power. If you plan to use a UBEC, be sure to connect things properly otherwise it will not work. 

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

Since this uses OpenCV adding an Neural Compute Stick 2 is perfect to expand on its capabilities. Follow this guide I found on PyImageSearch website to install openvino. https://www.pyimagesearch.com/2019/04/08/openvino-opencv-and-movidius-ncs-on-the-raspberry-pi/ . Also, using the openvino toolkit with the NCS2 is great as you can use the caffe model, for example to do object detection for the robot and have it move based on what it sees. For example, I can have it move left if it sees a cat, or right when it sees a dog. This is expandable even to other models like Tensorflow and ONNX. These options are helpful if you want to set up your own security robot at home. However, I recommend using a Pi 3 or 3B+ as they have more USB ports for future expansion, a faster CPU which means openvino will compile much faster than a Zero or Zero W. You will need to provide more power but you can get away with using a UBEC. 

Update: I got the NCS2 running with my robot and now I can talk about how I got it to work. The program uses MobileNet SSD and Caffe for object detection. And through several classes, if it sees the person class, the robot moves forward. However, this will be improved as object detection is very sensitive here and did cause my robot to stop and go and stop and go. So there will be improvements to add better accuracy. To run the code you must type the following `$ python openvino_real_time_object_detection_robot.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel`. If you are not in a virtual environment change python to python3. This can be modified to have the robot move left if it sees a cat and right if it sees a chair. However, sensitivity settings have to be made to ensure success. 

Here's a rundown of the arguments that must be run for it to work:

* `--prototxt`: This is the prototext that must be used with the program. In this case I'm using the `MobileNetSSD_deploy.prototxt'.
* `--model`: This the model that is required. In this case, I'm using the `MobileNetSSD_deploy.caffemodel` model.

Optional arguments include:
* `--confidence`: This is the confidence threshold. It is set to 0.2 by default.
* `--movidius`: This is a boolean variable to determine if the Movidius NCS2 will be used. It is set to zero by default.

### Using RealVNC with the robot along with the Intel NCS2

When using the NCS2 it is possible to run this untethered from an HDMI cable and that should be the preferred solution. To do this, go into the Raspberry Pi Configuration Menu or type `sudo raspi-config` and make sure to enable VNC in the interfaces menu. Then, go to another device (such as your smart phone) and install RealVNC. Once installed, look at your Pi's IP address using `ifconfig` and then use that address to log in remotely. This allows you to see what the robot is seeing, especially if you are doing object detection. And this is also helpful if you are setting up that security robot so you can see what is going on. 

### Acknowledgements

* Danny Staple, whose articles were very helpful. You can go to https://orionrobots.co.uk/ for more information on his projects.
* The Raspberry Pi Organization, specifically the MagiPi staff for having Danny post on their magazine.
