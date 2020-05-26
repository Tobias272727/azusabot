import requests
import re
from urllib.parse import urlencode

from threading import Thread

import re

import time
import random
import hashlib


class pixivic_image_spider:
    def __init__(self, searching_keyword, header = None):
        self.searching_keyword = searching_keyword
        if not header:
            self.header = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                        }
        else:
            self.header = header    
        self.get_random_image
            
    def get_random_image(self):
        page_num = random.randint(1, 10)
        # assign the random number into the para
        params={
              'page': str(page_num),
              'perSize': '30',
              'keyword': self.searching_keyword
          }
        # the api of pxivic
        base_url = 'https://api.pixivic.com/illustrations?'
        #combine the apiurl and keywords
        url = base_url + urlencode(params)
        # requeset
        ret = requests.get(url,headers = self.header)
        response = ret.content.decode()
        print(response)
        # get infomations of images
        img_links = re.findall(r'original.*?\.jpg', response)
        if len(img_links) >= 1:
            image_idx = random.randint(1,len(img_links))
            # get the random pic
            link = img_links[image_idx][:-4]
            
            self.image_loc = self.saveimage(link[11:])    
        else:
            self.image_loc = None
    
    def saveimage(self,link):
        """
        saving pics
        """
        header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "referer" :"https://m.pixivic.com/search/illusts?tag=%E5%85%AC%E4%B8%BB%E8%BF%9E%E7%BB%93&VNK=13a4c3fc" 
        }
        m = hashlib.md5()
        m.update(link.encode())
        name = m.hexdigest()
        link = "https://img.cheerfun.dev:233/c/540x540_70/img-master/img" + link[36:] + "_master1200.jpg"
        print('[INFO]:正在保存图片：' + link)
        ret = requests.get(link,headers = header)
        image_content = ret.content
        filename = 'C:/Users/tobias27/Desktop/CoolQ/data/image/azusabot/' + name + '.jpg'
        file_loc = name + '.jpg'
        
        with open(filename, 'wb') as f:
            f.write(image_content)
            
        print('[INFO]:保存成功，图片名为：{}.jpg'.format(name))
        
        return file_loc

'''
url = "https://m.pixivic.com/search/illusts"
parame = {"tag":"公主连结"}
'''
if __name__ == '__main__':
    spider = pixivic_image_spider('公主连接')
    spider.get_random_image()



