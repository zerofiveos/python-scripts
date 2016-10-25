import vlc
import time

vlc_instance = vlc.Instance()
media = vlc_instance.media_new_path('/home/os/Code/python-scripts/assets/male.jpg')

#player = vlc_instance.media_player_new()
#player.set_media(media)

#player.play()



media_list = vlc_instance.media_list_new()
media_list.add_media(media)
media = vlc_instance.media_new_path('/home/os/Code/python-scripts/assets/female.jpg')
media_list.add_media(media)
media_list.add_media(vlc_instance.media_new('/home/os/Code/python-scripts/assets/movie.mp4'))

mlplayer = vlc_instance.media_list_player_new()
mlplayer.set_media_list(media_list)

mplayer = vlc_instance.media_player_new()
#mplayer.set_media(media)
mplayer.set_fullscreen(True)
mlplayer.set_media_player(mplayer)
mlplayer.play()


#mplayer.play()


time.sleep(30)
