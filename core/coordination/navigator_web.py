import time
from logger.selenium_logger import logger


class Navigator:

    def __init__(self, driver, random_range):
        self.driver = driver
        self.random_range = random_range
        self.__module = 'Navigator'

# Old
    def bot_page(self, first_name):
        time.sleep(self.random_range.short_wait_range)
        try:
            self.driver.find_element_by_xpath("//span[text()='{0}']".format(first_name)).click()
        except Exception as e:
            logger.error('{0}: Error: {1}'.format(self.__module, e))
            raise Exception('{0}: Error: {1}'.format(self.__module, e))
        time.sleep(self.random_range.medium_wait_range)
        logger.info('{0}: navigate to Bot Page: success'.format(self.__module))

# Current
    def home_page(self):
        time.sleep(self.random_range.short_wait_range)
        try:
            self.driver.find_element_by_xpath("//a[contains(@aria-label,'{0}')]".format('Home')).click()
        except Exception as e:
            logger.error('{0}: Error: {1}'.format(self.__module, e))
            raise Exception('{0}: Error: {1}'.format(self.__module, e))
        time.sleep(self.random_range.medium_wait_range)
        logger.info('{0}: navigate to Home Page: success'.format(self.__module))

    def groups_page(self):
        time.sleep(self.random_range.short_wait_range)
        try:
            self.driver.find_element_by_xpath("//a[contains(@aria-label,'{0}')]".format('Groups')).click()
        except Exception as e:
            logger.error('{0}: Error: {1}'.format(self.__module, e))
            raise Exception('{0}: Error: {1}'.format(self.__module, e))
        time.sleep(self.random_range.medium_wait_range)
        logger.info('{0}: navigate to Groups Page: success'.format(self.__module))

# Old
    def find_friends_page(self):
        time.sleep(self.random_range.short_wait_range)
        try:
            self.driver.find_element_by_xpath("//a[text()='{0}']".format('Find Friends')).click()
        except Exception as e:
            logger.error('{0}: Error: {1}'.format(self.__module, e))
            raise Exception('{0}: Error: {1}'.format(self.__module, e))
        time.sleep(self.random_range.medium_wait_range)
        logger.info('{0}: navigate to Find Friends Page: success'.format(self.__module))
