import libjevois as jevois
import cv2
import numpy as np

## Simple test of programming JeVois modules in Python
#
# This module by default simply draws a cricle and a test message onto the grabbed video frames.
#
# Feel free to edit it and try something else.
#
# @author Laurent Itti
# 
# @videomapping YUYV 640 480 15.0 YUYV 640 480 15.0 JeVois SamplePythonModule
# @email itti\@usc.edu
# @address University of Southern California, HNB-07A, 3641 Watt Way, Los Angeles, CA 90089-2520, USA
# @copyright Copyright (C) 2017 by Laurent Itti, iLab and the University of Southern California
# @mainurl http://jevois.org
# @supporturl http://jevois.org/doc
# @otherurl http://iLab.usc.edu
# @license GPL v3
# @distribution Unrestricted
# @restrictions None
# @ingroup modules
class SamplePythonModule:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # A simple frame counter used to demonstrate sendSerial():
        self.frame = 0
        
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("canny", 100, jevois.LOG_INFO)

    # ###################################################################################################
    ## Process function with no USB output
    def process(self, inframe):
        jevois.LFATAL("process no usb not implemented")

    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        # Get the next camera image (may block until it is captured) and convert it to OpenCV BGR:
        img = inframe.getCvBGR()

        # Get image width, height, channels in pixels. Beware that if you change this module to get img as a grayscale
        # image, then you should change the line below to: "height, width = img.shape" otherwise numpy will throw. See
        # how it is done in the PythonOpenCv module of jevoisbase:
        height, width, chans = img.shape

        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()

        # Draw a couple of things into the image:
        # See http://docs.opencv.org/3.2.0/dc/da5/tutorial_py_drawing_functions.html for tutorial
        # See http://docs.opencv.org/3.0-beta/modules/imgproc/doc/drawing_functions.html and
        #     http://docs.opencv.org/3.2.0/d6/d6e/group__imgproc__draw.html for reference manual.
        cv2.circle(img, (int(width/2), int(height/2)), 100, (255,0,0), 3) 

        cv2.putText(img, "Hello JeVois - frame {}".format(self.frame), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0,0,255), 1, cv2.LINE_AA)

        # Write frames/s info from our timer (NOTE: does not account for output conversion time):
        fps = self.timer.stop()
        cv2.putText(img, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
    
        # Convert our BGR image to video output format and send to host over USB:
        outframe.sendCvBGR(img)
         
        # Send a string over serial (e.g., to an Arduino). Remember to tell the JeVois Engine to display those messages,
        # as they are turned off by default. For example: 'setpar serout All' in the JeVois console:
        jevois.sendSerial("DONE frame {}".format(self.frame));
        self.frame += 1

    # ###################################################################################################
    ## Parse a serial command forwarded to us by the JeVois Engine, return a string
    # This function is optional and only needed if you want your module to handle custom commands. Delete if not needed.
    def parseSerial(self, str):
        print("parseserial received command [{}]".format(str))
        if str == "hello":
            return self.hello()
        return "ERR: Unsupported command"
    
    # ###################################################################################################
    ## Return a string that describes the custom commands we support, for the JeVois help message
    # This function is optional and only needed if you want your module to handle custom commands. Delete if not needed.
    def supportedCommands(self):
        # use \n seperator if your module supports several commands
        return "hello - print hello using python"

    # ###################################################################################################
    ## Internal method that gets invoked as a custom command
    # This function is optional and only needed if you want your module to handle custom commands. Delete if not needed.
    def hello(self):
        return("Hello from python!")
        
