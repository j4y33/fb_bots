import random
import time
from selenium.webdriver.common.keys import Keys
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
from config.config import config
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class BotSearchPagesByLink(Scrolling, Mimic):

    def __init__(self, driver, bot, sql, random_range):
        super().__init__(random_range)
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__random_range = random_range
        self.__image_size = (512, 512)
        self.__module = 'BotSearchPagesByLink'

    def next_button_click(self, tag_name, button_text):
        submit_buttons = self.driver.find_elements_by_tag_name(tag_name)
        for button in submit_buttons:
            if button.text == button_text:
                self.driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(self.__random_range.short_wait_range)
                button.click()
                time.sleep(self.__random_range.short_wait_range)
                return True
        time.sleep(self.__random_range.short_wait_range)
        return False

    def action(self, link, config):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        # Check for links in DB
        self.__sql.save_extracted_pages(dst_id=8,
                                             url=link,
                                             name=None,
                                             likes=None,
                                             follow=None,
                                             bot_error=None)
        return
        self.driver.get(link)
        time.sleep(self.__random_range.short_wait_range)
        # Check privat/public group
        privat = False
        span = self.driver.find_elements_by_tag_name('span')
        for group in span:
            try:
                if 'Private group' in group.text:
                    privat = True
            except Exception as e:
                pass
        if privat:
            # Check if opened_groups setuped
            if config:
                logger.info('{0}: Skip privat group: {1}'
                            .format(self.__module, self.__bot[0]))
                return
        else:
            self.next_button_click("span", "About")
            time.sleep(self.__random_range.short_wait_range)
        members = None
        activity_today = None
        activity_30 = None
        members_span = self.driver.find_elements_by_tag_name('span')
        for span in members_span:
            if "Members ·" in span.text:
                try:
                    members = span.text.split('Members ·')[1].split(',')
                    members = int(str(members[0]) + str(members[1]))
                    time.sleep(self.__random_range.short_wait_range)
                    break
                except Exception as e:
                    members = span.text.split('Members ·')[1]
                    time.sleep(self.__random_range.short_wait_range)
                    break
        activity_div = self.driver.find_elements_by_tag_name('div')
        for div in activity_div:
            try:
                if "New posts today" in div.text:
                    try:
                        activity_today = div.text.split('Activity')[1].split('New posts today')[0].split(',')
                        activity_today = int(str(activity_today[0]) + str(activity_today[1]))
                    except Exception as e:
                        activity_today = div.text.split('Activity')[1].split('New posts today')[0]
                    try:
                        activity_30 = div.text.split('New posts today')[1].split('in the last 30 days')[0].split(',')
                        activity_30 = int(str(activity_30[0]) + str(activity_30[1]))
                    except Exception as e:
                        activity_30 = div.text.split('New posts today')[1].split('in the last 30 days')[0]
                    break
            except Exception as e:
                pass
        if activity_today is None:
            for div in activity_div:
                if "New post today" in div.text:
                    try:
                        activity_today = div.text.split('Activity')[1].split('New post today')[0].split(',')
                        activity_today = int(str(activity_today[0]) + str(activity_today[1]))
                        time.sleep(self.__random_range.short_wait_range)
                    except Exception as e:
                        activity_today = div.text.split('Activity')[1].split('New post today')[0]
                        time.sleep(self.__random_range.short_wait_range)
                    try:
                        activity_30 = div.text.split('New post today')[1].split('in the last 30 days')[0].split(',')
                        activity_30 = int(str(activity_30[0]) + str(activity_30[1]))
                        time.sleep(self.__random_range.short_wait_range)
                    except Exception as e:
                        activity_30 = div.text.split('New post today')[1].split('in the last 30 days')[0]
                        time.sleep(self.__random_range.short_wait_range)
                    break
        #created = self.driver.find_elements_by_class_name('timestamp')
        #for i in created:
        #    div = i.find_element_by_xpath('..')
        #    if div.text == 'Created ':
        #        print(i.get_attribute('title'))
        #        created = i.get_attribute('title')
        #        break
        self.__sql.save_extracted_groups(dst_id=8,
                                             url=link,
                                             members=None,
                                             activity_today=None,
                                             activity_last_30=None,
                                             created=None,
                                             name=None,
                                             bot_error=None,
                                             author=None,
                                             joined=None,
                                             access=privat,
                                             admins=None)
        logger.info('{0}: Finish: {1}'.format(self.__module, self.__bot[0]))
        #else:
        #    logger.info('{0}: Group has not enough members, skip: {1}'
        #                .format(self.__module, self.__bot[0]))
