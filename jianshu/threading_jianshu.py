import os
import re
import random
import threading
import requests
import redis
import fake_useragent
from queue import Queue
from bs4 import BeautifulSoup


class Producer(threading.Thread):
    """生产者类"""

    def __init__(self, cli, queue):
        super().__init__()
        self.cli = cli
        self.queue = queue

    def get_html(self):
        """
        获取页面源代码
        :return: response.text/None
        """
        # 获取1个页码
        page = self.queue.get()
        if page:
            # 使用随机的请求头和代理进行页面请求
            response = requests.get(url=url.format(page), headers=random.choice(headers), proxies=random.choice(proxies))
            return response.text
        else:
            return None

    def get_data(self, text):
        """
        生产数据(url)
        :param text: 页面源代码
        :return: None
        """
        soup = BeautifulSoup(text, 'lxml')
        # 找到所有a标签
        a_list = soup.find_all(attrs={'class': 'title'})
        for i in a_list:
            # 提取a标签中的链接
            link = i.attrs['href']
            # 将链接添加到redis集合中
            res = cli.sadd('jianshu:start_urls', link)
            print('res:', res, end=' ')
            print('link:', link)
            if res:
                print('生产了1条数据:', link)

    def run(self):
        """
        生产者线程执行函数
        :return: None
        """
        while True:
            # redis集合中的数据大于1000时结束循环
            if self.cli.scard('jianshu:start_urls') > 1000:
                break
            else:
                res = self.get_html()
                if res is None:
                    continue
                else:
                    self.get_data(res)
        print(f'name:{threading.current_thread().name} is over!!!')


class Consumer(threading.Thread):
    """消费者类"""

    def __init__(self, cli):
        super().__init__()
        self.cli = cli

    def get_data(self):
        """
        二次请求链接
        :return: response.text
        """
        # 从redis集合中随机弹出1个链接
        link = self.cli.spop('jianshu:start_urls')
        if link is None:
            return None
        else:
            url = 'https://www.jianshu.com' + link.decode()
            response = requests.get(url, headers=headers)
            return response.text

    def analysis(self, text):
        """
        获取页面中的需要保存的html
        :param text: 页面源代码
        :return: section
        """
        soup = BeautifulSoup(text, 'lxml')
        # 获取section标签
        section = soup.section
        return section

    def write_in(self, section):
        """
        将获取到的数据保存到本地
        :param section: section标签中的内容
        :return: None
        """
        # 找到section下的所有img标签
        img_list = section.find_all(name='img')
        # 获取文章标题
        h1 = section.h1.string
        for i in sign_list:
            # 文章标题中可能含有特殊字符，在此处使用下划线替换
            h1 = h1.replace(i, '_')
        # 获取section中的html字符串
        html_str = section.decode()
        for img in img_list:
            # 获取图片链接
            href = img.attrs.get('data-original-src')
            if href is None:
                print('i:', img)
                print('href is None')
            else:
                link = 'https:' + href
                res = requests.get(url=link)
                _, name = os.path.split(link)

                # 替换数据
                pattern1 = re.compile(f'data-original-src="{href}"')
                pattern2 = re.compile(f'style="padding-bottom:(.*?);"')
                html_str = pattern1.sub(f'src="./{name}"', html_str)
                html_str = pattern2.sub(f' ', html_str)

                path = f'd:\文档\{h1}'
                if os.path.exists(path):
                    pass
                else:
                    # 如果不存在该文件夹则创建
                    os.makedirs(path)
                # 保存图片
                with open(fr'd:\\文档\\{h1}\\{name}', 'wb') as f:
                    f.write(res.content)
        # 保存markdown
        with open(f'd:\文档\{h1}\{h1}.md', 'w', encoding='utf-8') as f:
            f.write(html_str)
        print('消费了1条数据')

    def run(self):
        """
        消费者线程执行函数
        :return: None
        """
        while True:
            text = self.get_data()
            if text is None:
                continue
            else:
                section = self.analysis(text)
                self.write_in(section)
                # 如果redis集合中没有数据则退出循环
                if self.cli.scard('jianshu:start_urls') == 0:
                    break
        print('大功告成！！！')


if __name__ == '__main__':
    # 连接redis
    cli = redis.Redis()

    # 字符列表
    sign_list = ['/', '\\', ':', '?', '*', '"', '<', '>', '|', ' ']

    # 实例化UserAgent对象
    user_agent = fake_useragent.UserAgent(use_cache_server=False)

    # 创建队列，用于存放页码
    queue = Queue()
    for i in range(1, 1000):
        queue.put(i)

    url = 'https://www.jianshu.com/?seen_snote_ids%5B%5D=73935917&seen_snote_ids%5B%5D=74070184&seen_snote_ids%5B%5D=73970173&seen_snote_ids%5B%5D=72455292&seen_snote_ids%5B%5D=73462800&seen_snote_ids%5B%5D=72763747&seen_snote_ids%5B%5D=74089799&seen_snote_ids%5B%5D=29616525&page={}'

    # 请求头列表
    headers = [
        {
        # 随机生成1个user-agent
        'User-Agent': user_agent.random,
        'Connection': 'keep-alive',
        'Host': 'www.jianshu.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'xxxxxxxxx',
        'X-PJAX': 'true',
        'X-CSRF-Token': 'xxxxxxxxx',
        },
        {
            # 随机生成1个user-agent
            'User-Agent': user_agent.random,
            'Connection': 'keep-alive',
            'Host': 'www.jianshu.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'xxxxxxxxx',
            'X-PJAX': 'true',
            'X-CSRF-Token': 'xxxxxxxxx',
        },
        {
            # 随机生成1个user-agent
            'User-Agent': user_agent.random,
            'Connection': 'keep-alive',
            'Host': 'www.jianshu.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'xxxxxxxxx',
            'X-PJAX': 'true',
            'X-CSRF-Token': 'xxxxxxxxx',
        },
    ]

    # 代理列表
    proxies = [
        {
            'http': 'http://58.220.95.86:9401',
            'https': 'http://58.220.95.86:9401',
        },
        {
            'http': 'http://47.112.221.156:3128',
            'https': 'http://47.112.221.156:3128',
        },
        {
            'http': 'http://218.60.8.99:3129',
            'https': 'http://218.60.8.99:3129',
        }
    ]

    # 线程列表
    thread_list = list()

    # 开启5个生产者线程
    for i in range(5):
        producer = Producer(cli, queue)
        thread_list.append(producer)
        producer.start()

    # 阻塞生产者线程
    for t in thread_list:
        print(t)
        t.join()

    # 开启5个消费者线程
    for j in range(5):
        consumer = Consumer(cli)
        consumer.start()
