import random
import time

from selenium.webdriver import ActionChains

from actions.scrolling import Scrolling
from core.coordination.navigator_web import Navigator
import base64
from PIL import Image
from io import BytesIO
from logger.selenium_logger import logger


class NewsFeed(Scrolling):
    def __init__(self, driver, bot, sql, random_range):
        super().__init__(random_range)
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__image_size = (512, 512)
        self.__random_range = random_range
        self.__navigator = Navigator(self.driver, self.random_range)
        self.__module = 'NewsFeed'

    def action(self):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        self.__navigator.home_page()
        time.sleep(self.__random_range.medium_wait_range)
        self.scroll_down_limited(self.__random_range.short_wait_range, self.__random_range.short_wait_range,
                                 self.driver)
        checked = False
        for i in range(self.__random_range.medium_wait_range):
            if random.randint(0, 1) == 0:
                self.scroll_up_limited(self.__random_range.medium_wait_range, self.__random_range.short_wait_range,
                                       self.driver)
            else:
                self.scroll_down_limited(self.__random_range.medium_wait_range, self.__random_range.short_wait_range,
                                         self.driver)
            if not checked:
                self.check_exist_on_page()
                checked = True
            time.sleep(self.__random_range.medium_wait_range)
        logger.info('{0}: News feed view finish: {1}'.format(self.__module, self.__bot[0]))

    def check_exist_on_page(self):
        all_actions = self.__sql.get_like_actions(self.__bot[0], self.__random_range.medium_wait_range)
        for action in all_actions:
            if 'like' in action:
                return
        feed_stories = self.driver.find_elements_by_xpath("//div[contains(@data-pagelet,'{0}')]".format('FeedUnit_'))
        for i in feed_stories:
            if 'aria-posinset' not in i.get_attribute('innerHTML'):
                print('Removed')
                feed_stories.remove(i)
        likes = self.__random_range.short_wait_range
        for like in range(likes):
            story = random.choice(feed_stories)
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(story).perform()
                time.sleep(self.__random_range.medium_wait_range)
                like_button = story.find_element_by_xpath("//div[@aria-label='{0}' "
                                                          "and contains(@role,'{1}')]".format('Like', 'button'))
                self.driver.execute_script("arguments[0].scrollIntoView();", like_button)
                time.sleep(self.__random_range.medium_wait_range)
                actions.move_to_element(like_button).perform()
                like_button.find_element_by_xpath('..').click()
                self.__sql.add_action(self.__bot[0], action_priority='middle', action_id='like',
                                      action_status=True, image=self.get_action_screen())
                feed_stories.remove(story)
                logger.info('{0}: Click like: {1}'.format(self.__module, self.__bot[0]))
            except:
                feed_stories.remove(story)

    def get_action_screen(self):
        screenshot = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
        screenshot.thumbnail(self.__image_size, Image.ANTIALIAS)
        img_byte = BytesIO()
        screenshot.save(img_byte, format='PNG')
        encoded_image = base64.b64encode(img_byte.getvalue())
        return encoded_image.decode('utf-8')
