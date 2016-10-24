import requests
import base64
import json
import urllib 
import uuid
#from PIL import Image
import os
import time
import numpy as np
import cv2

#APIs
face_recog_api = 'http://rrpp22.azurewebsites.net/api/video/process'
content_sync_api = 'http://rrpp22.azurewebsites.net/api/sync/latest/11' 

#asset folders
global asset_dir
current_working_dir = os.path.dirname(os.path.realpath(__file__))
asset_dir = current_working_dir + '/assets/'

if not os.path.exists(asset_dir):
    os.makedirs(asset_dir)

#default header
header = {'content-type':'application/json'}


def get_playlist():
    resp = requests.get(content_sync_api)

    if resp.status_code != 200:
        # This means something went wrong.
        print 'Error ' + str(resp.status_code)

    playlist = json.loads(resp.text)
    return playlist

def download_file(source_url):
    filename = source_url.split('/')[-1]
    if '?' in filename:
        filename = filename.split('?')[0]
    filename = asset_dir + filename

    urllib.urlretrieve(source_url, filename)
    return filename
            
#def run_playlist():
current_playlist = get_playlist()
        
    #while True:
new_playlist = get_playlist()
if new_playlist != current_playlist:
    current_playlist = new_playlist

#print current_playlist['ContentList'][1]
#print current_playlist['ContentList'][1]['ContentName']

for item in current_playlist['ContentList']:
    filename = download_file(item['ContentName'])
    print item['ContentName'] + ' downloaded to ' + filename

image_files = [
'/home/os/Code/python-scripts/assets/male.jpg',
'/home/os/Code/python-scripts/assets/female.jpg'
]

for image in image_files:
    img = cv2.imread(image, 1)
    print 'before'
    cv2.imshow('male.jpg', img)
    print 'after'
    cv2.waitKey(10000)

cv2.destroyAllWindows()

