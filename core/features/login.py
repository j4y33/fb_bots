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


class Login(Scrolling, Mimic, Cookies):

    def __init__(self, driver, bot, sql, random_range):
        super().__init__(random_range)
        self.__driver = driver
        self.__bot = bot
        self.__sql = sql
        self.random_range = random_range
        self.navigator = None
        self.__module = 'Login'

    def action(self):
        self.navigator = Navigator(self.__driver, self.random_range)
        logger.info('{0}: Start'.format(self.__module))
        # open google page and type facebook before login
        #self.__driver.get('https://www.google.com/')
        # google_query = driver.find_element_by_name('q')
        # self.mimicType(google_query, 'facebook')
        # time.sleep(self.mean_range)
        # google_query.send_keys(Keys.RETURN)
        self.__driver.get(config.facebook_page_web)
        if self.__bot[6] is not None:
            self.__driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
              Object.defineProperty(navigator, 'platform', {
                get: () => 'Win32'
              })
            """
            })
            self.add_cookies(self.__driver, json.loads(self.__bot[6]), self.__bot[0])
            time.sleep(1)
            self.__driver.get(config.facebook_page_web)
        else:
            # Web version
            self.__driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
              Object.defineProperty(navigator, 'platform', {
                get: () => 'Win32'
              })
            """
            })
            self.__driver.get(config.facebook_page_web)
            time.sleep(self.random_range.medium_wait_range)
            submit = self.__driver.find_elements_by_tag_name("button")
            for button in submit:
                try:
                    if button.get_attribute('title') == "Accept All":
                        print('Accept All')
                        time.sleep(self.random_range.short_wait_range)
                        button.click()
                        time.sleep(self.random_range.short_wait_range)
                        break
                except Exception as e:
                    print(e)
            print(self.__driver.execute_script("return navigator.platform"))
            time.sleep(self.random_range.medium_wait_range)
            elem = self.__driver.find_element_by_id('email')
            elem.click()
            time.sleep(self.random_range.short_wait_range)
            self.mimicType(elem, self.__bot[0])
            time.sleep(self.random_range.medium_wait_range)
            pw_elem = self.__driver.find_element_by_id('pass')
            pw_elem.click()
            time.sleep(self.random_range.short_wait_range)
            self.mimicType(pw_elem, self.__bot[1])
            time.sleep(self.random_range.medium_wait_range)
            submit = self.__driver.find_elements_by_tag_name("button")
            for button in submit:
                try:
                    if button.text.lower() == "Log In".lower():
                        time.sleep(1)
                        button.click()
                        time.sleep(self.random_range.medium_wait_range)
                        break
                except Exception as e:
                    print(e)
            time.sleep(self.random_range.medium_wait_range)
        time.sleep(self.random_range.medium_wait_range)
        check_login = None
        try:
            check_login = self.__driver.find_element_by_id('email')
        except Exception as e:
            pass
        if check_login is not None:
            logger.info('{0}: Login not success, trying login/password: {1}'.format(self.__module, self.__bot[0]))
            time.sleep(self.random_range.medium_wait_range)
            submit = self.__driver.find_elements_by_tag_name("button")
            for button in submit:
                try:
                    if button.get_attribute('title') == "Accept All":
                        print('Accept All')
                        time.sleep(self.random_range.short_wait_range)
                        button.click()
                        time.sleep(self.random_range.short_wait_range)
                        break
                except Exception as e:
                    print(e)
            elem = self.__driver.find_element_by_id('email')
            elem.click()
            self.mimicType(elem, self.__bot[0])
            time.sleep(self.random_range.medium_wait_range)
            elem = self.__driver.find_element_by_id('pass')
            elem.click()
            self.mimicType(elem, self.__bot[1])
            time.sleep(self.random_range.medium_wait_range)
            submit = self.__driver.find_elements_by_tag_name("button")
            for button in submit:
                try:
                    if button.text.lower() == "Log In".lower():
                        time.sleep(1)
                        button.click()
                        time.sleep(self.random_range.medium_wait_range)
                        break
                except Exception as e:
                    print(e)
            time.sleep(self.random_range.medium_wait_range)
            check_login = None
            try:
                check_login = self.__driver.find_element_by_id('email')
            except Exception as e:
                pass
            if check_login is not None:
                raise Exception("Login failed: {1}".format(self.__module, self.__bot[0]))
        time.sleep(self.random_range.medium_wait_range)
        try:
            self.navigator.home_page()
        except Exception as e:
            try:
                self.close_introduction()
            except Exception as e:
                pass
            try:
                self.close_terms()
            except Exception as e:
                pass
            try:
                self.change_language()
            except Exception as e:
                pass
            try:
                self.close_introduction()
            except Exception as e:
                self.close_terms()
        self.navigator.home_page()
        logger.info('{0}: Login success: {1}'.format(self.__module, self.__bot[0]))
        time.sleep(self.random_range.short_wait_range)

#<button value="1" class="_42ft _4jy0 _9fws _4jy3 _4jy1 selected _51sy" data-cookiebanner="accept_button" data-testid="cookie-policy-banner-accept" title="Accept All" type="submit" id="u_0_h">Accept All</button>
    def close_terms(self):
        self.next_button_click('button', 'I Accept')
        time.sleep(self.random_range.short_wait_range)
        self.next_button_click('button', 'Close')
        time.sleep(self.random_range.short_wait_range)

    def close_introduction(self):
        self.__driver.find_element_by_xpath("//div[@aria-label='{0}']".format('Next')).click()
        time.sleep(self.random_range.medium_wait_range)
        self.next_button_click('span', 'Get Started')
        time.sleep(self.random_range.medium_wait_range)
        # aria-label="Close introduction"
        self.__driver.find_element_by_xpath("//div[@aria-label='{0}']".format('Close Introduction')).click()
        time.sleep(self.random_range.medium_wait_range)
        self.__driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'platform', {
            get: () => 'Win32'
        })
        """
        })
        self.__driver.get(config.facebook_page_web)
        time.sleep(self.random_range.medium_wait_range)
        try:
            self.__driver.find_element_by_xpath("//div[@aria-label='{0}']".format('Close Introduction')).click()
        except Exception as e:
            pass
        time.sleep(self.random_range.short_wait_range)

    def change_language(self):
        # Change language
        self.__driver.get('https://www.facebook.com/settings?tab=language')
        time.sleep(self.random_range.medium_wait_range)
        #        page_src = self.driver.page_source
        self.__driver.switch_to.frame(self.__driver.find_element_by_tag_name("iframe"))
        time.sleep(self.random_range.short_wait_range)
        self.scroll_down_limited(self.random_range.short_wait_range, self.random_range.short_wait_range, self.__driver)
        self.__driver.find_element_by_xpath("//a[@title='{0}']".format('English (US)')).click()
        time.sleep(self.random_range.short_wait_range)
        self.__driver.get('https://www.facebook.com/')

    def next_button_click(self, tag_name, button_text):
        submit_buttons = self.__driver.find_elements_by_tag_name(tag_name)
        for button in submit_buttons:
            if button.text == button_text:
                self.__driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(self.random_range.short_wait_range)
                button.click()
                print('after click')
                time.sleep(self.random_range.short_wait_range)
        time.sleep(self.random_range.short_wait_range)
