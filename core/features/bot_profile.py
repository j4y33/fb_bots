import time
from actions.cookies import Cookies
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
from logger.selenium_logger import logger


class BotProfile(Scrolling, Mimic, Cookies):

    def __init__(self, driver, bot, sql):
        super().__init__()
        self.__driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__module = 'Profile'

    # About web
    def open_about_info_web(self):
        about = self.__driver.find_elements_by_tag_name("a")
        for info in about:
            if info.text.lower() == "About".lower():
                info.click()
                break
        time.sleep(self.mean_range)
        # Check it!!!
        skip_button = self.__driver.find_elements_by_tag_name("a")
        for skip in skip_button:
            if skip.text.lower() == "Skip".lower():
                time.sleep(self.shirt_range)
                skip.click()
                break
        logger.info('{0}: Open about info success'.format(self.__module))

    # About mobile
    def edit_about_info_mobile(self):
        about = self.__driver.find_elements_by_tag_name("div")
        for info in about:
            if info.text == "See Your About Info":
                time.sleep(self.mean_range)
                info.click()

    # Disable facerecognition
    def face_recognition(self):
        settings = self.__driver.find_elements_by_tag_name("a")
        for element in settings:
            if element.text == "Settings":
                element.click()
                time.sleep(self.mean_range)
                break
        self.scroll_down(self.shirt_range, self.__driver)
        continue_button = self.__driver.find_elements_by_tag_name("span")
        for button in continue_button:
            if button.text == "Continue":
                button.click()
                time.sleep(self.mean_range)
                break
        skip_button = self.__driver.find_elements_by_tag_name("span")
        for button in skip_button:
            if button.text == "Keep Off":
                button.click()
                time.sleep(self.mean_range)
                break
        close_button = self.__driver.find_elements_by_tag_name("span")
        for button in close_button:
            if button.text == "Close":
                button.click()
                time.sleep(self.mean_range)
                break

    # Setup language
    def setup_language_mobile(self):
        time.sleep(self.mean_range)
        self.__driver.get("https://m.facebook.com/language.php?n=%2Fhome.php")
        elem = self.__driver.find_elements_by_tag_name("input")
        for search in elem:
            try:
                time.sleep(self.mean_range)
                self.mimicType(search, "US")
            except:
                logger.info('{0}: Searching for input element'.format(self.__module))
        time.sleep(self.mean_range)
        language = self.__driver.find_element_by_class_name("_d01")
        language.click()
        time.sleep(self.mean_range)
        self.save_cookies(self.__driver, self.__bot[0], self.__sql)
