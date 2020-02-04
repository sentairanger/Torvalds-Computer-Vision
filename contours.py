#This is the code for the robot to detect contours
from time import sleep
import imutils
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from gpiozero import LED

#import the LED eye
devastator_eye = LED(25)

#Let the LED blink 4 times before the code runs
for x in range(1, 5):
  devastator_eye.off()
  sleep(0.5)
  devastator_eye.on()
  sleep(0.5)

#Setup the camera
def setup_camera():
  camera = PiCamera()
  camera.resolution = (128, 128)
  #camera.rotation = 180 #Set this variable only if your camera is upside down
  capture_buffer = PiRBGArray(camera, size=(128, 128))
  camera.start_preview()
  sleep(2)
  return camera, capture_buffer

#Define the saturated colors function 
def get_saturated_colors(image):
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #This converts a BGR format to an HSV format 
  #Mask for vivid colors
  cnts = cv2.findContours(masked.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  contours = imutils.grab_contours(cnts)
  contours = sorted(contours, key=cv2.contourArea, reverse=True)
  color = [0, 0, 0]
  m = cv2.moments(contours[0])
  if m["m00"] > 0:
    cx = int(m["m10"] / m["m00"])
    cy = int(m["m01"] / m["m00"])
    color = hsv[cy, cx]
  return masked, contours, color

#The camera will take a contour, original and masked picture and save them as original.png, masked.png and with_contours.jpg
if __name__ == '__main__':
  camera, capture_buffer = setup_camera()
  camera.capture(capture_buffer, format="bgr")
  image = capture_buffer.array
  masked_contours, found_color = get_saturated_colors(image)
  cv2.imwrite('original.jpg' , image)
  cv2.imwrite('masked.jpg', masked)
  cv2.drawContours(image, contours[:1], -1, (0, 255, 0), 1)
  cv2.imwrite('with_contours.png', image)
  print(found_color)
