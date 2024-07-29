import os
import sys
import time
from naoqi import ALProxy

IP = "192.168.1.128"
PORT = 9559

try:
  videoRecorderProxy = ALProxy("ALVideoRecorder", IP, PORT)
except Exception as e:
  print ("Error when creating ALVideoRecorder proxy:")
  print (str(e))
  exit(1)

videoRecorderProxy.setFrameRate(10.0)
videoRecorderProxy.setResolution(2) # Set resolution to VGA (640 x 480)
# We'll save a 5 second video record in /home/nao/recordings/cameras/
videoRecorderProxy.startRecording("/home/nao/recordings/cameras", "test")
print ("Video record started.")

time.sleep(5)

videoInfo = videoRecorderProxy.stopRecording()
print ("Video was saved on the robot: ", videoInfo[1])
print ("Total number of frames: ", videoInfo[0])