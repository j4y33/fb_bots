import time
from datetime import datetime
from actions.cookies import Cookies
from browser.browser_properties import BrowserProperties
from config.config import config
from database.bot_sql import BotSql
from logger.selenium_logger import logger
from selenium import webdriver


class BotRunTest(Cookies):

    def __init__(self):
        self._running = True
        self.sql = None
        self.bot = None
        self.__login_status = False
        self.driver = None
        self.__module = "BotRunTest"

    def run(self, bot_core, action, priority):
        if self._running:
            try:
                self.sql = BotSql()
            except Exception as e:
                logger.error('{0}: start bot failed, SQL error: {1}'.format(self.__module, e))
                raise Exception("{0}: start bot failed, SQL error: {1}".format(self.__module ,e))
            self.bot = self.sql.get_bot_test()
            logger.info('{0}: Start bot: {1}'.format(self.__module, self.bot[0]))
            #1. Start browser
            if self.bot is not None:
                chrome_properties = BrowserProperties(disable_web_gl=True, canvas=True,
                                                      web_gl=False, disable_js=False, ua=self.bot[15])
            else:
                chrome_properties = BrowserProperties(disable_web_gl=True, canvas=True,
                                                      web_gl=False, disable_js=False, ua=None)
            chrome_options, ua = chrome_properties.get_driver_options
            self.driver = webdriver.Chrome(executable_path=config.chromedriver, options=chrome_options)
            try:
                bot_core.run(self.bot, self.driver, self.sql, action, priority)
            except Exception as e:
                logger.error('{0}: BotCore Error: {1} message {2}'.format(self.__module, self.bot[0], e))
                raise Exception('{0}: BotCore Error: {1} message {2}'.format(self.__module, self.bot[0], e))
            self.save_cookies(self.driver, self.bot[0], self.sql)
            logger.info('{0}: bot growing success: {1}'.format(self.__module, self.bot[0]))