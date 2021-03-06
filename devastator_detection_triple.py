#import libraries
from gpiozero import CamJamKitRobot #import Robot only if you use a different board
from contours import get_saturated_colors, setup_camera #import from the contours script

#setup the robot as well as the camera function
#If you don't use the CamJam Edukit 3 here are the instructions 
#Let's say you use the pins 27 and 17 for left and 24 and 23 for right. Then alter it as such:
#robot = Robot(left=(27, 17), right=(24,23))
devastator_robot = CamJamKitRobot()
camera, capture_buffer = setup_camera()

#Like before this sets the robot up
for raw in camera.capture_continuous(capture_buffer, format="bgr"):
    image = raw.array
    masked, contours, found_color = get_saturated_colors(image) #This is exactly invoked as in the last script. 
    print(f"Color {found_color}, h value: {found_color[0]}") #Just like before it prints the color name and the value
    if 5 < found_color[0] < 40:
        print("yellow")
        devastator_robot.backward()
    elif 100 < found_color[0] < 135:
        print("blue")
        devastator_robot.forward()
    elif 165 < found_color[0] < 180: #Red is added here for expandability. Again, based on the color wheel and it chooses the first value of the array
        print("red")
        devastator_robot.right()
    else:
        devastator_robot.stop() #It stops if it sees no other color. 
    capture_buffer.truncate(0)
