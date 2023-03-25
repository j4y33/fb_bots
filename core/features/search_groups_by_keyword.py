import random
import time
from selenium.webdriver.common.keys import Keys
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
from config.config import config
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class BotSearchGroups(Scrolling, Mimic):

    def __init__(self, driver, bot, sql, image_size):
        super().__init__()
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.driver)
        self.__module = 'BotSearchGroups'
        self.__image_size = image_size

    def next_button_click(self, tag_name, button_text):
        submit_buttons = self.driver.find_elements_by_tag_name(tag_name)
        for button in submit_buttons:
            if button.text == button_text:
                self.driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(self.shirt_range)
                button.click()
                time.sleep(self.shirt_range)
                return True
        time.sleep(self.shirt_range)
        return False

    def action(self, config):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        total_groups_links = []
        print(config[2][0].split(','))
        for keyword in config[2][0].split(','):
            self.__navigator.home_page()
            search_element = self.driver.find_element_by_name("q")
            self.mimicType(search_element, keyword)
            time.sleep(self.shirt_range)
            search_element.send_keys(Keys.RETURN)
            time.sleep(self.mean_range)
            top_buttons = self.driver.find_elements_by_tag_name("li")
            for button in top_buttons:
                if button.text.lower() == "Groups".lower():
                    time.sleep(self.shirt_range)
                    button.click()
                    break
            time.sleep(self.mean_range)
            # Check Public private groups if set opened_groups
            if config[7]:
                self.next_button_click('span', 'Public groups')
                time.sleep(self.mean_range)
            self.scroll_down_limited(pause=self.shirt_range, limit=self.shirt_range, driver=self.driver)
            groups_div = self.driver.find_elements_by_tag_name("div")
            for group in groups_div:
                try:
                    if "clearfix".lower() in group.get_attribute('class').lower():
                        links = group.find_elements_by_tag_name("a")
                        for a in links:
                            if a.get_attribute('role').lower() == "presentation".lower():
                                exclude = False
                                for exclude_keyword in config[3][0].split(','):
                                    if exclude_keyword in a.get_attribute('aria-label'):
                                        exclude = True
                                if not exclude:
                                    print(a.get_attribute('href'))
                                    total_groups_links.append(a.get_attribute('href'))
                                break
                except Exception as e:
                    pass
        for link in total_groups_links:
            self.save_group(link, config)

    def save_group(self, link, config):
        # Check for links in DB
        checked_group = self.__sql.check_group_in_extracted_groups(config[1], link)
        if checked_group is not None:
            logger.info('{0}: Group already exist, skip: {1}'
                        .format(self.__module, link))
            return
        self.driver.get(link)
        time.sleep(self.mean_range)
        # Check privat/public group
        privat = False
        span = self.driver.find_elements_by_tag_name('span')
        for group in span:
            try:
                if group.text == 'Private group':
                    privat = True
            except Exception as e:
                pass
        if privat:
            # Check if opened_groups setuped
            if config[7]:
                logger.info('{0}: Skip privat group: {1}'
                            .format(self.__module, self.__bot[0]))
                return
        else:
            self.next_button_click("span", "About")
            time.sleep(self.mean_range)
        members = None
        activity_today = None
        activity_30 = None
        members_span = self.driver.find_elements_by_tag_name('span')
        for span in members_span:
            if "Members ·" in span.text:
                try:
                    members = span.text.split('Members ·')[1].split(',')
                    members = int(str(members[0]) + str(members[1]))
                    break
                except Exception as e:
                    members = span.text.split('Members ·')[1]
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
                        time.sleep(self.shirt_range)
                    except Exception as e:
                        activity_today = div.text.split('Activity')[1].split('New post today')[0]
                        time.sleep(self.shirt_range)
                    try:
                        activity_30 = div.text.split('New post today')[1].split('in the last 30 days')[0].split(',')
                        activity_30 = int(str(activity_30[0]) + str(activity_30[1]))
                        time.sleep(self.shirt_range)
                    except Exception as e:
                        activity_30 = div.text.split('New post today')[1].split('in the last 30 days')[0]
                        time.sleep(self.shirt_range)
                    break
        # created = self.driver.find_elements_by_class_name('timestamp')
        # for i in created:
        #    div = i.find_element_by_xpath('..')
        #    if div.text == 'Created ':
        #        print(i.get_attribute('title'))
        #        created = i.get_attribute('title')
        #        break
        if int(members) > config[5]:
            self.__sql.save_extracted_groups(dst_id=config[1],
                                             url=link,
                                             members=int(members),
                                             activity_today=int(activity_today),
                                             activity_last_30=int(activity_30),
                                             created=None,
                                             author=None,
                                             joined=None,
                                             access=privat,
                                             admins=None)
            logger.info('{0}: Finish: {1}'
                        .format(self.__module, self.__bot[0]))
        else:
            logger.info('{0}: Group has not enough members, skip: {1}'
                        .format(self.__module, self.__bot[0]))

