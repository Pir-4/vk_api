__author__ = 'valentin'
# -*- coding: utf-8 -*-

import urllib2
import lxml.html
import time
import os
import webbrowser


def chechConnection(): #check the Internet connection
    try:
        response = urllib2.urlopen('http://google.com',timeout=1)
        return  True
    except urllib2.URLError as err: pass
    return False

def downloadWget(url,save_path):

    filename = url[url.rindex("/"):]
    if os.path.exists(save_path+filename):
        print "Ok (repetition)"
        return

    cmd = "wget -P "+ save_path+" "+url
    os.popen(cmd)
    chk = os.path.exists(save_path+filename)
    if chk:
        print("Ok")
    else:
        print("Fail")
def errors(answer):
    err = get_value_tags(answer,"erroe_code")
    err_msg = get_value_tags(answer,"error_msg")

    for i in range(0,len(err)):
        print "Error ###",err[i]," : ",err_msg[i]," ###"

    if len(err) != 0:
        os._exit(0);

def print_list(dist):
    while 1>0:
        i = 1
        for elem in dist:
            str = elem[1]
            print i,":",str
            i += 1
        id = input(":")
        if id < i and id > 0:
            return dist[id-1][0]
        elif id ==0:
            print "Goodbye!!!"
            os._exit(0)
            return 0

def get_value_tags(answer,tag):
    arr_tag = []
    doc = lxml.html.document_fromstring(answer)
    for it in doc.cssselect(str(tag)):
       arr_tag.append(it.text)
    return arr_tag

#******************************************************************
def get_access_tomen(app_id,redirect_url,scope):
    """
    varsion API = 5.35
    """
    print("On the address bar, copy the access token and lifetime and add them to the configuration file")
    url = "https://oauth.vk.com/authorize?"
    url += "client_id=" + app_id
    url += "&display=page"
    url += "&redirect_url="+redirect_url
    url += "&scope="+scope
    url += "&response_type=token&v=5.35"
    webbrowser.open_new_tab(url)
    os._exit(0)

def getAlbums(owner_id,access_token,user_group):
    url = "https://api.vk.com/method/photos.getAlbums.xml?"
    url += "owner_id="
    if user_group:
        url +="-"
    url += str(owner_id)
    url += "&access_token="+access_token

    page = urllib2.urlopen(url)
    answer = page.read()

    errors(answer)

    title = get_value_tags(answer,"title")
    aid = get_value_tags(answer,"aid")

    dist = []
    for i in range(0,len(aid)):
        tmp = []
        tmp.append(aid[i])
        tmp.append(title[i])
        dist.append(tmp)

    return dist

def getUserGroup(user_id,access_token):

    url = "https://api.vk.com/method/groups.get.xml?"
    url += "user_id="+user_id
    url += "&extended=1"
    url += "&access_token="+access_token

    page = urllib2.urlopen(url)
    answer = page.read()

    errors(answer)

    gid = get_value_tags(answer,"gid")
    name = get_value_tags(answer,"name")

    dist = []
    for i in range(0,len(gid)):
         tmp = []
         tmp.append(gid[i])
         tmp.append(name[i])
         dist.append(tmp)

    return dist




def getIdPhotos(owner_id,album_id,access_token,user_group):
    url = "https://api.vk.com/method/photos.get.xml?"
    url += "&owner_id="
    if user_group:
        url +="-"
    url+=str(owner_id)
    url += "&album_id="+album_id
    url += "&access_token="+access_token

    page = urllib2.urlopen(url)
    answer = page.read()

    errors(answer)

    pid = get_value_tags(answer,'pid')

    return pid


def getByid(photo_id,access_token):
    url = "https://api.vk.com/method/photos.getById.xml?"
    url += "&photos="+photo_id
    url += "&access_token="+access_token

    page = urllib2.urlopen(url)
    answer = page.read()

    errors(answer)

    down_url_big = get_value_tags(answer,'src_big')
    down_url_xxbig = get_value_tags(answer,'src_xbig')

    photo_url = down_url_big[0]
    if len(down_url_xxbig) != 0:
        photo_url = down_url_xxbig[0]

    return photo_url

