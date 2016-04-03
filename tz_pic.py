# coding=utf-8
# 爬取百度贴吧某个帖子里的图片，并存储到以帖子id命名的文件夹中
# 贴吧的图经过缩图，所以从http://imgsrc.baidu.com/forum/pic/item/直接获取

'''
Script Name     : tz_pic.py
Author          : dingbx
Created         : 2016-04-04
Last Modified   : 
Version         : 1.0
Modifications   : 
Description     : crawl pictures from a Baidu tiezi
Test Environment: Mac OS X 10.11, Python 2.7
'''

import urllib2,urllib
import re
import os,sys
import filter

#Description    : 抓取某一帖子图片
class TiebaImgCrawler(object):
    #x为图片编号，webpage为帖子网址
    def __init__(self, path):
        self.x = 0
        self.webpage = ""
        if path[-1] != '/':
            path = path + '/'
        self.folder = path
    #获取html页面中的图片并存到path里
    def getImg(self, html, path):
        reg = r'<img class="BDE_Image".+src="(.+?\.jpg)"'    #有时候需要修改正则表达式
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        for imgurl in imglist:
            bigurl = "http://imgsrc.baidu.com/forum/pic/item/" + imgurl.split('/')[-1]    #获取原图
            print bigurl
            urllib.urlretrieve(bigurl, path + '/%s.jpg' % self.x)
            if filter.pic_single_filter(path + '/%s.jpg' % self.x):
                self.x+=1
    #主函数，循环爬取帖子里的所有页直到最后一页，将图片存在帖子id的文件夹内
    def crawl(self):
        self.x = 0
        subpage = ""
        nextpagepat = re.compile(r'<a href="(.*)">下一页</a>')   #匹配下一页标签的正则表达式
        tzid = self.webpage.split('/')[-1]  #获取帖子id
        store_path = self.folder + tzid     #根据输入参数中的folder/tzid设置保存路径
        if(os.path.exists(store_path)):
            os.popen('rm -rf '+ store_path)
        os.makedirs(store_path)
        while (True):
            #webpage = "http://www.baidu.com"
            html = urllib2.urlopen(self.webpage + subpage).read()    #获取html页面
            m = re.findall(nextpagepat,html)        #找出所有匹配nextpage的项
            self.getImg(html, store_path)          #保存当前页的所有图片
            if m:    #如果存在下一页，获取下一页的url
                print m[0].split('?')[1]
                subpage = "?" + m[0].split('?')[1]
            else:    #如果不存在下一页，跳出循环
                print "end"
                break
    def setTzPage(self,page):
        self.webpage = page


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: python tz_pic.py http://tieba.baidu.com/p/4451963977 (folder)"
    folder = "./"
    if len(sys.argv) == 3:
        folder = sys.argv[2]
    #判断是否要爬取默认网址（主要测试用）
    if len(sys.argv) > 1:
        webpage = sys.argv[1]
    else:
        yorno = raw_input("Do you want to crawl the default page (http://tieba.baidu.com/p/4451963977)? y/n ")
        if yorno == 'y':
            webpage = "http://tieba.baidu.com/p/4451963977"
        else:
            sys.exit(0)
    crawler = TiebaImgCrawler(folder)   #初始化的同时设置存储路径
    crawler.setTzPage(webpage)  #设置贴子的url
    crawler.crawl()             #开始爬取
    