from gpiozero import CamJamKitRobot
from contours import get_saturated_colors, setup_camera #import from the contours script
from time import sleep

#setup the robot as well as the camera function
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
        devastator_robot.stop()
    capture_buffer.truncate(0)