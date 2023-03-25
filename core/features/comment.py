import time
from actions.scrolling import Scrolling
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger
from selenium.webdriver.common.keys import Keys
import base64
from PIL import Image
from io import BytesIO


class Comment(Scrolling):
    def __init__(self, driver, bot, sql, image_size):
        super().__init__()
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__source = None
        self.__image_size = image_size
        self.__navigator = Navigator(self.driver)
        self.__module = 'Comment'

    def action(self, sources):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        self.__navigator.home_page()
        self.__source = sources
        # Pages
        if sources[2]:
            print(sources[2])
        # Walls
        if sources[3]:
            self.check_exist_on_page()
        # searches
        if sources[4]:
            print(sources[4])
        # groups
        if sources[7]:
            print(sources[7])
        # permalinks
        if sources[8]:
            print(sources[8])
        time.sleep(10000)

    def check_exist_on_page(self):
        likes = 0
        for i in range(self.long_range):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.shirt_range)
            feed_stories = self.driver.find_elements_by_tag_name("div")
            for story in feed_stories:
                comment_status = None
                try:
                    if story.get_attribute('data-testid') is not None:
                        if story.get_attribute('data-testid').lower() == "fbfeed_story".lower():
                            found_keyword = []
                            found_exclude_keyword = []
                            for keyword in self.__source[5]:
                                if keyword in story.text:
                                    found_keyword.append(keyword)
                            for exclude_keyword in self.__source[6]:
                                if exclude_keyword in story.text:
                                    found_exclude_keyword.append(exclude_keyword)
                            if found_keyword is not None and found_exclude_keyword is None:
                                # Like Comment Share Buttons
                                if comment_status is not None:
                                    continue
                                like = story.find_elements_by_tag_name("a")
                                for data in like:
                                    if data.get_attribute('rel') == 'theater' and data.get_attribute('ajaxify') is not None:
                                        check_posted_link = self.__sql.check_post_result(self.__bot[0], data.get_attribute('ajaxify'))
                                        print('Posted link')
                                        print(check_posted_link)
                                        print(data.get_attribute('ajaxify'))
                                        if check_posted_link is not None:
                                            continue
                                        self.driver.execute_script("arguments[0].scrollIntoView();", story)
                                        time.sleep(self.shirt_range)
                                        for button in like:
                                            if button.get_attribute('role') == 'button' \
                                                    and button.text.lower() == 'Like'.lower() \
                                                    and likes < 1:
                                                time.sleep(self.shirt_range)
                                                button.click()
                                                time.sleep(self.shirt_range)
                                                self.__sql.add_action(self.__bot[0], action_priority='base',
                                                                        action_id='like',
                                                                        action_status=True,
                                                                        image=self.get_action_screen())
                                                logger.info('{0}: Click like: {1}'.format(self.__module,
                                                                                            self.__bot[0]))
                                                # Add to post results
                                                self.__sql.add_post_result(bot_id=self.__bot[0],
                                                                            keywords=self.__source[5],
                                                                            exclude_keywords=self.__source[6],
                                                                            posted_link=data.get_attribute(
                                                                                'ajaxify'),
                                                                            action_type="like",
                                                                            story_text=story.text,
                                                                            action_screen=self.get_action_screen())
                                                likes += 1
                                                break
                                        if self.__source[9] is not None and comment_status is None:
                                            comment_buttons = story.find_elements_by_tag_name("span")
                                            for button in comment_buttons:
                                                if button.text.lower() == "Comment".lower():
                                                    print('Found comment button')
                                                    self.driver.execute_script(
                                                        "arguments[0].scrollIntoView();", button)
                                                    time.sleep(self.shirt_range)
                                                    button.click()
                                                    time.sleep(self.shirt_range)
                                                    print('After click comment button')
                                                    break
                                            comment = story.find_elements_by_tag_name("div")
                                            for input in comment:
                                                try:
                                                    if input.get_attribute('aria-label').lower() == "Write a comment...".lower():
                                                        self.driver.execute_script(
                                                            "arguments[0].scrollIntoView();", input)
                                                        time.sleep(self.shirt_range)
                                                        try:
                                                            input.send_keys(self.__source[9])
                                                        except Exception as e:
                                                            print('Error in send text')
                                                        time.sleep(self.shirt_range)
                                                        try:
                                                            input.send_keys(Keys.RETURN)
                                                        except Exception as e:
                                                            print('Error in send enter')
                                                        self.__sql.add_action(self.__bot[0],
                                                                                action_priority='base',
                                                                                action_id='comment',
                                                                                action_status=True,
                                                                                image=self.get_action_screen())
                                                        # Add to post results
                                                        self.__sql.add_post_result(bot_id=self.__bot[0],
                                                                                    keywords=self.__source[5],
                                                                                    exclude_keywords=
                                                                                    self.__source[6],
                                                                                    posted_link=data.get_attribute(
                                                                                        'ajaxify'),
                                                                                    action_type="comment",
                                                                                    story_text=story.text,
                                                                                    action_screen=self.get_action_screen())
                                                        comment_status = 'comment'
                                                        logger.info('{0}: Comment success: {1}'.format(
                                                            self.__module, self.__bot[0]))
                                                        break
                                                except Exception as e:
                                                    pass
                                        time.sleep(self.shirt_range)
                                    logger.info('{0}: Finish: {1}'.format(
                                        self.__module, self.__bot[0]))
                except Exception as e:
                        print(e)

    def get_action_screen(self):
        screenshot = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
        screenshot.thumbnail(self.__image_size, Image.ANTIALIAS)
        img_byte = BytesIO()
        screenshot.save(img_byte, format='PNG')
        encoded_image = base64.b64encode(img_byte.getvalue())
        return encoded_image.decode('utf-8')
