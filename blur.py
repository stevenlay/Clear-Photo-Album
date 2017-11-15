from imutils import paths
import shutil
import cv2
import sys
import os

def laplacian_variance(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()

src = sys.argv[1]
dest = src+'/blurry'

for path in paths.list_images(src):
    print(path)
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_var = laplacian_variance(gray)

    #not blurry 
    if image_var > 100:
         cv2.putText(image, "Not Blurry: {:.2f}".format(image_var), (0,20), cv2.FONT_HERSHEY_PLAIN, 1.50, (0,255,0), 2)
    #blurry
    else:
        #need to move the image to another directory
        if not os.path.exists(dest):
            os.makedirs(dest)
        cv2.putText(image, "Blurry: {:.2f}".format(image_var), (0,20), cv2.FONT_HERSHEY_PLAIN, 1.50, (0,0,255), 2)
        
        #handle duplicate copy
        try:
            shutil.copy2(path, dest)
            os.remove(path)
        except shutil.SameFileError:
            pass
    cv2.imshow("Picture", image)
    key = cv2.waitKey(0)