import time
import boto3
from actions.mimic_type import Mimic
from actions.random_range import RR
from actions.scrolling import Scrolling
from core.coordination.navigator_web import Navigator
from selenium.webdriver.common.keys import Keys
from logger.selenium_logger import logger
import base64
from PIL import Image
from io import BytesIO


class Post(Scrolling, Mimic):
    def __init__(self, driver, bot, sql, random_range):
        super().__init__(random_range)
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__image_size = (512,512)
        self.__random_range = random_range
        self.__navigator = Navigator(self.driver, self.random_range)
        self.__module = 'Post'

    def from_s3(self, bucket, key):
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket, key)
        # Check photo or video
        img = Image.open(BytesIO(obj.get()['Body'].read()))
        img.save('/tmp/{0}'.format(key.split('/')[1]))
        return '/tmp/{0}'.format(key.split('/')[1])

    def action(self):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        #self.__sql.update_campaigns_posts_status('publishing', post)

        # Update campaigns errors
        #self.__sql.update_campaigns_posts_status('error', post)
        #self.__sql.update_campaigns_errors(post)

        #self.__sql.update_campaigns_posts(self.__bot[0], content[0])
        post_text = None
        content = None
        post_id = None
        dst_lists = self.__sql.get_campaign_destination_lists(self.__bot[0])
        for dst in dst_lists:
            if post_id is not None:
                break
            all_campaigns = self.__sql.get_campaigns(dst[0])
            for camp in all_campaigns:
                camp_post = self.__sql.get_campaigns_post_by_camp_id(self.__bot[0], camp[0])
                if camp_post:
                    post_id = camp_post[0]
                    post_text = camp_post[2]
                    content = camp_post[3]
                    break
        if post_id is not None:

            self.__navigator.groups_page()
            time.sleep(self.__random_range.medium_wait_range)
            all_links = self.driver.find_elements_by_tag_name("a")
            for element in all_links:
                try:
                    if element.get_attribute('role') == "link" and 'Last active' in element.text:
                        group_name = element.text.split('Last')[0].rstrip()
                        print(group_name)
                        self.__sql.add_group_page(self.__bot[0], element.get_attribute('href'), group_name,
                                                  'joined', self.get_action_screen())
                except Exception as e:
                    pass
            bot_groups = self.__sql.get_groups(self.__bot[0])
            for group in bot_groups:
                print('Post in group')
                not_posted_group = self.__sql.check_campaigns_posts_group(post_id, group[0])
                if not_posted_group is not None:
                    self.driver.get(group[2])
                    time.sleep(self.__random_range.medium_wait_range)
                    self.scroll_up_limited(self.__random_range.short_wait_range, self.__random_range.short_wait_range, self.driver)
                    self.write_post("What's on your mind", post_text, content, group[0], 0, False)
                    self.__sql.update_posted_groups(group[0], post_id)
                    break
            self.__navigator.home_page()
            bot_wall = self.__sql.check_campaigns_posts_walls(post_id, self.__bot[0])
            print(bot_wall)
            if bot_wall is not None:
                self.write_post("What's on your mind", post_text, content, 0, 0, True)
                self.__sql.update_posted_walls(self.__bot[0], post_id)
            logger.info('{0}: Done'.format(self.__module))

    def write_post(self, input_element_text, post, content, group, dst, wall):
        logger.info('{0}: Start write post: {1}'.format(self.__module, self.__bot[0]))
        search_text_in_group = "Write something..."
        search_text_in_wall = "What's on your mind"
        search_text = None
        print(wall)
        if wall:
            search_text = search_text_in_wall
        else:
            search_text = search_text_in_group
        print(search_text)
        post_text_area = self.driver.find_elements_by_tag_name("span")
        for textarea in post_text_area:
            try:
                if input_element_text.lower() in textarea.text.lower():
                    textarea.click()
                    time.sleep(self.__random_range.medium_wait_range)
                    #self.driver.find_element_by_xpath("//div[@aria-label='{0}']".format('Close')).click() # Works
                    #print('works')
                    #textbox = self.driver.find_element_by_xpath("//div[@role='{0}']".format('textbox'))
                    textbox = self.driver.find_elements_by_tag_name("div")
                    for input in textbox:
                        if input.get_attribute('style') == 'white-space: pre-wrap;' and search_text.lower() in input.text.lower():
                            print(input.text.lower())
                            print('send keys')
                            parent = input.find_element_by_xpath('..')
                            final = parent.find_element_by_xpath('..')
                            text_box = final.find_elements_by_tag_name('div')
                            for box in text_box:
                                if box.get_attribute('role') == "textbox":
                                    print('Find text_box')
                                    box.send_keys(post)
                                    break
                            # For future if need fill from without send_keys
                            #self.driver.execute_script("arguments[0].innerText = '{0}'".format(post), final.find_element_by_tag_name("span"))
                            time.sleep(self.__random_range.short_wait_range)
                            break
                    break
            except Exception as e:
                print(e)
        print('Text done')
        if content is not None:
            print('Content is not none')
            label = None
            if wall:
                print("in wall")
                label = self.driver.find_element_by_xpath("//div[@aria-label='{0}']".format('Photo/Video'))
                parent_div = label.find_element_by_xpath('..')
                all_elements = parent_div.find_element_by_xpath('..')
                input = all_elements.find_element_by_tag_name('input')
                input.send_keys(self.from_s3('fbook-content', content))
                time.sleep(self.__random_range.medium_wait_range)
                post_button = self.driver.find_elements_by_tag_name("div")
                for button in post_button:
                    try:
                        if button.get_attribute('role') == 'button' and button.text.lower() == "Post".lower():
                            button.click()
                            break
                    except Exception as e:
                        print(e)
                time.sleep(self.__random_range.medium_wait_range)
            else:
                print('Not in wall')
                label = self.driver.find_element_by_id("toolbarLabel")
                all_elements = label.find_element_by_xpath('..')
                input = all_elements.find_element_by_tag_name('input')
                input.send_keys(self.from_s3('fbook-content', content))
                time.sleep(self.__random_range.medium_wait_range)
                self.driver.find_element_by_xpath("//div[@aria-label='{0}']".format('Post')).click()
                time.sleep(self.__random_range.medium_wait_range)

        logger.info('{0}: Write post finished'.format(self.__module))

    def get_action_screen(self):
        screenshot = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
        screenshot.thumbnail(self.__image_size, Image.ANTIALIAS)
        img_byte = BytesIO()
        screenshot.save(img_byte, format='PNG')
        encoded_image = base64.b64encode(img_byte.getvalue())
        return encoded_image.decode('utf-8')
