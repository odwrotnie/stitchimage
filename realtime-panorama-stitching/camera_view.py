from __future__ import print_function

# noinspection PyUnresolvedReferences
import cv2
import imutils
import numpy as np
from imutils.video import VideoStream

from pyimagesearch.basicmotiondetector import BasicMotionDetector

# camStream = VideoStream(src="rtmp://83.17.11.77:1935/orlen/kamera_2").start()
camStream = cv2.VideoCapture(0)
motion = BasicMotionDetector(minArea=500)

while True:
    ret, frame = camStream.read()
    # cam = imutils.resize(cam, width=800)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    locs = motion.update(gray)
    if len(locs) > 0:
        # initialize the minimum and maximum (x, y)-coordinates,
        # respectively
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        # loop over the locations of motion and accumulate the
        # minimum and maximum locations of the bounding boxes
        for l in locs:
            (x, y, w, h) = cv2.boundingRect(l)
            (minX, maxX) = (min(minX, x), max(maxX, x + w))
            (minY, maxY) = (min(minY, y), max(maxY, y + h))

        # draw the bounding box
        cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                      (0, 0, 255), 3)

    cv2.imshow("Left Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
camStream.stop()
