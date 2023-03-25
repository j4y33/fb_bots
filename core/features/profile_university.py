import time
from actions.cookies import Cookies
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class BotUniversity(Scrolling, Mimic, Cookies):

    def __init__(self, driver, bot, sql):
        super().__init__()
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.driver)
        self.__module = 'Profile'

    # About web
    def open_about_info_web(self):
        about = self.driver.find_elements_by_tag_name("a")
        for info in about:
            if info.text.lower() == "About".lower():
                info.click()
                break
        time.sleep(self.mean_range)
        # Check it!!!
        skip_button = self.driver.find_elements_by_tag_name("a")
        for skip in skip_button:
            if skip.text.lower() == "Skip".lower():
                time.sleep(self.shirt_range)
                skip.click()
                break
        logger.info('{0}: Open about info success'.format(self.__module))

    def action(self):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        self.__navigator.bot_page(self.__bot[9])
        self.open_about_info_web()
        time.sleep(self.shirt_range)
        work_and_edu = self.driver.find_elements_by_tag_name("a")
        for info in work_and_edu:
            if info.text.lower() == "Work and Education".lower():
                info.click()
                break
        time.sleep(self.shirt_range)
        college = self.driver.find_elements_by_tag_name("div")
        for info in college:
            if info.text.lower() == "Add a college".lower():
                time.sleep(self.shirt_range)
                info.click()
                break
        time.sleep(self.mean_range)
        school_input = self.driver.find_elements_by_tag_name("input")
        for i in school_input:
            if i.get_attribute("placeholder").lower() == 'What school/university did you attend?'.lower() \
                    and i.get_attribute("type") == 'text':
                try:
                    self.mimicType(i, self.__bot[19])
                    time.sleep(self.shirt_range)
                    self.driver.find_element_by_class_name("_599p").click()
                    break
                except Exception as e:
                    pass
        #Add year to year
        time.sleep(self.shirt_range)
        save_button = self.driver.find_elements_by_tag_name("button")
        for info in save_button:
            if info.text.lower() == "Save Changes".lower():
                time.sleep(self.shirt_range)
                info.click()
                break
        time.sleep(self.mean_range)
        # Click NO for share this as a post
        no_button = self.driver.find_elements_by_tag_name("a")
        for info in no_button:
            if info.text.lower() == "No".lower():
                info.click()
                break
        time.sleep(self.shirt_range)