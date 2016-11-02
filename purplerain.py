import requests
import json
import urllib 
import os
import time
#import vlc
import sched
import sqlite3

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

def create_playlist_table(conn, c):
    c.execute("CREATE TABLE playlist (sequence int, filename text, path text)")
    conn.commit()

def set_base_content(conn, c):
    c.execute("INSERT INTO playlist VALUES (1, 'male.jpg', '" + asset_dir + "male.jpg')")
    c.execute("INSERT INTO playlist VALUES (2, 'female.jpg', '" + asset_dir + "female.jpg')")
    conn.commit()

def get_max_sequence(conn, c):
    c.execute("SELECT MAX(sequence) FROM playlist")
    results = c.fetchone()
    max_seq = results[0]
    print 'Current max sequence: ' + str(max_seq)
    max_seq = max_seq + 1
    print 'Incrementing to: ' + str(max_seq)
    return max_seq

def write_playlist():
    print 'Getting content playlist from server.'
    current_playlist = get_playlist()
    print 'Done.'

    new_playlist = get_playlist()
    if new_playlist != current_playlist:
        current_playlist = new_playlist

    print 'Connecting to database...'
    conn = sqlite3.connect('purplepi.db')
    c = conn.cursor()
    print 'Connection opened.'

    try:
        c.execute("SELECT * FROM playlist")
    except sqlite3.OperationalError:
        print "Table playlist not found. Creating one."
        create_playlist_table(conn, c)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    #print current_playlist['ContentList'][1]
    #print current_playlist['ContentList'][1]['ContentName']

    #Set base content into queue
    print 'Setting up base content.....'
    c.execute("SELECT COUNT(*) FROM playlist")
    count = c.fetchone()
    print count[0]

    if count[0] <= 0:
        print 'Table empty - set base content'
        set_base_content(conn, c)
    
    #Check bases content data
    c.execute("SELECT * FROM playlist")
    print c.fetchall()
    print 'Done'

    print 'Download contents...'
    max_seq = get_max_sequence(conn, c)
    for item in current_playlist['ContentList']:
        filename = download_file(item['ContentName'])
        print item['ContentName'] + ' downloaded to ' + filename
        c.execute("INSERT INTO playlist VALUES (" + str(max_seq) + ", '"+ item['ContentName'] +"', '" + filename + "')")
        max_seq += 1

    conn.commit()
    c.execute("SELECT * FROM playlist")
    print c.fetchall()
    print 'Done'

def get_targeted_ad():
    print 'getting targeted ad....'
    default_snapshot_interval = 5 #5 seconds interval of each photos

    #threading.Timer(default_snapshot_interval, get_targeted_ad)
    
    #take photo
    #call API and get response
    #add response to global queue

    #repeat
s = sched.scheduler(time.time, time.sleep)

write_playlist()

'thread 1 - get playlist, populate global queue, play items'
'thread 2 - take pic, upload, get response and update global queu'
