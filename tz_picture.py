#coding=utf-8
#爬取百度贴吧某个帖子里的图片，并存储到以帖子id命名的文件夹中
#贴吧的图经过缩图，所以从http://imgsrc.baidu.com/forum/pic/item/直接获取
#不能过滤广告和图标类图片

import urllib2
import urllib
import re
import os


class TiebaImgCrawler(object):
    def __init__(self):
        self.x = 0
        self.webpage = ""
    def getImg(self, html, path):
        reg = r'<img class="BDE_Image".+src="(.+?\.jpg)"'
        imgre = re.commypile(reg)
        imglist = re.findall(imgre,html)
        for imgurl in imglist:
            bigurl = "http://imgsrc.baidu.com/forum/pic/item/" + imgurl.split('/')[-1]
            print bigurl
            urllib.urlretrieve(bigurl, path+'/%s.jpg' % self.x)
            self.x+=1
    
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
            #pat = re.compile('')
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