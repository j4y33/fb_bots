import time

from actions.cookies import Cookies
from actions.random_range import RR
from core.coordination.model import ActionModel
from core.features.login import Login
from core.features.quick_login import QuickLogin


class BotTest(Cookies):
    def __init__(self, driver=None, bot=None, sql=None):
        self.__driver = driver
        self.__bot = bot
        self.__sql = sql
        self.screen = None
        self.__status = False
        self.__module = "Bot"
        self.__current_action = None
        self.__append_next = None
        self.range_selector = None

    def run(self, bot, driver, sql, action, priority):
        self.__driver = driver
        self.__bot = bot
        self.__sql = sql
        self.range_selector = RR(sql, bot)

        action_name = action
        login = QuickLogin(self.range_selector)
        login.action(driver, self.__bot)
        #login = Login(driver, self.__bot, self.__sql, self.range_selector)
        #login.action()
        print('after login')
        self.save_cookies(self.__driver, self.__bot[0], self.__sql)
        actions = ActionModel.get_actions(priority)
        action = actions[action](self.__driver, self.__bot, self.__sql, self.range_selector)
        action.action()
        time.sleep(10000)

        actions = ActionModel.get_actions(priority)
        action = actions[action](self.__driver, self.__bot, self.__sql, self.range_selector)
        groups = self.__sql.get_tools_find_pages(8)
        print(groups)
        for group in groups[4]:
            for i in group.split(','):
                action.action(i, False)