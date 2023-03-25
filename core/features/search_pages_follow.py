# Более приоритетно чем групы
import random
import time
from selenium.webdriver.common.keys import Keys
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
from config.config import config
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class BotSearchPagesFollow(Scrolling, Mimic):

    def __init__(self, driver, bot, sql):
        super().__init__()
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.driver)
        self.__module = 'BotSearchPagesFollow'

    def get_last_name(self):
        with open(config.bot_last_names) as bots_file:
            last_names = bots_file.read().splitlines()
        return random.choice(last_names)

    def action(self):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        self.__navigator.home_page()
        search_element = self.driver.find_element_by_name("q")
        self.mimicType(search_element, self.get_last_name())
        time.sleep(self.shirt_range)
        search_element.send_keys(Keys.RETURN)
        time.sleep(self.mean_range)
        top_buttons = self.driver.find_elements_by_tag_name("li")
        for button in top_buttons:
            if button.text.lower() == "Pages".lower():
                time.sleep(self.shirt_range)
                button.click()
                break
        time.sleep(self.mean_range)
        maximum_requests = self.shirt_range
        pages_div = self.driver.find_elements_by_tag_name("div")
        count_pages = self.__sql.count_follow_pages(self.__bot[0])
        for page in pages_div:
            if count_pages[0] >= self.long_range:
                break
            if maximum_requests == 0:
                break
            try:
                if "clearfix".lower() in page.get_attribute('class').lower():
                    links = page.find_elements_by_tag_name("a")
                    for a in links:
                        if a.get_attribute('role').lower() == "presentation".lower():
                            follow_buttons = page.find_elements_by_tag_name("a")
                            for add in follow_buttons:
                                if add.text.lower() == "Follow".lower():
                                    add.click()
                                    maximum_requests -= 1
                                    time.sleep(self.shirt_range)
                                    self.__sql.add_follow_page(self.__bot[0], a.get_attribute('href'))
                                    logger.info('{0}: Bot sent follow request: {1}'
                                                .format(self.__module, self.__bot[0]))
                                    break
                            like_buttons = page.find_elements_by_tag_name("button")
                            for add in like_buttons:
                                if add.text.lower() == "Like".lower():
                                    add.click()
                                    maximum_requests -= 1
                                    time.sleep(self.shirt_range)
                                    self.__sql.add_follow_page(self.__bot[0], a.get_attribute('href'))
                                    logger.info('{0}: Bot sent like request: {1}'
                                                .format(self.__module, self.__bot[0]))
                                    break
                            break
            except Exception as e:
                logger.error('{0}: Warning: {1}'.format(self.__module, e))
        logger.info('{0}: Complete: {1}'.format(self.__module, self.__bot[0]))
        time.sleep(self.shirt_range)
