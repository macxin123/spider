import re
import requests
import fake_useragent


def get_data(text):
    """
    提取页面源码中的信息
    :param text: 页面源代码
    :return: result
    """
    # 生成正则对象
    pattern = re.compile(r'<a class="title" target="_blank" href="(.*?)">(.*?)</a>', re.S)
    # 查找符合上一行正则对象的数据
    result = pattern.finditer(text)

    return result


def show_data(title_and_link):
    """
    展示数据
    :param title_and_link: 数据
    :return: None
    """
    # 重新声明num, judge
    global num

    for i in title_and_link:
        # 打印数据
        print(f'{num}:https://www.jianshu.com{i.group(1).strip()}', end=' ')
        print(i.group(2).strip())
        num += 1
        if num > 10:
            print('完成任务！！！')
            break


def main():
    """
    主函数
    :return: None
    """
    # 实例化UserAgent对象
    user_agent = fake_useragent.UserAgent(use_cache_server=False)
    url = 'https://www.jianshu.com/?seen_snote_ids%5B%5D=66169577&seen_snote_ids%5B%5D=70078184&seen_snote_ids%5B%5D=59133070&seen_snote_ids%5B%5D=71131220&seen_snote_ids%5B%5D=69717831&seen_snote_ids%5B%5D=71082246&seen_snote_ids%5B%5D=69512409&seen_snote_ids%5B%5D=66364233&seen_snote_ids%5B%5D=68425069&seen_snote_ids%5B%5D=65829398&seen_snote_ids%5B%5D=70390517&seen_snote_ids%5B%5D=70715611&seen_snote_ids%5B%5D=60025426&seen_snote_ids%5B%5D=69454619&page={}'
    # 请求头
    headers = {
        # 随机生成1个user-agent
        'User-Agent': user_agent.random,
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': '__yadk_uid=u6WMVsb886ziVwVNJygG7JmmKuendrEN; _ga=GA1.2.1239389295.1589263315; __gads=ID=5214e15cd2d35dd2:T=1590630291:S=ALNI_MbaAmI-lSHf9uc1WiMKghWJUqNdCg; remember_user_token=W1syMTY0MjIzNl0sIiQyYSQxMSRQNHJUcVNLRjQvc3FZNEp1cnoxM2guIiwiMTU5Mzg2OTEzNC41OTQ4MzU4Il0%3D--def1851a75aab60b6b281a296ec3c58d409304ae; read_mode=day; default_font=font2; locale=zh-CN; _m7e_session_core=f0902ed385432c92591ce0155690ffa0; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1593757782,1593826640,1593845543,1593869136; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2221642236%22%2C%22%24device_id%22%3A%2217207797614549-02cc4b55db66dc-d373666-1327104-17207797615b7a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22desktop%22%2C%22%24latest_utm_medium%22%3A%22timeline%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%2C%22first_id%22%3A%2217207797614549-02cc4b55db66dc-d373666-1327104-17207797615b7a%22%7D; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1593871051',
    }
    # 设置代理
    proxies = {
        'http': 'http://54.241.121.74:3128',
        'https': 'http://54.241.121.74:3128',
    }

    # 循环请求页面
    for i in range(10):
        response = requests.get(
            url=url.format(i),
            headers=headers,
            # proxies=proxies
        )
        # 解析页面
        title_and_link = get_data(response.text)
        # 展示数据
        show_data(title_and_link)

        # 如果judge为True，代表已经爬取了1000条数据
        if num > 10:
            break


if __name__ == '__main__':
    num = 1
    main()
