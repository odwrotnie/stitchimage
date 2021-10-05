from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
from datetime import datetime

# images_path = "images/hockey"
images_path = "images/scottsdale"
output_file = "output %s.png" % datetime.now()

print("[INFO] loading images...")
image_paths = sorted(list(paths.list_images(images_path)))
images = []

for img in image_paths:
	print("Appending image: ", img)
	image = cv2.imread(img)
	images.append(image)

print("Stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)#, ratio=0.75, reprojThresh=4.0)

if status == 0:
	print("Writing output to: %s" % output_file)
	cv2.imwrite(output_file, stitched)
	print("Show the image (waiting for key press)")
	cv2.imshow("Stitched", stitched)
	cv2.waitKey(0)

# otherwise the stitching failed, likely due to not enough keypoints)
# being detected
else:
	print("Image stitching failed: %s" % status)
