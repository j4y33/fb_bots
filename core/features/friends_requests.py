import time

from actions.scrolling import Scrolling
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class BotFriendsRequests(Scrolling):

    def __init__(self, driver, bot, sql):
        super().__init__()
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.driver)
        self.__module = 'BotFriendsRequests'

    def action(self):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        self.__navigator.find_friends_page()
        max_requests = 1
        friends_list = self.driver.find_elements_by_tag_name("div")
        for confirm_request in friends_list:
            if max_requests == 0:
                break
            try:
                if 'friendRequestItem'.lower() in confirm_request.get_attribute('class').lower():
                    print("found friendRequestItem")
                    # Click confirm button
                    confirm = confirm_request.find_elements_by_tag_name("button")
                    for button in confirm:
                        print("Start seach for button")
                        if max_requests == 0:
                            break
                        if button.text.lower() == "Confirm".lower():
                            print("Click")
                            button.click()
                            max_requests -= 1
                            a = confirm_request.find_elements_by_tag_name("a")
                            for link in a:
                                if link.get_attribute("aria-hidden") == 'true':
                                    self.__sql.add_friend(self.__bot[0], link.get_attribute("href"), 'confirmed')
                                    break
                            logger.info('{0}: Confirmed a new friend'.format(self.__module))
            except Exception:
                pass
        logger.info('{0}: Confirm finish'.format(self.__module))

