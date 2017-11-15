from imutils import paths
import cv2
import sys

for path in paths.list_images(sys.argv[1]):
    #print(path)
    image = cv2.imread(path)
    cv2.imshow("Picture", image)
    key = cv2.waitKey(0)