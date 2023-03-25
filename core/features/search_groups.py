import random
import time
from selenium.webdriver.common.keys import Keys
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
from config.config import config
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class BotSearchGroups(Scrolling, Mimic):

    def __init__(self, driver, bot, sql):
        super().__init__()
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.driver)
        self.__module = 'BotSearchGroups'

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
            if button.text.lower() == "Groups".lower():
                time.sleep(self.shirt_range)
                button.click()
                break
        time.sleep(self.mean_range)
        self.scroll_down_limited(self.shirt_range, self.shirt_range, self.driver)
        maximum_requests = self.shirt_range
        groups_div = self.driver.find_elements_by_tag_name("div")
        count_pages = self.__sql.count_groups_pages(self.__bot[0])
        for group in groups_div:
            if count_pages[0] >= self.long_range:
                break
            if maximum_requests == 0:
                break
            try:
                if "clearfix".lower() in group.get_attribute('class').lower():
                    links = group.find_elements_by_tag_name("a")
                    for a in links:
                        if a.get_attribute('role').lower() == "presentation".lower():
                            join_buttons = group.find_elements_by_tag_name("a")
                            for button in join_buttons:
                                try:
                                    if button.text.lower() == "join".lower():
                                        button.click()
                                        time.sleep(self.mean_range)
                                        maximum_requests -= 1
                                        # Answer questions
                                        answer_question = self.driver.find_elements_by_tag_name("span")
                                        for close in answer_question:
                                            try:
                                                if "layerCancel".lower() in close.get_attribute('class').lower():
                                                    logger.info('{0}: Bot sent subscribe request to private group: {1}'
                                                                .format(self.__module, self.__bot[0]))
                                                    close.click()
                                                    time.sleep(self.shirt_range)
                                                    exit_buttons = self.driver.find_elements_by_tag_name("button")
                                                    for exit_button in exit_buttons:
                                                        if exit_button.text.lower() == "Exit".lower():
                                                            exit_button.click()
                                                            time.sleep(self.shirt_range)
                                                            break
                                            except Exception as e:
                                                logger.error('{0}: Warning: {1}'.format(self.__module, e))
                                        self.__sql.add_group_page(self.__bot[0], a.get_attribute('href'))
                                        logger.info('{0}: Bot sent subscribe request: {1}'
                                                    .format(self.__module, self.__bot[0]))
                                        break
                                except Exception as e:
                                    logger.error('{0}: Warning: {1}'.format(self.__module, e))
                            break
            except Exception as e:
                logger.error('{0}: Warning: {1}'.format(self.__module, e))
