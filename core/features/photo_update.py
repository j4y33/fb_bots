import os
import time
import urllib.request
from actions.random_range import RR
from core.coordination.navigator_web import Navigator
from core.selectors.images_selector import ImageSelector
from logger.selenium_logger import logger


class PhotoUpdate(RR):

    def __init__(self, driver, bot, sql):
        super().__init__()
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.driver)
        self.__images = ImageSelector()
        self.__module = 'Profile'

    def action(self):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        avatar = self.__images.get_image(self.__bot[0])
        self.__navigator.bot_page(self.__bot[9])
        time.sleep(self.shirt_range)
        edit_button = self.driver.find_elements_by_tag_name("a")
        for photo in edit_button:
            try:
                if photo.text.lower() == "Edit Profile".lower():
                    photo.click()
                    break
            except Exception as e:
                pass
        time.sleep(self.mean_range)
        photo_button = self.driver.find_elements_by_tag_name("div")
        for button in photo_button:
            try:
                if button.get_attribute("aria-label").lower() == "Update your profile picture".lower():
                    button.click()
                    break
            except Exception as e:
                pass
        time.sleep(self.mean_range)
        upload_input = self.driver.find_elements_by_tag_name("input")
        for i in upload_input:
            if i.get_attribute("title").lower() == "Choose a file to upload".lower():
                photo_file = os.path.join(os.getcwd(), "photo_update.jpg")
                urllib.request.urlretrieve(avatar,
                                           photo_file) # Get image from API
                i.send_keys(photo_file)
        time.sleep(self.long_range)
        save_button = self.driver.find_elements_by_tag_name("button")
        for i in save_button:
            try:
                if i.text.lower() == "Save".lower() and i.get_attribute("type").lower() == "submit":
                    i.click()
            except Exception as e:
                pass
        time.sleep(self.long_range)
        post_button = self.driver.find_elements_by_tag_name("button")
        for i in post_button:
            try:
                if i.text.lower() == "Post".lower() and i.get_attribute("type").lower() == "submit":
                    i.click()
                    self.__sql.update_bot_picture(self.__bot[0], avatar)
            except Exception as e:
                pass
        time.sleep(self.long_range)
        self.driver.refresh()
        time.sleep(self.mean_range)
        self.driver.refresh()
        logger.info('{0}: Update profile photo success'.format(self.__module))