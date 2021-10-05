# USAGE
# python realtime_stitching.py

# import the necessary packages
from __future__ import print_function
from pyimagesearch.basicmotiondetector import BasicMotionDetector
from pyimagesearch.panorama import Stitcher
from imutils.video import VideoStream
import numpy as np
import datetime
import imutils
import time
import cv2
import json
import argparse

def undistort(img):
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    undistorted_img_resized = imutils.resize(undistorted_img, width=800)
    return undistorted_img_resized

parser = argparse.ArgumentParser(description='Realtime panorama stitching DEMO')
parser.add_argument('-src', help="[file | cam]", type=str, default="cam")
parser.add_argument('-leftStream', help="left video stream", type=str, default="0")
parser.add_argument('-rightStream', help="right video stream", type=str, default="1")

#image calibration parameters:
parser.add_argument('-imgHeight', help="height of the image", type=int, default=3024)
parser.add_argument('-imgWidth', help="widthy of the image", type=int, default=4032)
parser.add_argument('-calibrationDataFile', '--calibrationDataFile', help="name of the json file with calibration data", type=str, default="")

args = parser.parse_args()
src = args.src
leftStreamSrc = args.leftStream
rightStreamSrc = args.rightStream
imgUndistort = args.calibrationDataFile != ""

if imgUndistort:
	H = args.imgHeight
	W = args.imgWidth
	dataFileName = args.calibrationDataFile
	DIM=(W, H)
	with open(dataFileName, 'r') as f:
		data=f.read()
	param = json.loads(data)
	K = np.array(param["K"])
	ORIGINAL_D = np.array(param["D"])
	X = -0.2
	D=np.array([[X], [X], [X], [X]])

print("Data source: ", src)
if src == "cam":
	leftStream = cv2.VideoCapture(int(leftStreamSrc))
	rightStream = cv2.VideoCapture(int(rightStreamSrc))
else:
	leftStream = cv2.VideoCapture(leftStreamSrc)
	rightStream = cv2.VideoCapture(rightStreamSrc)

if not leftStream.isOpened():
    print("Cannot open left stream")
    exit()
if not rightStream.isOpened():
    print("Cannot open right stream")
    exit()

# initialize the image stitcher, motion detector, and total
# number of frames read
stitcher = Stitcher()
motion = BasicMotionDetector(minArea=500)
total = 0

# loop over frames from the video streams
while True:
	# grab the frames from their respective video streams
	ret, left = leftStream.read()
	if not ret:
		print("Left stream problem")
		break
	ret, right = rightStream.read()
	if not ret:
		print("Right stream problem")
		break
	# resize the frames
	left = imutils.resize(left, width=720)
	right = imutils.resize(right, width=720)

	if imgUndistort:
		left = undistort(left)
		right = undistort(right)

	cv2.imshow("left", left)
	cv2.imshow("right", right)

	# stitch the frames together to form the panorama
	# IMPORTANT: you might have to change this line of code
	# depending on how your cameras are oriented; frames
	# should be supplied in left-to-right order
	result = stitcher.stitch([left, right])

	# no homograpy could be computed
	if result is None:
		print("[INFO] homography could not be computed")
		break

	# convert the panorama to grayscale, blur it slightly, update
	# the motion detector
	gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	locs = motion.update(gray)

	# only process the panorama for motion if a nice average has
	# been built up
	if total > 32 and len(locs) > 0:
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
		cv2.rectangle(result, (minX, minY), (maxX, maxY),
			(0, 0, 255), 3)

	# increment the total number of frames read and draw the 
	# timestamp on the image
	total += 1
	timestamp = datetime.datetime.now()
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(result, ts, (10, result.shape[0] - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

	# show the output images
	cv2.imshow("Result", result)
	cv2.imshow("Left Frame", left)
	cv2.imshow("Right Frame", right)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
print("[INFO] cleaning up...")
leftStream.release()
rightStream.release()
cv2.destroyAllWindows()