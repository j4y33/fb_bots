import time
from actions.cookies import Cookies
from actions.mimic_type import Mimic
from actions.scrolling import Scrolling
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class BotCity(Scrolling, Mimic, Cookies):

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
        # Check it on a new bots!!!
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
        places = self.driver.find_elements_by_tag_name("a")
        for info in places:
            if info.text.lower() == "Places you've lived".lower():
                print("Places button clicked")
                info.click()
                break
        time.sleep(self.shirt_range)
        current_city = self.driver.find_elements_by_tag_name("div")
        for info in current_city:
            if info.text.lower() == "Add your current city".lower():
                print("Current city button detected")
                time.sleep(self.shirt_range)
                info.click()
                break
        time.sleep(self.shirt_range)
        cities_input = self.driver.find_elements_by_tag_name("input")
        for i in cities_input:
            if i.text == '' and i.get_attribute("name") != 'q' and i.get_attribute("type") == 'text':
                try:
                    self.mimicType(i, self.__bot[17])
                    time.sleep(self.shirt_range)
                    self.driver.find_element_by_class_name("_599p").click()
                    break
                except Exception as e:
                    pass
        time.sleep(self.mean_range)
        save_button = self.driver.find_elements_by_tag_name("button")
        for info in save_button:
            if info.text.lower() == "Save Changes".lower():
                info.click()
                break
        # Dismiss
        time.sleep(self.mean_range)
        dismiss_button = self.driver.find_elements_by_tag_name("button")
        for info in dismiss_button:
            if info.text.lower() == "Dismiss".lower():
                info.click()
                break
        time.sleep(self.shirt_range)
        logger.info('{0}: Setup city success'.format(self.__module))