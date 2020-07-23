import re
import io
import base64
import random
from fontTools.ttLib import TTFont
from scrapy.http import HtmlResponse
from anjvke.custom_settings import custom_settings


class My_Middleares_Download:
    """自定义下载中间件"""

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(custom_settings.get('PROXY'))

    def process_response(self, request, response, spider):
        pattern = re.compile(r'utf-8;base64,(.*?)\'\)')
        # 使用正则匹配base64字符串
        base64_str = pattern.search(response.text).group(1)
        # 对base64字符串解码
        font_content = base64.b64decode(base64_str)
        # 解析字体库
        font = TTFont(io.BytesIO(font_content))

        # 保存文件
        # font.saveXML('font.xml')
        # font.save('font.woff')

        keys = font.getBestCmap()
        # 创建解码字典
        keys = {hex(k)[2:]: str(int(v[-2:]) - 1) for k, v in keys.items()}
        text = response.text
        # 替换页面源代码
        for k, v in keys.items():
            text = text.replace(f'&#x{k};', v)

        return HtmlResponse(url=request.url, body=text, encoding='utf-8')