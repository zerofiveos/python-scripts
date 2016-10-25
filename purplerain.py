import requests
#import base64
import json
import urllib 
#import uuid
#from PIL import Image
import os
import time
#import numpy as np
#import cv2
import vlc

#APIs
face_recog_api = 'http://rrpp22.azurewebsites.net/api/video/process'
content_sync_api = 'http://rrpp22.azurewebsites.net/api/sync/latest/11' 

#asset folders
global asset_dir
print 'Setting up assets folder'
current_working_dir = os.path.dirname(os.path.realpath(__file__))
asset_dir = current_working_dir + '/assets/'

if not os.path.exists(asset_dir):
    print 'Assets folder not found. Creating a new folder....'
    os.makedirs(asset_dir)
    print 'Created: ' + asset_dir

print 'Assets folder set to: ' + asset_dir

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

    try:
        urllib.urlretrieve(source_url, filename)       
    except:
        print "file download error"
    return filename
            
#def run_playlist():
print 'Getting content playlist from server.'
current_playlist = get_playlist()
print 'Done.'

#TODO: spin off new thread to constantly check if playlist has changed. if changed, update VLC playlist and play new content.
    #while True:
new_playlist = get_playlist()
if new_playlist != current_playlist:
    current_playlist = new_playlist

#print current_playlist['ContentList'][1]
#print current_playlist['ContentList'][1]['ContentName']

vlc_instance = vlc.Instance()
#add base media content -- content to display even if the sync fails
print 'Setting up base content.'
media = vlc_instance.media_new_path('/home/os/Code/python-scripts/assets/male.jpg') #to check if base content exists
media_list = vlc_instance.media_list_new()
media_list.add_media(media)
media = vlc_instance.media_new_path('/home/os/Code/python-scripts/assets/female.jpg')
media_list.add_media(media)
#test video
#media_list.add_media(vlc_instance.media_new('/home/os/Code/python-scripts/assets/movie.mp4'))
print 'Done'

print 'Setting up media player instances'
mlplayer = vlc_instance.media_list_player_new()
mlplayer.set_media_list(media_list)

mplayer = vlc_instance.media_player_new()
mplayer.set_fullscreen(True)
mlplayer.set_media_player(mplayer)

for item in current_playlist['ContentList']:
    filename = download_file(item['ContentName'])
    print item['ContentName'] + ' downloaded to ' + filename
    media = vlc_instance.media_new_path(filename)
    media_list.add_media(media)

mlplayer.play()
time.sleep(60)

'''image_files = [
'/home/os/Code/python-scripts/assets/male.jpg',
'/home/os/Code/python-scripts/assets/female.jpg'
]

for image in image_files:
    img = cv2.imread(image, 1)
    print 'before'
    cv2.imshow('male.jpg', img)
    print 'after'
    cv2.waitKey(10000)

cv2.destroyAllWindows()'''

