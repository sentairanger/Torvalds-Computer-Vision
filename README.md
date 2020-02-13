# Torvalds-Computer-Vision

## Overview of the project

This is a project I did based on the tutorial by Danny Staple in the Magpi magazine issue 90. Here is a link for more information. https://magpi.raspberrypi.org/articles/add-navigation-to-a-low-cost-robot . However I must make this clear that I decided to change things here as well as correcting some of the errors in his code. Yes there were a few errors I had to correct and I also used different processses to get things running.

### Needed Items

To get things started I had my Raspberry Pi Robot which uses the Devastator Tank Mobile Platform from DFRobot. I had a Pi Zero W as well as a generic USB power supply, 6 AA batteries and two HDD LEDs for eyes. For the motor controller I used the one included with the CamJam Edukit 3. I had a Pi Camera mounted on a 3D printed mount. To get things started I had to install OpenCV using the instructions from the link above. 

### Getting everything running

After everything was set up I connected a monitor and bluetooth keyboard/mouse controller to get the code running. Every time I ran any code I had to invoke the `export LD_PRELOAD=/usr/lib/arm-linux_gnueabihf/libatomic.so` variable because otherwise it would not run. Now if you compiled OpenCV this would not be needed. Also note that if you are going to install the headless version of OpenCV make sure you only install it on CLI environment not a GUI one. I did that and it kept giving me issues until I uninstalled and replaced it with the correct version. First I used the `contours.py` script which takes a picture and returns three image types: the original, masked and contoured. The masked image is the image where all color is removed and replaced with white. The contoured image shows the image with a green line drawn around the captured color. After that I ran the first code,`devastator_nav.py` where it would turn left or right if the colors blue or yellow were present. This is similar to an obstacle avoidance robot. After that I decided to try color detection so I ran the `devastator_detection.py` script so that the robot moves only when it sees blue or yellow. After that success I ran the `devastator_detection_triple.py` script to have the robot move forward when it sees red. 

### Note on running this with other hardware

If you are running this with any other hardware, make sure you adjust accordingly. Example, if you use an L298N as opposed to the motor controller from CamJam Edukit 3, make sure you change the import to `from gpiozero import Robot` and then set the Robot equal to `Robot(left=(pin1, pin2), right=(pin3, pin4))` where pin1 through pin4 are the pin numbers you choose. Also if you prefer to use another Pi make sure to give it proper power. If you plan to use a UBEC, be sure to connect things properly otherwise it will not work. 

### Using an Intel NCS2 with the robot

Since this uses OpenCV adding an Neural Compute Stick 2 is perfect to expand on its capabilities. Follow this guide I found on PyImageSearch website to install openvino. https://www.pyimagesearch.com/2019/04/08/openvino-opencv-and-movidius-ncs-on-the-raspberry-pi/ . Also, using the openvino toolkit with the NCS2 is great as you can use the caffe model, for example to do object detection for the robot and have it move based on what it sees. For example, I can have it move left if it sees a cat, or right when it sees a dog. This is expandable even to other models like Tensorflow and ONNX. However, I recommend using a Pi 3 or 3B+ as they have more USB ports for future expansion, a faster CPU. 

### Acknowledgements

* Danny Staple, whose articles were very helpful. You can go to https://orionrobots.co.uk/ for more information on his projects.
* The Raspberry Pi Organization, specifically the MagiPi staff for having Danny post on their magazine.
