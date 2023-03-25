import time

from actions.random_range import RR
from logger.selenium_logger import logger


class Navigator(RR):
    def __init__(self):
        super().__init__()
        self.__module = 'Navigator'

    def news_feed(self, driver):
        time.sleep(self.shirt_range)
        logger.info('{0}: navigate to News Feed'.format(self.__module))
        driver.find_element_by_name('News Feed').click()

    def friend_requests(self, driver):
        time.sleep(self.shirt_range)
        logger.info('{0}: navigate to Friend Requests'.format(self.__module))
        driver.find_element_by_name('Friend Requests').click()

    def messages(self, driver):
        time.sleep(self.shirt_range)
        logger.info('{0}: navigate to Messages'.format(self.__module))
        driver.find_element_by_name('Messages').click()

    def notifications(self, driver):
        time.sleep(self.shirt_range)
        logger.info('{0}: navigate to Notifications'.format(self.__module))
        driver.find_element_by_name('Notifications').click()

    def search(self, driver):
        time.sleep(self.shirt_range)
        logger.info('{0}: navigate to Search'.format(self.__module))
        driver.find_element_by_name('Search').click()

    def more(self, driver):
        time.sleep(self.shirt_range)
        logger.info('{0}: navigate to More'.format(self.__module))
        driver.find_element_by_name('More').click()

    def bot_page(self, driver, first_name, last_name):
        logger.info('{0}: navigate to Bot Page'.format(self.__module))
        self.more(driver)
        time.sleep(self.shirt_range)
        links = driver.find_elements_by_tag_name('li')
        for link in links:
            if link.text == '{0} {1}'.format(first_name, last_name):
                link.click()
