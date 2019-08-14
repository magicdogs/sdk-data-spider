import requests
from urllib3.util.retry import Retry
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter


session = requests.Session()
retries = Retry(total=5, backoff_factor=0.1,status_forcelist=[500, 502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))


class HttpHelper(object):

    @staticmethod
    def http_get(request_url):
        print("get url request: ", request_url)
        r = session.get(request_url, timeout=2)
        r.encoding = 'utf-8'
        return r.text

    @staticmethod
    def get_url_host(request_url):
        parsed_uri = urlparse(request_url)
        result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return result

    @staticmethod
    def get_url_host_without_prefix(request_url):
        parsed_uri = urlparse(request_url)
        result = '{uri.netloc}'.format(uri=parsed_uri)
        return result

    @staticmethod
    def http_simple_get(request_url):
        print("get url request: ", request_url)
        response = requests.get(request_url, timeout=1)
        response.encoding = "utf-8"
        return response

    @staticmethod
    def test_http():
        url = 'http://www.xiemizhe.ren/product/index.php'
        for i in range(0, 100):
            HttpHelper.http_get(url)


# HttpHelper.test_http()
