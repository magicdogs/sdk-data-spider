import time
from pyquery import PyQuery as pq

from data import Data
from http_utils import HttpHelper


class XieMiZhe:
    url = 'http://www.xiemizhe.ren/product/index.php'
    data = []

    def __init__(self, name='xiemizhe'):
        self.name = name

    def parser_data(self, html):
        d = pq(html)
        hosts = HttpHelper.get_url_host(self.url)
        for i in d(".cat_list").find("li").items():
            url = hosts + i.find("a").attr("href")
            self.data.append(Data(i.text(),url))

    def save(self, data):
        link_html = HttpHelper.http_get(data["link"])
        attr_url = pq(link_html).find("#warp").find("a").attr("href")
        data["item"].appInfo.append({"app_name": data["text"], "link": attr_url})

    def start(self, thread_pool):
        html = HttpHelper.http_get(self.url)
        self.parser_data(html)
        host = HttpHelper.get_url_host(self.url)
        for item in self.data:
            try:
                sub_html = HttpHelper.http_get(item.url)
                sub_data = pq(sub_html).find(".loan_product ul li")
                for i in sub_data.items():
                    text = i.find(".loan_info").find("h2").text()
                    link = i.find(".imgbox").find("a").attr("href")
                    thread_pool.job_queue.put((self.save, ({"text": text, "link": host + link, "item": item})))
            except Exception as e:
                print(e)
                pass
