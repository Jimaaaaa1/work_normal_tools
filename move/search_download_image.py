

# -*- coding:utf8 -*-
import requests
import json
from urllib import parse
import os
import time

class BaiduImageSpider(object):
    def __init__(self):
        self.json_count = 0  # 请求到的json文件数量（一个json文件包含30个图像文件）
        self.url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=5179920884740494226&ipn=rj&ct' \
                   '=201326592&is=&fp=result&queryWord={' \
                   '}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={' \
                   '}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&nojc=&pn={' \
                   '}&rn=30&gsm=1e&1635054081427= '
        self.directory = "/media/zhd/data/数据/消防通道占用数据/爬取/"  # 存储目录
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30 '
        }

    # 创建存储文件夹
    def create_directory(self, name):
        self.directory = self.directory.format(name)
        # 如果目录不存在则创建
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.directory += '{}'

    # 获取图像链接
    def get_image_link(self, url):
        list_image_link = []
        strhtml = requests.get(url, headers=self.header)  # Get方式获取网页数据
        jsonInfo = json.loads(strhtml.text)
        for index in range(30):
            list_image_link.append(jsonInfo['data'][index]['thumbURL'])
        return list_image_link

    # 下载图片
    def save_image(self, img_link, filename):
        res = requests.get(img_link, headers=self.header)
        if res.status_code == 404:
            print(f"图片{img_link}下载出错------->")
        with open(filename, "wb") as f:
            f.write(res.content)
            print("存储路径：" + filename)

    # 入口函数
    def run(self):
        searchName = input("查询内容：")
        searchName_parse = parse.quote(searchName)  # 编码

        self.create_directory(searchName)

        pic_number = 0  # 图像数量
        for index in range(self.json_count):
            pn = (index+1)*30
            request_url = self.url.format(searchName_parse, searchName_parse, str(pn))
            list_image_link = self.get_image_link(request_url)
            for link in list_image_link:
                pic_number += 1
                self.save_image(link, self.directory.format(str(pic_number)+'.jpg'))
                time.sleep(0.2)  # 休眠0.2秒，防止封ip
        print(searchName+"----图像下载完成--------->")

def BeingSearch():
    # 配置你的 API 密钥和终结点
    API_KEY = 'YOUR_BING_API_KEY'
    ENDPOINT = 'https://api.bing.microsoft.com/v7.0/images/search'

    # 搜索关键词
    query = '吊装'
    # 请求的图片数量
    num_results = 10

    # 设置请求头和请求参数
    headers = {
        'Ocp-Apim-Subscription-Key': API_KEY
    }

    params = {
        'q': query,
        'count': num_results
    }

    # 发起请求并获取响应
    response = requests.get(ENDPOINT, headers=headers, params=params)
    data = response.json()

    # 创建文件夹保存图片
    folder = '吊装图片'
    if not os.path.exists(folder):
        os.makedirs(folder)

    # 解析 JSON 数据并下载图片
    for item in data.get('value', []):
        image_url = item['contentUrl']
        try:
            img_data = requests.get(image_url).content
            img_name = os.path.join(folder, image_url.split('/')[-1])
            with open(img_name, 'wb') as f:
                f.write(img_data)
            print(f'图片下载成功: {img_name}')
        except Exception as e:
            print(f'下载失败: {image_url}, 错误: {e}')


if __name__ == '__main__':
    spider = BaiduImageSpider()
    spider.directory = "/media/zhd/data/数据/起重检测数据/爬取/"
    spider.json_count = 50   # 定义下载100组图像，也就是1500张（每组30张），可以自己修改
    spider.run()

