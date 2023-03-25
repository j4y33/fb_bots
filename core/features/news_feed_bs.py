import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from actions.scrolling import Scrolling
from core.coordination.navigator_web import Navigator
import base64
from PIL import Image
from io import BytesIO
from logger.selenium_logger import logger


class NewsFeedBS(Scrolling):
    def __init__(self, driver, bot, sql, random_range):
        super().__init__(random_range)
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__image_size = (512, 512)
        self.__random_range = random_range
        self.__navigator = Navigator(self.driver, self.random_range)
        self.__module = 'NewsFeedBS'

    def action(self):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        self.__navigator.home_page()
        logger.info('{0}: Start news feed view: {1}'.format(self.__module, self.__bot[0]))
        time.sleep(self.__random_range.short_wait_range)
        self.scroll_down_limited(self.__random_range.short_wait_range, self.__random_range.short_wait_range,
                                 self.driver)
        self.feed_story()
        time.sleep(self.__random_range.short_wait_range)
        logger.info('{0}: News feed view finish: {1}'.format(self.__module, self.__bot[0]))

    def feed_story(self):
        facebook_src = BeautifulSoup(self.driver.page_source, features="html.parser")
        single = facebook_src.find_all('div', {'data-pagelet': re.compile("^FeedUnit_")})
        post_link = None
        for story in single:
            likes = story.find_all('div', {'aria-label': 'Like'})
            xpath = self.xpath_soup(story)
            story_element = self.driver.find_element_by_xpath(xpath)
            actions = ActionChains(self.driver)
            actions.move_to_element(story_element).perform()
            for like in likes:
                xpath = self.xpath_soup(like)
                like_element = self.driver.find_element_by_xpath(xpath)
                actions.move_to_element(like_element).perform()
                like_element.click()
            links = story.find_all('a', {'role': 'link', 'tabindex': "0"})
            for link in links:
                try:
                    parent = link.find_parent('span')
                    if parent is not None:
                        post_link = link.get('href')
                except:
                    pass
            # Save post_link

    def xpath_soup(self, element):
        """
        Generate xpath from BeautifulSoup4 element.
        :param element: BeautifulSoup4 element.
        :type element: bs4.element.Tag or bs4.element.NavigableString
        :return: xpath as string
        :rtype: str
        Usage
        -----
        """
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name if 1 == len(siblings) else '%s[%d]' % (
                    child.name,
                    next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)

    def get_action_screen(self):
        screenshot = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
        screenshot.thumbnail(self.__image_size, Image.ANTIALIAS)
        img_byte = BytesIO()
        screenshot.save(img_byte, format='PNG')
        encoded_image = base64.b64encode(img_byte.getvalue())
        return encoded_image.decode('utf-8')
