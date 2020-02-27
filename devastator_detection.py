#import libraries
from gpiozero import CamJamKitRobot #if you don't have this board switch this with Robot
from contours import get_saturated_colors, setup_camera #import from the contours program

#Setup the robot, and camera function
#These are the instructions if you don't own the CamJam Edukit 3
#Let's say you use the pins 27 and 17 for left and 24 and 23 for right. Then alter it as such:
#robot = Robot(left=(27, 17), right=(24,23))
devastator_robot = CamJamKitRobot()
camera, capture_buffer = setup_camera()

#Set things up for movement
for raw in camera.capture_continuous(capture_buffer, format="bgr"):
    image = raw.array 
    masked, contours, found_color = get_saturated_colors(image) #This is called from the contours script
    print(f"Color {found_color}, h value: {found_color[0]}") #This will print the color name as well as the value in an RBG array
    if 5 < found_color[0] < 40: #This chooses the first value of the array. This chooses values based on the color wheel
        print("yellow")
        devastator_robot.backward()
    elif 100 < found_color[0] < 135:
        print("blue")
        devastator_robot.forward() 
    else:
        devastator_robot.stop()
    capture_buffer.truncate(0)
