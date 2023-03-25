# Добавить проверку кол-ва друзей у тех кому мы шлем запрос, так как в начале лучше слать тем у кого много друзей
import time
from actions.scrolling import Scrolling
from core.coordination.navigator_web import Navigator
from logger.selenium_logger import logger


class BotMayKnowFriends(Scrolling):

    def __init__(self, driver, bot, sql):
        super().__init__()
        self.driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__navigator = Navigator(self.driver)
        self.__module = 'BotMayKnowFriends'

    def action(self):
        # Use navigator class for change current page
        logger.info('{0}: Start'.format(self.__module))
        self.__navigator.find_friends_page()
        max_requests = 1
        sent_requests = []
        friends_propose_list = self.driver.find_elements_by_class_name('friendBrowserListUnit')
        for li in friends_propose_list:
            if max_requests == 0:
                break
            add_friend = li.find_elements_by_tag_name('button')
            for button in add_friend:
                if max_requests == 0:
                    break
                if button.text.lower() == 'Add Friend'.lower():
                    time.sleep(self.shirt_range)
                    button.click()
                    max_requests -= 1
                    links = li.find_elements_by_tag_name('a')
                    for a in links:
                        if a.get_attribute("role") == 'presentation':
                           sent_requests.append(a.get_attribute("href"))
                           break

        for item in sent_requests:
            self.__sql.add_friend(self.__bot[0], item, 'sent')
        logger.info('{0}: Finish'.format(self.__module))
