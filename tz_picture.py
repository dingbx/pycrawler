# coding=utf-8
# 爬取百度贴吧某个帖子里的图片，并存储到以帖子id命名的文件夹中
# 贴吧的图经过缩图，所以从http://imgsrc.baidu.com/forum/pic/item/直接获取
# author: dingbx
# date: 2016-4-2

import urllib2
import urllib
import re
import os


#Description    : 抓取某一帖子图片
class TiebaImgCrawler(object):
    #x为图片编号，webpage为帖子网址
    def __init__(self):
        self.x = 0
        self.webpage = ""
    #获取html页面中的图片并存到path里
    def getImg(self, html, path):
        reg = r'<img class="BDE_Image".+src="(.+?\.jpg)"'    #有时候需要修改正则表达式
        imgre = re.commypile(reg)
        imglist = re.findall(imgre,html)
        for imgurl in imglist:
            bigurl = "http://imgsrc.baidu.com/forum/pic/item/" + imgurl.split('/')[-1]    #获取原图
            print bigurl
            urllib.urlretrieve(bigurl, path+'/%s.jpg' % self.x)
            self.x+=1
    #主函数，循环爬取帖子里的所有页直到最后一页，将图片存在帖子id的文件夹内
    def crawl(self):
        subpage = ""
        nextpagepat = re.compile(r'<a href="(.*)">下一页</a>')
        tzid = self.webpage.split('/')[-1]
        if(os.path.exists(tzid)):
            os.popen('rm -rf ./' + tzid)
        os.mkdir(tzid)
        while (True):
            #webpage = "http://www.baidu.com"
            html = urllib2.urlopen(self.webpage + subpage).read()
            m = re.findall(nextpagepat,html)
            self.getImg(html, tzid)
            if m:
                print m[0].split('?')[1]
                subpage = "?" + m[0].split('?')[1]
            else:
                print "end"
                break

    def setTzpage(self,pag):
        self.webpage = pag


if __name__ == '__main__':
    webpage = "http://tieba.baidu.com/p/2460150866"
    #webpage = "http://tieba.baidu.com/p/4451963977"
    crawler = TiebaImgCrawler()
    crawler.setTzpage(webpage)
    crawler.crawl()