__author__ = 'valentin'
# -*- coding: utf-8 -*-

import sys
import argparse
import os

def read_config(path):
    try:
        file = open(path,'r')
    except:
        print("file not found")
        return
    lines = file.readlines()
    file.close()
    dist = {}
    for line in lines:
        line = line.replace(' ','')
        line = line.replace('\n','')
        st = line.find("=",0,len(line))
        if st != -1:
            dist[line[:st]]=line[st+1:]

    return dist

def get_path_config():
    usr_conf = "/config/usr_config.txt"
    app_conf = "/config/app_config.txt"
    path = os.getcwd()
    s_p = path.rindex("/")
    app_conf = path[:s_p]+app_conf
    usr_conf = path[:s_p]+usr_conf
    return usr_conf,app_conf

def write_config(namespace):
    path = "*/config.txt"
    file = open(path,'w')
    lines = []
    lines.append('app_id = '+ namespace.app_id)
    lines.append('clinet_secret = '+str(namespace.access_token))
    lines.append('user_id = '+str(namespace.user_mail))
    lines.append('user_pass = '+str(namespace.user_pass))
    lines.append('user_login = '+str(namespace.user_login))

    for line in lines:
        file.write(line+'\n')
    file.close()

def createParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    file_parser = subparsers.add_parser('file')
    file_parser.add_argument ('-r', '--rfile', type=str,
                         default='*/usr_config.txt')
    # file_parser.add_argument ('-w', '--wfile', type=argparse.FileType(mode='w', bufsize=-1),
    #                      default='/my_files/github/download_photo_vk/photo')


    conf_parser = subparsers.add_parser('config')
    conf_parser.add_argument ('--user_id',type = str,default='')
    conf_parser.add_argument ('--user_pass',type = str,default='')
    conf_parser.add_argument ('--app_id',type = str,default='')
    conf_parser.add_argument ('--clinet_secret',type = str,default='')
    conf_parser.add_argument ('--user_login',type = str,default='')

    return parser