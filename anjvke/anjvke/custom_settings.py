import fake_useragent

user_agent = fake_useragent.UserAgent(use_cache_server=False)

custom_settings = {
    # robots协议
    'ROBOTSTXT_OBEY': False,

    # 请求头
    'DEFAULT_REQUEST_HEADERS':{
        'User-Agent': user_agent.random,
    },

    'PROXY': [
        'https://103.216.51.210:8191',
        'https://223.241.5.60:4216',
        'https://59.110.153.189:80',
    ],

    # 下载中间件
    'DOWNLOADER_MIDDLEWARES' : {
        'anjvke.my_middlewares.My_Middleares_Download': 500,
    },

    # item管道中间件
    'ITEM_PIPELINES': {
        'anjvke.pipelines.MongoPipeline': 300,
    },

    # 数据库url
    'MONGO_URI': 'localhost',

    # mongo数据库
    'MONGO_DATABASE': 'anjvke',
}