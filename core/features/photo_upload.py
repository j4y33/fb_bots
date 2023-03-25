import os
import ssl
import time
import urllib.request
from actions.random_range import RR
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class PhotoUpload(RR):

    def __init__(self, driver, bot, sql):
        super().__init__()
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.driver)
        self.__module = 'PhotoUpload'

    def action(self):
        # Use navigator class for change current page
        #ssl._create_default_https_context = ssl._create_unverified_context # Mac
        logger.info('{0}: Start'.format(self.__module))
        avatar = self.__sql.get_image(self.__bot[0], self.__bot[11])
        self.__navigator.bot_page(self.__bot[9])
        time.sleep(self.shirt_range)
        try:
            self.driver.find_element_by_xpath("//a[text()='Add Photo']").click()
        except Exception as e:
            self.__sql.update_bot_picture(self.__bot[0], avatar)
            logger.info('{0}: Profile photo already exist'.format(self.__module))
            return
        time.sleep(self.mean_range)
        a_tag = self.driver.find_elements_by_tag_name("a")
        for a in a_tag:
            try:
                if a.get_attribute("aria-label").lower() == "Upload Photo".lower():
                    upload_input = a.find_element_by_tag_name("input")
                    logger.info('{0}: Find upload button'.format(self.__module))
                    photo_file = os.path.join(os.getcwd(), "photo.jpg")
                    logger.info('{0}: Download avatar: {1}'.format(self.__module, photo_file))
                    logger.info('{0}: avatar: {1}'.format(self.__module, avatar))
                    urllib.request.urlretrieve(avatar,
                                               photo_file) # Get image from API
                    upload_input.send_keys(photo_file)
                    break
            except Exception as e:
                pass
        time.sleep(self.long_range)
        save_buttons = self.driver.find_elements_by_xpath("//button[text()='Save']")
        for button in save_buttons:
            if button.get_attribute("value") == "1":
                button.click()
                break
        time.sleep(self.long_range)
        self.__sql.update_bot_picture(self.__bot[0], avatar)
        logger.info('{0}: Upload profile photo success'.format(self.__module))
