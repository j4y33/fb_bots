import random
import time
from selenium.webdriver.common.keys import Keys
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
import base64
from PIL import Image
from io import BytesIO
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class FollowPage(Scrolling, Mimic):

    def __init__(self, driver, bot, sql, random_range):
        super().__init__(random_range)
        self.__driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.__driver, random_range)
        self.__random_range = random_range
        self.__module = 'FollowPage'
        self.__image_size = (512, 512)

    def next_button_click(self, tag_name, button_text):
        submit_buttons = self.__driver.find_elements_by_tag_name(tag_name)
        for button in submit_buttons:
            if button.text == button_text:
                self.__driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(self.__random_range.short_wait_range)
                button.click()
                time.sleep(self.__random_range.short_wait_range)
                return True
        time.sleep(self.__random_range.short_wait_range)
        return False

    def action(self):
        pages = self.__sql.get_extracted_pages_for_join(self.__bot[0], self.__random_range.dst_id)
        if pages:
            link = pages[0][2]
        else:
            return
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        self.__driver.get(link)
        time.sleep(self.__random_range.medium_wait_range)
        self.__driver.find_element_by_xpath("//div[contains(@aria-label,'{0}')]".format('Close chat')).click()
        time.sleep(self.__random_range.medium_wait_range)
        page_name = None
        self.__driver.find_element_by_xpath("//div[contains(@aria-label,'{0}')]".format('Like')).click()
        time.sleep(self.__random_range.short_wait_range)
        # Save to database
        self.__sql.update_extracted_pages_sucess(self.__bot[0], link)
        self.__sql.add_follow_page(self.__bot[0], link)
        logger.info('{0}: Bot sent like request: {1}'
                    .format(self.__module, self.__bot[0]))
        time.sleep(self.__random_range.short_wait_range)

        logger.info('{0}: Finish: {1}'.format(self.__module, self.__bot[0]))

    def get_action_screen(self):
        screenshot = Image.open(BytesIO(self.__driver.get_screenshot_as_png()))
        screenshot.thumbnail(self.__image_size, Image.ANTIALIAS)
        img_byte = BytesIO()
        screenshot.save(img_byte, format='PNG')
        encoded_image = base64.b64encode(img_byte.getvalue())
        return encoded_image.decode('utf-8')
