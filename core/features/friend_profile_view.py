import time
from actions.cookies import Cookies
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
from logger.selenium_logger import logger


class FriendsProfileView(Scrolling, Mimic, Cookies):

    def __init__(self, driver, bot, sql):
        super().__init__()
        self.__driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__module = 'FriendsProfileView'

    def action(self):
        about = self.__driver.find_elements_by_tag_name("a")
        for i in about:
            print(i)
