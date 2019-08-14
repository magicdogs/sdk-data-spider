from http_utils import HttpHelper
import io
import socket
import re

os_open = io.open("text2.txt", mode="r")

site_set = set([])
for i in os_open.readlines():
    host = HttpHelper.get_url_host(i.replace("\n", ""))
    host_domain = HttpHelper.get_url_host_without_prefix(i.replace("\n", ""))
    site_set.add(host_domain)
    # try:
    #     print(host, "\t", socket.gethostbyname(host_domain))
    # except Exception as e:
    #     pass

for i in site_set:
    mod_text = re.sub(r':\d+', "", i)
    try:
        print(mod_text, "\t", socket.gethostbyname(mod_text))
    except Exception as e:
        pass
