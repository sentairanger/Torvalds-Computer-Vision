#This is the code used for the robot to move based on the color it sees using the Pi Camera
from gpiozero import CamJamKitRobot
from contours import setup_camera, get_saturated_colors

#Setup the camjamkit robot. The pins are already defined by the board
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
