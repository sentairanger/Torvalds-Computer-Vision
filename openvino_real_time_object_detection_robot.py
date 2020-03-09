# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
from time import sleep
import cv2 
from gpiozero import LED, CamJamKitRobot #change this to Robot if you are not using CamJamKitRobot

# construct the argument parse and parse the arguments
# The -p and -m arguments are required as the robot needs the prototxt file and the pretrained model
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prototxt", required=True,
    help="path to Caffe 'deploy' prototxt file")
parser.add_argument("-m", "--model", required=True,
    help="path to Caffe pre-trained model")
parser.add_argument("-c", "--confidence", type=float, default=0.2,
    help="minimum probability to filter weak detections")
parser.add_argument("-u", "--movidius", type=bool, default=0,
    help="boolean indicating if the Movidius should be used")
args = vars(parser.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
# An ignore class can be added to ignore classes like boats and bottles to only track living things like people or cats
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

#Setup the robot, LED and its boolean value which should be set to false first.
#If you plan to use the Robot module as opposed to the CamJamKitRobot module alter the code as such:
#Let's say you use the pins 27 and 17 for left and 24 and 23 for right. Then alter it as such:
#robot = Robot(left=(27, 17), right=(24,23))
#Also, you can choose another pin number for the LED if you wish. Also, the pin numbering is in BCM format so be sure to take that into consideration.
devastator_eye = LED(25)
devastator_robot = CamJamKitRobot()
robotOn = False
# Blink the LED 4 times to initiate code
#You can omit this but it helps to have this so you know that it's working properly
#Also, it looks cool if you use the LEDs as the eyes for your robot.
for x in range(1, 5):
        devastator_eye.off()
        sleep(0.5)
        devastator_eye.on()
        sleep(0.5)

# load our serialized model from disk
# This will reference both the model and prototxt file
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# specify the target device as the Myriad processor on the NCS2
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
# Change usePiCamera=True to src=0 only if you plan to use a Webcam instead
#NOTE: If you use a webcam be sure that it has a mount for it. You can use electrical tape or even double sided tape.
print("[INFO] starting video stream...")
vs = VideoStream(usePiCamera=True).start()
sleep(2.0)
fps = FPS().start()

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    # You can alter this to whatever width you want such as 500 or 600 depending on your preferences
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the prediction on the frame
            # The confidence * 100 number will be formatted as a percentage such as 52.7%
            # A rectangle will be drawn with coordinates startX, startY, endX, endY
            # Then text will be added to the top of the rectangle using Hershey Simplex Font. You can use any other font you want
            #y will equal startY - 15 only if  startY - 15 is less than 15, otherwise it will equal startY + 15
            label = "{}: {:.2f}%".format(CLASSES[idx],
                confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            #If the robotOn variable is true and the classes chosen is a person move the robot forward
            if (CLASSES[15]) and not robotOn:
                devastator_robot.forward()
                robotOn = True
                


            
            


        #If the class does not equal person and the variable is false the robot will stop 
    else:
        devastator_robot.stop()
        robotOn = False
        
        
        
    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    # This can use any key you want such as s or t or x
    if key == ord("q"):
        break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
# The first one will show elapsed time and the second shows approximate FPS. 
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
# Windows will be closed down and video streaming will stop
cv2.destroyAllWindows()
vs.stop()
devastator_robot.stop() #Add this in case the robot is still running. This will turn off the motors gracefully.
