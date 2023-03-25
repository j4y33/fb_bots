import random
import time
from selenium.webdriver.common.keys import Keys
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
from config.config import config
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class BotSearchForFriends(Scrolling, Mimic):

    def __init__(self, driver, bot, sql):
        super().__init__()
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.driver)
        self.__module = 'BotSearchForFriends'

    def get_first_name(self):
        with open(config.bot_first_names) as bots_file:
            names = bots_file.read().splitlines()
        return random.choice(names).split(',')

    def get_last_name(self):
        with open(config.bot_last_names) as bots_file:
            last_names = bots_file.read().splitlines()
        return random.choice(last_names)

    def action(self):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        self.__navigator.home_page()
        search_name = "{0} {1}".format(self.get_first_name()[1], self.get_last_name())
        search_element = self.driver.find_element_by_name("q")
        self.mimicType(search_element, search_name)
        time.sleep(self.shirt_range)
        search_element.send_keys(Keys.RETURN)
        time.sleep(self.mean_range)
        top_buttons = self.driver.find_elements_by_tag_name("li")
        for button in top_buttons:
            if button.text.lower() == "People".lower():
                time.sleep(self.shirt_range)
                button.click()
                break
        time.sleep(self.mean_range)
        maximum_requests = 1
        friend_div = self.driver.find_elements_by_tag_name("div")
        for friend in friend_div:
            if maximum_requests == 0:
                break
            try:
                if "clearfix".lower() in friend.get_attribute('class').lower():
                    print("clearfix detected")
                    a = friend.find_elements_by_tag_name("a")

                    for element in a:
                        print(element.get_attribute('role').lower())
                        if element.get_attribute('role').lower() == "presentation".lower():
                            print("role detected")
                            add_buttons = friend.find_elements_by_tag_name("button")
                            for add in add_buttons:
                                if add.text.lower() == "Add Friend".lower() and maximum_requests != 0:
                                    print("add detected")
                                    add.click()
                                    time.sleep(self.shirt_range)
                                    self.__sql.add_friend(self.__bot[0], element.get_attribute('href'), 'sent')
                                    logger.info('{0}: Bot sent a new friend request: {1}'.format(self.__module, self.__bot[0]))
                                    maximum_requests -= 1
                                    break
                            break
            except Exception as e:
                print(e)
        logger.info('{0}: Complete: {1}'.format(self.__module, self.__bot[0]))
        time.sleep(self.shirt_range)