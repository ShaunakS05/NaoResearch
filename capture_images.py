#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import time
import argparse
import cv2 as cv
import sys

# Python Image Library
from PIL import Image

from naoqi import ALProxy


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)
    parser.add_argument("--families", type=str, default='tag36h11')
    parser.add_argument("--nthreads", type=int, default=1)
    parser.add_argument("--quad_decimate", type=float, default=2.0)
    parser.add_argument("--quad_sigma", type=float, default=0.0)
    parser.add_argument("--refine_edges", type=int, default=1)
    parser.add_argument("--decode_sharpening", type=float, default=0.25)
    parser.add_argument("--debug", type=int, default=0)
    args = parser.parse_args()
    return args
def main():
    ##################################################################
    args = get_args()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height
    families = args.families
    nthreads = args.nthreads
    quad_decimate = args.quad_decimate
    quad_sigma = args.quad_sigma
    refine_edges = args.refine_edges
    decode_sharpening = args.decode_sharpening
    debug = args.debug
    ################################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)
    # Detector #############################################################
    # at_detector = Detector(
    #     families=families,
    #     nthreads=nthreads,
    #     quad_decimate=quad_decimate,
    #     quad_sigma=quad_sigma,
    #     refine_edges=refine_edges,
    #     decode_sharpening=decode_sharpening,
    #     debug=debug,
    # )
    elapsed_time = 0
    camProxy = ALProxy("ALVideoDevice", IP, PORT)
    resolution = 2    # VGA
    colorSpace = 11   # RGB

    while True:
        start_time = time.time()
        ######################################################
        # ret, image = cap.read()
        # if not ret:
        #     break
        # debug_image = copy.deepcopy(image)
        # ##############################################################
        # image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        # tags = at_detector.detect(
        #     image,
        #     estimate_tag_pose=False,
        #     camera_params=None,
        #     tag_size=None,
        # )
        # print(len(tags))
        # #################################################################
        # debug_image = draw_tags(debug_image, tags, elapsed_time)
        # elapsed_time = time.time() - start_time
        # ##################################################
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break
        ##############################################################
        videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)
        t0 = time.time()

        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        naoImage = camProxy.getImageRemote(videoClient)

        t1 = time.time()

        # Time the image transfer.
        print ("acquisition delay ", t1 - t0)

        camProxy.unsubscribe(videoClient)


        # Now we work with the image returned and save it as a PNG  using ImageDraw
        # package.

        # Get the image size and pixel array.
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        array = naoImage[6]

        # Create a PIL Image from our pixel array.
        im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

        # # Save the image.
        # im.save("NaoPhotos/camImage" + str(num) + ".png", "PNG")
        # im.show()

        num = num + 1
    
        cv.imshow('AprilTag Detect Demo', im)

    cap.release()
    cv.destroyAllWindows()
def draw_tags(
    image,
    tags,
    elapsed_time,
):
    for tag in tags:
        tag_family = tag.tag_family
        tag_id = tag.tag_id
        center = tag.center
        corners = tag.corners
        center = (int(center[0]), int(center[1]))
        corner_01 = (int(corners[0][0]), int(corners[0][1]))
        corner_02 = (int(corners[1][0]), int(corners[1][1]))
        corner_03 = (int(corners[2][0]), int(corners[2][1]))
        corner_04 = (int(corners[3][0]), int(corners[3][1]))
        #
        cv.circle(image, (center[0], center[1]), 5, (0, 0, 255), 2)
        #
        cv.line(image, (corner_01[0], corner_01[1]),
                (corner_02[0], corner_02[1]), (255, 0, 0), 2)
        cv.line(image, (corner_02[0], corner_02[1]),
                (corner_03[0], corner_03[1]), (255, 0, 0), 2)
        cv.line(image, (corner_03[0], corner_03[1]),
                (corner_04[0], corner_04[1]), (0, 255, 0), 2)
        cv.line(image, (corner_04[0], corner_04[1]),
                (corner_01[0], corner_01[1]), (0, 255, 0), 2)
        # ID
        # cv.putText(image,
        #            str(tag_family) + ':' + str(tag_id),
        #            (corner_01[0], corner_01[1] - 10), cv.FONT_HERSHEY_SIMPLEX,
        #            0.6, (0, 255, 0), 1, cv.LINE_AA)
        cv.putText(image, str(tag_id), (center[0] - 10, center[1] - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)
    #
    cv.putText(image,
               "Elapsed Time:" + '{:.1f}'.format(elapsed_time * 1000) + "ms",
               (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
               cv.LINE_AA)
    return image
if __name__ == '__main__':
    main()