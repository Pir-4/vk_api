__author__ = 'valentin'
# -*- coding: utf-8 -*-

import sys
import pars_config
import api
import os


# if __name__ == '__main__':
#     parser = createParser()
#     namespace = parser.parse_args(sys.argv[1:])
#
#     if namespace.command == "config":
#         print("ttt")
#         write_config(namespace)
#
#     elif namespace.command == "file":
#         path = namespace.rfile
#         read_config(path)

if not api.chechConnection():
    print("Error: No access to the Internet")
    os._exit(0)

path1,path2 = pars_config.get_path_config()
dist = pars_config.read_config(path1)
dist.update(pars_config.read_config(path2))

if(dist['access_token'] == ""):
    api.get_access_tomen(dist['app_id'],dist['redirect_url'],dist['scope'])

start = []
elem = []
elem.append(1)
elem.append("My albom")
start.append(elem)
elem = []
elem.append(2)
elem.append("My groups")
start.append(elem)
elem = []
elem.append(3)
elem.append("My audio")
start.append(elem)

value =  api.print_list(start)

if value == 1:
    dist_albom = api.getAlbums(dist['user_id'],dist['access_token'],False)
    album_id = api.print_list(dist_albom)
    list_photo_id = api.getIdPhotos(dist['user_id'],album_id,dist['access_token'],False)
    photo_url = api.getByidAll(list_photo_id,dist['user_id'],False,dist['access_token'])
    api.downloadPhotos(photo_url)

elif value == 2:
    dist_group = api.getUserGroup(dist['user_id'],dist['access_token'])
    group_id = api.print_list(dist_group)
    dist_albom = api.getAlbums(group_id,dist['access_token'],True)
    album_id = api.print_list(dist_albom)
    list_photo_id = api.getIdPhotos(group_id,album_id,dist['access_token'],True)
    photo_url = api.getByidAll(list_photo_id,group_id,True,dist['access_token'])
    api.downloadPhotos(photo_url)
elif value == 3:
    count = int(input("How many songs to load ? "))
    dist_audio = api.getAudioList(dist['user_id'],dist['access_token'],False,count)
    audio_id = api.print_list_audio(dist_audio)
    audio_url = api.get_Audio_Url(dist['user_id'],dist['access_token'],audio_id)
    api.downloadAudio(audio_url)