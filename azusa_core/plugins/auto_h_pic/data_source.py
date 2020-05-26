import requests
import re
from urllib.parse import urlencode

from threading import Thread
import json
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
        self.get_random_image()
            
    def get_random_image(self):
        page_num = 1
        # assign the random number into the para
        params={
              'page': str(page_num),
              'perSize': '30',
              'keyword':  self.searching_keyword
          }
        # the api of pxivic
        base_url = 'https://api.pixivic.com/illustrations?'
        #combine the apiurl and keywords
        url = base_url + urlencode(params)
        
        # requeset
        ret = requests.get(url,headers = self.header)
        response = ret.content.decode()
        print('openning url:',url,'\n' + self.searching_keyword)
        # uncode json
        re_dict = json.loads(response)
        
        #print(response)
        # get infomations of images
        print('长度',len(re_dict['data']))
        if len(re_dict['data']) == 0:
            self.image_loc = None
        else:
            # get the random pic
            item_idx = random.randint(0, min(10,len(re_dict['data'])-1))
            img_urls = re_dict['data'][item_idx]['imageUrls']
            image_idx = random.randint(0, len(img_urls)-1)
            img_link = img_urls[image_idx]['original']
            print(img_link)
            if len(img_link) > 15:
                link = img_link[:-4]
                self.image_loc = self.saveimage(link)

        
        
          
    
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
    

async def get_auto_h_pic(wife: str) -> str:
    if '老婆' in wife:
        wife = wife.replace('老婆','') 
    spider = pixivic_image_spider(wife)
    if spider.image_loc:
        CQ_str = '[CQ:image,file=azusabot\\' + spider.image_loc+']'
        return CQ_str + '你要的色图，この変態！'
    else:
        return '醒醒，这个' + wife + '不是人类，应该不是你老婆'
    