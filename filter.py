# -*- coding:UTF-8 -*-
#!/usr/bin/python

'''
Script Name     : deleteSmallImage.py
Author          : svoid
Created         : 2015-03-14
Last Modified   : 2016-4-4 by dingbx
Version         : 1.0
Modifications   : 
Description     : 文件相关操作
Test Environment: Mac OS X 10.11, Python 2.7
'''

import os
import sys
import stat 
import time

#get the files in the dir, rename it as dir/file, return the file list
def get_dir_file(dirname):
    filelist = []
    for file in os.listdir(dirname):
        targetFile = os.path.join(dirname,  file) 
        filelist.append(targetFile)
    return filelist
def get_file_size(filename):
    return os.stat(filename)[stat.ST_SIZE]
#filter a single file
def pic_single_filter(filepath):
    if (get_file_size(filepath) <= 1024*50 and os.path.exists(filepath)) :
        os.remove(filepath)
        print("delete file %s"%(filepath))
        return False
    else:
        print("file is well") 
        return True 
#filter the files in the dir
def pic_folder_filter(dirname):
    filelist = get_dir_file(dirname)
    for file in filelist:
        if (get_file_size(file) <= 1024*50 and os.path.exists(file)) :
            os.remove(file)
            print("delete file %s"%(file))
        else:
            print("file not exists or file is well")