from imutils import paths
import shutil
import cv2
import sys
import os
from imgurpython import ImgurClient 
import lib.config 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def laplacian_variance(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()

print("Name of the folder in the same directory as this script?")
src = input()
dest = src+'/blurry'

client_id = lib.config.client_id
client_secret = lib.config.client_secret
client_user = lib.config.client_user
client_password = lib.config.client_password
client = ImgurClient(client_id, client_secret)


auth_url = (client.get_auth_url('pin'))
print("Click to authorize Imgur Account.")
print(auth_url)
#driver = webdriver.Chrome()
#driver.get(auth_url)

#user = driver.find_element_by_xpath('//*[@id="username"]')
#user.clear()
#password = driver.find_element_by_xpath('//*[@id="password"]')
#password.clear()
#user.send_keys(client_user)
#password.send_keys(client_password)

#driver.find_element_by_name("allow").click()
#try:
#    pinNum_pres = WebDriverWait(driver, 10).until(
#        EC.presence_of_element_located((By.ID, "pin"))
#    )
#    pinNum = driver.find_element_by_name("pin").get_attribute("value")
#    print(pinNum)
#except:
#    print("Timed out")

creds = client.authorize(input("Enter Pin Number here: "))
client.set_user_auth(creds['access_token'], creds['refresh_token'])
print("Authorized")

#Create the album
albumConfig = {
    'title': src,
    'description': 'No blurry pictures'
}

album = client.create_album(albumConfig)
print("Alum ID: " + album['id'])
album_link = 'https://imgur.com/a/' + album['id']
img_cfg = {
    'album': album['id']
}
for path in paths.list_images(src):
    print(path)
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_var = laplacian_variance(gray)

    #not blurry 
    if image_var > 100:
        #upload to imgur album here, otherwise move to folder
        #cv2.putText(image, "Not Blurry: {:.2f}".format(image_var), (0,20), cv2.FONT_HERSHEY_PLAIN, 1.50, (0,255,0), 2)
        #blurry
        image = client.upload_from_path(path, config=img_cfg, anon=False)
    else:
        #need to move the image to another directory
        if not os.path.exists(dest):
            os.makedirs(dest)
        #cv2.putText(image, "Blurry: {:.2f}".format(image_var), (0,20), cv2.FONT_HERSHEY_PLAIN, 1.50, (0,0,255), 2)
        
        #handle duplicate copy
        try:
            shutil.copy2(path, dest)
            os.remove(path)
        except shutil.SameFileError:
            pass
print("Done")
print("Link to the album" + album_link);

#driver.get(album_link);