import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import config
from actions.cookies import Cookies
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
import base64
from PIL import Image
from io import BytesIO
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class GroupsShare(Scrolling, Mimic, Cookies):

    def __init__(self, driver, bot, sql, random_range):
        super().__init__(random_range)
        self.__driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__image_size = (512, 512)
        self.__navigator = Navigator(self.__driver, random_range)
        self.__random_range = random_range
        self.__module = 'GroupsShare'

    def action(self):
        logger.info('{0}: Start'.format(self.__module))
        links_for_check = []
        self.__driver.get(config.facebook_page_web)
        time.sleep(self.__random_range.medium_wait_range)
        self.__driver.find_element_by_xpath("//span[contains(text(), 'Pages')]").click()
        time.sleep(self.__random_range.medium_wait_range)
        self.__driver.find_element_by_xpath("//span[contains(text(), 'Liked Pages')]").click()
        time.sleep(self.__random_range.medium_wait_range)
        liked_pages = self.__driver.find_elements_by_xpath("//div[contains(@aria-label,'{0}')]".format('Liked'))
        for page in liked_pages:
            a = page.find_element_by_xpath('../..').find_element_by_css_selector('a')
            links_for_check.append(a.get_attribute('href').split('?')[0])
            self.__sql.add_group_page(self.__bot[0],
                                      a.get_attribute('href').split('?')[0])
        # Get bot dst id
        campaign_id = None
        dst = self.__sql.get_campaign_destination_lists(self.__bot[0])
        if dst:
            campaigns = self.__sql.get_campaigns(dst[0][0])
            if campaigns:
                campaign_id = campaigns[0][0]
            else:
                return
        keywords = None
        exclude_keywords = None
        share_posts = self.__sql.get_campaigns_scrap_and_share_posts(campaign_id)
        print(share_posts)
        all_groups = share_posts[3].split('|')
        keywords = share_posts[4].split('|')
        exclude_keywords = share_posts[5].split('|')
        shared_text = share_posts[8].split('|')
        share_to_maximum_groups = share_posts[7]
        if share_to_maximum_groups > 1:
            share_to_maximum_groups = random.randrange(1, share_to_maximum_groups)
        scrap_link = random.choice(all_groups)
        self.__navigator.groups_page()
        time.sleep(self.__random_range.short_wait_range)
        list_of_groups = self.__driver.find_element_by_xpath(
            "//div[contains(@aria-label,'{0}')]".format('List of groups'))
        all_groups_links = list_of_groups.find_elements_by_tag_name('a')
        for link in all_groups_links:
            if 'groups' in link.get_attribute('href') \
                    and 'feed' not in link.get_attribute('href') \
                    and 'notifications' not in link.get_attribute('href') \
                    and 'discover' not in link.get_attribute('href') \
                    and 'create' not in link.get_attribute('href'):
                links_for_check.append(link.get_attribute('href').split('?')[0])
                group_name = None
                span = link.find_elements_by_tag_name('span')
                for element in span:
                    parent = element.find_element_by_xpath('../..')
                    if parent.tag_name == 'span':
                        if 'Last active' not in element.text:
                            group_name = element.text
                self.__sql.add_group_page(self.__bot[0],
                                          link.get_attribute('href').split('?')[0],
                                          group_name,
                                          'joined',
                                          self.get_action_screen())
        # Add check pages
        start_scraping = False  # Change to Flase
        for g in links_for_check:
            if scrap_link in g or g in scrap_link:
                start_scraping = True
        if not start_scraping:
            logger.info('{0}: Nothing to share: {1}'.format(self.__module, self.__bot[0]))
            return
        self.__driver.get(scrap_link)
        time.sleep(self.__random_range.short_wait_range)
        self.scroll_down_limited(self.__random_range.short_wait_range,
                                 self.__random_range.long_wait_range,
                                 self.__driver)
        # find posts
        all_divs = self.__driver.find_elements_by_tag_name('div')
        post_to_share = None
        for div in all_divs:
            if div.get_attribute('aria-posinset'):
                k = False  # Change to false
                for key in keywords:
                    if key in div.text:
                        k = True
                e = False
                for ecl in exclude_keywords:
                    if ecl in div.text:
                        e = True
                post_status = False
                if k and not e:
                    all_a = div.find_elements_by_tag_name('a')
                    for a in all_a:
                        if 'permalink' in a.get_attribute('href') or 'photos' in a.get_attribute('href'):
                            post_status = self.__sql.add_scraped_post(a.get_attribute('href').split('?')[0],
                                                                      campaign_id, self.get_action_screen())
                            if post_status:
                                post_to_share = self.__sql.get_scraped_post(campaign_id,
                                                                            a.get_attribute('href').split('?')[0])
                                break
                    if post_status:
                        break
        # print(post_to_share[1])
        if post_to_share is None:
            post_to_share = self.__sql.check_shared_posts(self.__bot[0], campaign_id)
            if post_to_share is None:
                logger.info('{0}: Nothing to share: {1}'.format(self.__module, self.__bot[0]))
                return
        time.sleep(self.__random_range.short_wait_range)
        self.__driver.get(post_to_share[1])
        time.sleep(self.__random_range.long_wait_range)
        element = WebDriverWait(self.__driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Close chat']")))
        element.click()
        time.sleep(self.__random_range.short_wait_range)
        self.__driver.find_element_by_xpath("//span[text()='Share']").click()
        time.sleep(self.__random_range.medium_wait_range)
        try:
            self.__driver.find_element_by_xpath("//span[contains(text(), 'More Options')]").click()
            time.sleep(self.__random_range.short_wait_range)
        except:
            pass
        self.__driver.find_element_by_xpath("//span[contains(text(), 'Share to a group')]").click()
        time.sleep(self.__random_range.medium_wait_range)
        share_aria = self.__driver.find_element_by_xpath("//div[@aria-label='{0}']".format('Share to a group'))
        write_text = None
        random.shuffle(shared_text)
        for text in shared_text:
            if self.__sql.check_shared_text(text, post_to_share[0]):
                write_text = text
                break
        if write_text is not None:
            text_box = share_aria.find_element_by_xpath("//div[contains(@aria-describedby, 'placeholder')]")
            self.mimicType(text_box, write_text)
            self.__sql.update_shared_text(write_text, post_to_share[0])
        shared_links = []
        for share_maximum in range(share_to_maximum_groups):
            share_buttons = share_aria.find_elements_by_xpath("//div[@aria-label='{0}']".format('Share'))
            for element in share_buttons:
                parent = element.find_element_by_xpath('../../..')
                grand_parent = parent.find_element_by_xpath('../..')
                link = grand_parent.find_element_by_tag_name('a').get_attribute('href').split('?')[0]
                # Check group dst status
                if self.__sql.check_group(self.__bot[0], link) is not None:  # is not
                    element.click()
                    shared_links.append(link)
                    time.sleep(self.__random_range.medium_wait_range)
                    self.__sql.update_scraped_post_group(self.__bot[0], link, post_to_share[0])
                    break
        # Get post url
        for link in shared_links:
            self.__driver.get(link)
            time.sleep(self.__random_range.long_wait_range)
            members_url = self.__driver.find_elements_by_tag_name('a')
            for members_button in members_url:
                if 'members' in members_button.get_attribute('href') and members_button.text == 'Members':
                    members_button.click()
                    break
            time.sleep(self.__random_range.medium_wait_range)
            self.__driver.find_element_by_xpath(
                "//a[contains(text(), '{0} {1}')]".format(self.__bot[9], self.__bot[10])).click()
            time.sleep(self.__random_range.medium_wait_range)
            last_post = self.__driver.find_element_by_xpath("//div[@aria-posinset='1']")
            posts_url = last_post.find_elements_by_tag_name('a')
            for post in posts_url:
                if 'permalink' in post.get_attribute('href') or 'photo' in post.get_attribute('href'):
                    self.__sql.add_liked_post(self.__bot[0], post.get_attribute('href').split('?')[0], campaign_id, self.get_action_screen())
                    break
        logger.info('{0}: Share post done: {1}'.format(self.__module, self.__bot[0]))

    def get_action_screen(self):
        screenshot = Image.open(BytesIO(self.__driver.get_screenshot_as_png()))
        screenshot.thumbnail(self.__image_size, Image.ANTIALIAS)
        img_byte = BytesIO()
        screenshot.save(img_byte, format='PNG')
        encoded_image = base64.b64encode(img_byte.getvalue())
        return encoded_image.decode('utf-8')
