import threading
import requests
import pymongo


def get_data(url, headers):
    """
    提取接口数据
    :param url: 分页链接
    :param headers: 请求头
    :return: None
    """
    response = requests.get(url=url, headers=headers, verify=False)
    # 由于返回的是json数据，所以使用json方法保存
    text = response.json()
    feedsInfo = text['data']['feedsInfo']
    for new in feedsInfo:
        # 将文章新闻与视频新闻区分开来
        if new['feedNews']['body']['isVideo']:
            title = new['feedNews']['body']['title']
            print(title, end=' ')
            link = new['feedBase']['algorithmInfo']['doc_id']
            # 请求视频接口
            link = f'https://mlol.qt.qq.com/go/mlol_news/video?docid={link}&favzone=&zone=plat&gameid=3'
            result = requests.get(link, headers, verify=False)
            result = result.json()
            # 如果返回请求错误的信息，则打印错误消息以及result
            try:
                msg = result['msg']
                url = msg['url']
            except Exception as e:
                print('res:\n', result)
                print('请求出现异常:\n', e)
            print(url)
            # 将数据更新到MongoDB中
            col.update_one(
                {'title': title},
                {'$set': {'title': title, 'url': url}},
                upsert=True
            )
        else:
            title = new['feedNews']['body']['title']
            print(title, end=' ')
            url = new['feedBase']['intent']
            print(url)
            # 将数据更新到MongoDB中
            col.update_one(
                {'title': title},
                {'$set': {'title': title, 'url': url}},
                upsert=True
            )


def main():
    """
    主函数
    :return: None
    """
    url = 'https://mlol.qt.qq.com/go/mlol_news/followed_feeds?&favzone=&zone=plat&ip=192.168.1.101&network=4G&slidetype=1&next={}'
    headers = {
        'user-agent': 'QTL/8.0.7 (iPhone; iOS 13.5.1; Scale/2.00)',
        'cookie': 'accountType=1; acctype=; clientType=10',
        'qimei': 'e5e47b7c-340d-4dbd-9d7e-c4e225fbaf04',
    }

    # 使用多线程优化爬取速度
    for t in range(10):
        thread = threading.Thread(target=get_data, args=(url.format(t), headers))
        thread.start()


if __name__ == '__main__':
    # 连接MongoDB
    client = pymongo.MongoClient()
    # 指定数据库
    db = client['lol']
    # 指定集合
    col = db['news']
    # 程序入口
    main()