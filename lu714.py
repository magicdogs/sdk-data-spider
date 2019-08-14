from pyquery import PyQuery as pq
from data import Data
import re
from http_utils import HttpHelper


class Lu714:
    url = 'https://www.lu714.com/'
    data = []

    def __init__(self, name='lu714'):
        self.name = name

    def parser_data(self, html):
        d = pq(html)
        hosts = HttpHelper.get_url_host(self.url)
        for i in d("#content p").eq(2).find("a").items():
            url = hosts + i.attr("href")
            self.data.append(Data(i.text(),url))

    @staticmethod
    def save(data):
        # link_html = HttpHelper.http_get(data["link"])
        # attr_url = pq(link_html).find("#warp").find("a").attr("href")
        data["item"].appInfo.append({"app_name": data["text"], "link": data["link"]})

    def start(self, thread_pool):
        html = HttpHelper.http_get(self.url)
        hosts = HttpHelper.get_url_host(self.url)
        self.parser_data(html)
        for item in self.data:
            try:
                sub_html = HttpHelper.http_get(item.url)
                sub_data = pq(sub_html).find("#mrtj a")
                for i in sub_data.items():
                    text = i.text().replace(" ","")
                    mod_text = re.sub(r'-（.*）', "", text)
                    link = hosts + i.attr("href")
                    thread_pool.job_queue.put((Lu714.save, ({"text": mod_text, "link": link, "item": item})))
            except Exception as e:
                print(e)
                pass
