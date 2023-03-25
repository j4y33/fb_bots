import requests
from config.config import config


class ImageSelector:
    def __init__(self):
        self.__images_url = config.images_url

    def get_list(self, bot_id):
        r = requests.post("{0}?{1}".format(self.__images_url , bot_id))
        return r.json()

    def get_image(self, bot_id) -> str:
        r = requests.post("{0}?{1}".format(self.__images_url , bot_id))
        return r.json()
