import sys
import time
import numpy as np

# Python Image Library
from PIL import Image
import matplotlib.pyplot as plt
from naoqi import ALProxy


def showNaoImage(IP, PORT):
  """
  First get an image from Nao, then show it on the screen with PIL.
  """

  device = discover_one_device()
  resolution = 2    # VGA
  colorSpace = 11   # RGB

  # Set up the matplotlib figure and axis
  plt.ion()  # Interactive mode on
  fig, ax = plt.subplots()
  img = ax.imshow(np.zeros((480, 640, 3), dtype=np.uint8))  # Initialize with a blank image
  ax.set_title('NAO Camera Feed')
  
  num = 0  
  while True:

    scene_sample, gaze_sample = device.receive_matched_scene_video_frame_and_gaze()
    t0 = time.time()

    # Get a camera image.
    # image[6] contains the image data passed as an array of ASCII chars.



    # Now we work with the image returned and save it as a PNG  using ImageDraw
    # package.

    # Get the image size and pixel array.
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]

    # Create a PIL Image from our pixel array.
    im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

    # Save the image.
    # im.save("NaoPhotos/camImage" + str(num) + ".png", "PNG")
    # im.show()

    image_array = np.frombuffer(array, dtype=np.uint8).reshape((imageHeight, imageWidth, 3))

    # Update the image displayed in matplotlib
    img.set_data(image_array)
    plt.draw()
    plt.pause(0.1)  # Pause to update the plot and to control the update rate

    num += 1
  



if __name__ == '__main__':
  IP = "192.168.1.128"  # Replace here with your NaoQi's IP address.
  PORT = 9559

  # Read IP address from first argument if any.
  if len(sys.argv) > 1:
    IP = sys.argv[1]

  naoImage = showNaoImage(IP, PORT)