import requests, json
from PyQt5.QtCore import QThread, pyqtSignal
from Logger import logger


# https://blog.csdn.net/weixin_45741835/article/details/109590702封装requests
class HTTPThread(QThread):
    '''
        发送请求类，继承线程类
    '''
    respSignal = pyqtSignal(str)
    def __init__(self, url=None, method='GET', data=None, headers=None):
        super(HTTPThread, self).__init__()
        self.url = url
        self.method = method.upper()
        self.data = data
        self.headers = headers

    def run(self):
        # print('开始发送请求')
        if self.method == 'GET':
            response = requests.get(self.url, headers=self.headers)
            logger.info('GET请求,%s' % self.url)
        elif self.method == 'POST':
            response = requests.post(self.url, data=json.dumps(self.data), headers=self.headers)
            logger.info('POST请求,%s' % self.url)
        self.respSignal.emit(response.text)
