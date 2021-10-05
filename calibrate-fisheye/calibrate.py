import cv2
assert int(cv2.__version__[0]) >= 3, 'The fisheye module requires opencv version >= 3.0.0'
import numpy as np
import os
import glob
import json
import argparse

parser = argparse.ArgumentParser(description='Undistort image based on calibrate data')
parser.add_argument('-row', help="chessboard number of rows", type=int, default=6)
parser.add_argument('-col', help="chessboard number of columns", type=int, default=9)
parser.add_argument('-calibrationDataFile', help="name of the output json file with calibration data", type=str, default="data.json")

args = parser.parse_args()
dataFileName = args.calibrationDataFile

CHECKERBOARD = (args.row-1, args.col-1)

subpix_criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv2.fisheye.CALIB_CHECK_COND+cv2.fisheye.CALIB_FIX_SKEW
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
_img_shape = None
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('images/*.jpg')

print("Images to be processed: ", images)
assert images, 'There should be some images in the directory'

def calculate_points(fname):
    print("\nProcess file: ", fname)
    global _img_shape, gray
    img = cv2.imread(fname)
    if _img_shape == None:
        _img_shape = img.shape[:2]
    else:
        assert _img_shape == img.shape[:2], "All images must share the same size."
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("Gray shape: ", gray.shape)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,
                                             cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    print("Found chessboard corners: ", ret)
    # print("Corners: ", corners)
    # assert ret, "Chessboard corners should be found"
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1), subpix_criteria)
        imgpoints.append(corners)

for f in images:
    calculate_points(f)

N_OK = len(objpoints)
K = np.zeros((3, 3))
D = np.zeros((4, 1))
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]

rms, _, _, _, _ = \
    cv2.fisheye.calibrate(
        objpoints,
        imgpoints,
        gray.shape[::-1],
        K,
        D,
        rvecs,
        tvecs,
        calibration_flags,
        (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
    )

print("Found " + str(N_OK) + " valid images for calibration")
print("DIM=" + str(_img_shape[::-1]))
print("K=np.array(" + str(K.tolist()) + ")")
print("D=np.array(" + str(D.tolist()) + ")")

param = {
   'K': K.tolist(),
   'D': D.tolist()
}
res = json.dumps(param)
print(res)

with open(dataFileName, 'w') as f:
    f.write(res)

