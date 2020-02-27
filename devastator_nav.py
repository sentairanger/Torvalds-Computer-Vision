#This is the code used for the robot to move based on the color it sees using the Pi Camera
#import needed libraries
from gpiozero import CamJamKitRobot #Change this to Robot if you do not have the Cam Jam Edukit 3 robotics kit
from contours import setup_camera, get_saturated_colors #import from the contours program 

#Setup the camjamkit robot. The pins are already defined by the board
#The following instructions are for those who do not use the Cam Jam Edukit 3 robotics kit
#Let's say you use the pins 27 and 17 for left and 24 and 23 for right. Then alter it as such:
#robot = Robot(left=(27, 17), right=(24,23))
devastator_robot = CamJamKitRobot()
camera, capture_buffer = setup_camera()

#When the robot sees yellow, the robot turns left, when the robot sees blue it turns right. Otherwise it goes forward
for raw in camera.capture_continuous(capture_buffer, format="bgr"):
  image = raw.array
  masked, contours, found_color = get_saturated_colors(image)
  print(f"Color {found_color}, h value: {found_color[0]}")
  if 5 < found_color[0] < 40: #It looks at the first element of the found_color variable.
    print("yellow")
    devastator_robot.left()
  elif 100 < found_color[0] < 135:
    print("blue")
    devastator_robot.right()
  else:
    devastator_robot.forward()
  capture_buffer.truncate(0)
