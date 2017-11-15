from imutils import paths
import cv2
import sys

def laplacian_variance(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()

for path in paths.list_images(sys.argv[1]):
    #print(path)
    image = cv2.imread(path)
    image_var = laplacian_variance(image)

    #not blurry 
    if image_var > 100:
         cv2.putText(image, "Not Blurry: {:.2f}".format(image_var), (0,20), cv2.FONT_HERSHEY_PLAIN, 1.50, (0,255,0), 2)
    #blurry
    else:
         cv2.putText(image, "Blurry: {:.2f}".format(image_var), (0,20), cv2.FONT_HERSHEY_PLAIN, 1.50, (0,0,255), 2)
    cv2.imshow("Picture", image)
    key = cv2.waitKey(0)