import cv2
import imutils
import numpy as np
import os
import sys
import glob
import json
import argparse

parser = argparse.ArgumentParser(description='Undistort image based on calibrate data')
parser.add_argument('-imgHeight', help="height of the image", type=int, default=4032)
parser.add_argument('-imgWidth', help="widthy of the image", type=int, default=3024)
parser.add_argument('-calibrationDataFile', '--calibrationDataFile', help="name of the json file with calibration data", type=str, default="data.json")

args = parser.parse_args()

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

def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    # https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#initundistortrectifymap
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    undistorted_img_resized = imutils.resize(undistorted_img, width=800)
    cv2.imshow("undistorted %s" % img_path, undistorted_img_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

images = glob.glob('images/*.jpg')

print("Showing only the first image")
for f in images[:1]:
    undistort(f)
