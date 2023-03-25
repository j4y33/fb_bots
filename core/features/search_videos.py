import random
import time
from selenium.webdriver.common.keys import Keys
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
from config.config import config
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class BotSearchVideos(Scrolling, Mimic):

    def __init__(self, driver, bot, sql):
        super().__init__()
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.driver)
        self.__module = 'BotSearchVideos'

    def get_last_name(self):
        with open(config.bot_last_names) as bots_file:
            last_names = bots_file.read().splitlines()
        return random.choice(last_names)

    def action(self):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        self.__navigator.home_page()
        search_element = self.driver.find_element_by_xpath("//input[@type='search']")
        self.mimicType(search_element, self.get_last_name())
        time.sleep(self.shirt_range)
        search_element.send_keys(Keys.RETURN)
        time.sleep(self.mean_range)
        #top_buttons = self.driver.find_elements_by_tag_name("div")
        #for button in top_buttons:
        #    if button.text.lower() == "Videos".lower():
        #        time.sleep(self.shirt_range)
        #        button.click()
        #        break
        #time.sleep(self.mean_range)
        logger.info('{0}: Videos view success'.format(self.__module))
