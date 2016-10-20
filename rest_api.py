import requests
import base64
import json
import urllib 
import uuid

#Open image file from camera
with open('dafuq.jpeg', 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read())

#with open('image') as basesixfour_image:
#    json_encoded_image = basesixfour_image.read()

json_encoded_image = {}

json_encoded_image['base64Image'] = encoded_string

header = {'content-type':'application/json'}

resp = requests.post('http://rrrppp333.azurewebsites.net/api/video/process', data=json.dumps(json_encoded_image), headers=header )

if resp.status_code != 200:
    # This means something went wrong.
    print 'Error ' + str(resp.status_code)

json_output = json.loads(resp.text)

video_to_play = json_output['videoName']
uploaded_image = json_output['uploadedImage'] 

print video_to_play
print uploaded_image

video_file_name = 'video' + str(uuid.uuid1()) + '.mp4'

testfile = urllib.URLopener()
testfile.retrieve(video_to_play, video_file_name)

def play_movie(path):
    from os import system
    system("vlc -f -L " + path)

play_movie(video_file_name)