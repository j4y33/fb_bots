import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config.config import config
from actions.cookies import Cookies
from actions.mimic_type import Mimic
from actions.random_range import RR
from actions.scrolling import Scrolling
from logger.selenium_logger import logger
from core.coordination.navigator_web import Navigator


class QuickLogin(Scrolling, Mimic, Cookies):

    def __init__(self, range_selector):
        super().__init__(range_selector)
        self.driver = None
        self.range_selector = range_selector
        self.__module = 'QuickLogin'

    def action(self, driver, bot):
        self.driver = driver
        driver.get('https://www.google.com/')
        logger.info('{0}: Start'.format(self.__module))
        if bot[6] is not None:
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
              Object.defineProperty(navigator, 'platform', {
                get: () => 'Win32'
              })
            """
            })
            print(bot[6])
            self.add_cookies(driver, json.loads(bot[6]), bot[0])
            time.sleep(1)
            driver.get(config.facebook_page_web)
        logger.info('{0}: Login success: {1}'.format(self.__module, bot[0]))
        time.sleep(self.range_selector.short_wait_range)