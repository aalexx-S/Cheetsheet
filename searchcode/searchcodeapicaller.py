import time
import threading
import requests

from .singleton import Singleton


class SearchcodeApiCaller(metaclass=Singleton):
    """
    Singleton class. Call .call() to call http get on an api.
    """

    def __init__(self):
        self.__time = 0
        self.__lock = threading.Lock()

    def call(self, url, timeout=1):
        """
        Inputs:
            url: Http get url.
            timeout: timeout in seconds since last call.
        """
        while True:
            if time.time() < self.__time + timeout:
                time.sleep(self.__time + timeout - time.time())
            else:
                with self.__lock:
                    if time.time() > self.__time + timeout:
                        self.__time = time.time()
                        res = requests.get(url)
                        if res.ok:
                            return res.json()
                        return None

    def __repr__(self):
        return f'SearchcodeApiCaller, singleton class at {hex(id(self))}.'