def getPhotosIdString(photo_id,user_id,user_group):
    st = ""
    if user_group:
        st+="-"
    st += str(user_id)+"_"+str(photo_id)

    return st

def getByidAll(list_photo_id,user_id,flag,access_token):

    warring = "It will be downloaded "+str(len(list_photo_id))+" photos. Are you sure? (Y/N)"
    answer = raw_input(warring)
    if answer.lower() == "n":
        print "Goodbye!"
        os._exit(0)

    print("Wait , is getting url to download photos from vk!!!")
    i = 0
    f = 0
    photo_url = []
    for id in list_photo_id:
        i += 1
        f += 1
        st = getPhotosIdString(id,user_id,flag)
        photo_url.append(getByid(st,access_token))
        print f," ++"
        if i == 5:
            time.sleep(3)
            i = 0

    return photo_url

def downloadPhotos(list_url):
    st = os.getcwd()
    s_p = st.rindex("/")
    st = st[:s_p]+"/downloads"

    name = str(raw_input("Enter the name which will be packs downloaded pictures (in English): "))
    save_path = st+"/"+str(name)
    print "save path: ",save_path

    warring = "Ready to start download (Y/N)"
    answer = raw_input(warring)
    if answer.lower() == "n":
        print "Goodbye!"
        os._exit(0)

    for ul in list_url:
        downloadWget(ul,save_path)




#***************** Aufio *************************************

def getAudioList(owner_id,access_token,user_group,count):
    url = "https://api.vk.com/method/audio.get.xml?"
    url += "owner_id="
    if user_group:
        url +="-"
    url += str(owner_id)
    url += "&access_token="+access_token
    url += "&count="+str(count)

    page = urllib2.urlopen(url)
    answer = page.read()

    errors(answer)

    title = get_value_tags(answer,"title")
    aid = get_value_tags(answer,"aid")
    artist = get_value_tags(answer,"artist")

    for i in range(0,len(artist)):
        title[i] = artist[i]+" - "+title[i]

    dist = []
    for i in range(0,len(aid)):
        tmp = []
        tmp.append(aid[i])
        tmp.append(title[i])
        dist.append(tmp)

    return dist

def get_Audio_Url(owner_id,access_token,audio_id):
    url = "https://api.vk.com/method/audio.getById.xml?"
    url += "audios="+str(owner_id)+"_"+str(audio_id)
    url += "&access_token="+access_token

    page = urllib2.urlopen(url)
    answer = page.read()

    errors(answer)
    print answer
    url = get_value_tags(answer,"url")
    title = get_value_tags(answer,"title")
    artist = get_value_tags(answer,"artist")
    audio = []
    for i in range(0,len(url)):
        elem = []
        elem.append(artist[i]+" - "+title[i])
        st = url[i]
        s_end = st.index("?")
        s_start = st.rindex("/",0,s_end)
        s_start = st.rindex(".",s_start,s_end)
        elem.append(st[s_start:s_end])
        elem.append(url[i])
        audio.append(elem)


    return audio


def downloadAudio(audio_url):
    st = os.getcwd()
    s_p = st.rindex("/")
    st = st[:s_p]+"/downloads"

    name = str(raw_input("Enter the name which will be packs downloaded audio (in English): "))
    save_path = st+"/"+str(name)
    print "save path: ",save_path

    warring = "Ready to start download (Y/N)"
    answer = raw_input(warring)
    if answer.lower() == "n":
        print "Goodbye!"
        os._exit(0);

    for elem in audio_url:
        st_e = elem[2].index("?")
        st_s = elem[2].rindex("/",0,st_e)
        filename = elem[2][st_s+1:]

        path_file1 = save_path+"/"+elem[0]+elem[1]
        path_file2 = save_path+"/"+filename

        if(os.path.exists(path_file1) or os.path.exists(path_file2)):
            print "This file exists "
        else:
            downloadWget(elem[2],save_path)

            print filename
            try:
                os.rename(save_path+"/"+filename, save_path+"/"+elem[0]+elem[1])
            except:
                print "You can not rename a file"

