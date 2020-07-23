# spider

    这是一些普通的爬虫程序，仅供学习参考。 

## requirements.txt文件

    存放着项目中正在使用或即将使用的依赖库。可使用下述代码安装：

    pip install -r 项目目录/requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com


## jianshu文件夹

jianshu网站的爬虫

- re_jianshu.py

    使用了re模块提取简书接口的部分数据
- redis_jianshu.py

    使用lxml模块进行页面解析，并使用了redis进行了去重操作
- set_jianshu.py

    使用了set集合对url进行去重
- threaning_jianshu.py

   基于生产者消费者模式的多线程爬虫 

## anjvke文件夹

anjvke网站的租房信息爬虫，使用了scrapy框架，并对页面的base64加密进行了破解，最后将取得的房源信息保存到MongoDB中
