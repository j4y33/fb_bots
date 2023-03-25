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


class JoinGroup(Scrolling, Mimic):

    def __init__(self, driver, bot, sql, random_range):
        super().__init__(random_range)
        self.__driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.__driver, random_range)
        self.__random_range = random_range
        self.__module = 'JoinGroup'
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
        groups = self.__sql.get_extracted_groups_for_join(self.__bot[0], self.__random_range.dst_id)
        if groups:
            link = groups[0][2]
        else:
            return
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        self.__driver.get(link)
        time.sleep(self.__random_range.medium_wait_range)
        exit_status = False
        error_status = False
        group_name = None
        search_group_name = self.__driver.find_elements_by_tag_name("div")
        for a in search_group_name:
            try:
                if a.get_attribute('aria-label') == 'Join Group':
                    time.sleep(self.__random_range.short_wait_range)
                    a.click()
            except Exception as e:
                pass
        time.sleep(self.__random_range.medium_wait_range)
        # Answer questions
        answer_question = self.__driver.find_elements_by_tag_name("span")
        for close in answer_question:
            try:
                if close.text == 'Cancel':
                    logger.info('{0}: Close answer window group: {1}'
                                .format(self.__module, self.__bot[0]))
                    close.click()
                    time.sleep(self.__random_range.medium_wait_range)
                    exit_buttons = self.__driver.find_elements_by_tag_name("div")
                    for exit_button in exit_buttons:
                        try:
                            if exit_button.get_attribute('aria-label') == "Exit":
                                exit_button.click()
                                exit_status = True
                                time.sleep(self.__random_range.short_wait_range)
                                break
                        except Exception as e:
                            pass
                    break
            except Exception as e:
                logger.error('{0}: Warning: {1}'.format(self.__module, e))
        try:
            group_name = self.__driver.find_element_by_name("description").get_attribute('content').split('has')[0]
        except Exception as e:
            logger.error('{0}: Group name error: {1}'
                         .format(self.__module, self.__bot[0]))
        # Save to database
        logger.info('{0}: Start saving to database: {1} error status: {2}, group name: {3}'
                    .format(self.__module, self.__bot[0], error_status, group_name))
        try:
            if error_status:
                self.__sql.update_extracted_groups_error(self.__bot[0], link, exit_status)
            else:
                self.__sql.update_extracted_groups_sucess(self.__bot[0], link, exit_status)
                self.__sql.add_group_page(bot_id=self.__bot[0],
                                          link=link,
                                          group_name=group_name,
                                          status='pending',
                                          screen=self.get_action_screen())
        except Exception as e:
            logger.error('{0}: Warning: {1}'.format(self.__module, e))
        time.sleep(self.__random_range.short_wait_range)
        logger.info('{0}: Finish: {1}'.format(self.__module, self.__bot[0]))

    def get_action_screen(self):
        screenshot = Image.open(BytesIO(self.__driver.get_screenshot_as_png()))
        screenshot.thumbnail(self.__image_size, Image.ANTIALIAS)
        img_byte = BytesIO()
        screenshot.save(img_byte, format='PNG')
        encoded_image = base64.b64encode(img_byte.getvalue())
        return encoded_image.decode('utf-8')

