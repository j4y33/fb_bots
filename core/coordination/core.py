import threading
import time
from datetime import datetime

from actions.cookies import Cookies
from actions.random_range import RR
from actions.tracker import Tracker
from core.coordination.action_selector import ActionSelector
from core.coordination.model import ActionModel
from core.features.login import Login
import base64
from PIL import Image
from io import BytesIO

from core.features.quick_login import QuickLogin


class Bot(Cookies):
    def __init__(self, driver=None, bot=None, sql=None):
        super().__init__()
        self.__driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__group_id = None
        self.__dst_id = None
        self.__image_size = None
        self.lock = threading.Lock()
        self.screen = None
        self.__status = False
        self.__module = "Bot"
        self.posts = None
        self.groups = None
        self.__range_selector = None
        self.__current_action = None
        self.__append_next = None
        self.range_selector = None
        self.__action_selector = None

    def run(self, bot, driver, sql, login_status, image_size):
        self.__driver = driver
        self.__bot = bot
        self.__sql = sql
        self.__image_size = image_size
        self.range_selector = RR(sql, bot)
        self.__action_selector = ActionSelector(sql, bot, driver, self.__image_size, self.range_selector)

        if not login_status:
            login = Login(self.__driver, self.__bot, self.__sql, self.range_selector)  # Remove to login
            with self.lock:
                self.__current_action = 'login'
            login.action()
            self.__sql.add_action(self.__bot[0], 'login', 'login', True,
                                  self.get_action_screen())
            self.save_cookies(self.__driver, self.__bot[0], self.__sql)
        with self.lock:
            self.__current_action = None
        self.__sql.update_bot_last_used_date(bot[0])

        engagement_level = self.range_selector.engagement_level
        session_time = self.range_selector.session_time
        tracker = Tracker(engagement_level, session_time, self.__sql, self.__bot,
                          self.range_selector.use_session_settings, self.range_selector.use_engagement_levels,
                          datetime.now())
        tracker.add_new_track()
        while True:
            # Check what algorithm what bot will use or both
            if self.range_selector.use_session_settings and self.range_selector.use_engagement_levels:
                for i in range(engagement_level):
                    if self.__sql.check_bot_used_time(bot[0], session_time) is not None:
                        break
                    self.__action_selector.calculate_action(tracker)
                    self.__sql.update_bot_last_used_date(bot[0])
                break
            elif self.range_selector.use_session_settings:
                if self.__sql.check_bot_used_time(bot[0], session_time) is not None:
                    break
                self.__action_selector.calculate_action(tracker)
                self.__sql.update_bot_last_used_date(bot[0])
            else:
                for i in range(engagement_level):
                    self.__action_selector.calculate_action(tracker)
                    self.__sql.update_bot_last_used_date(bot[0])
                break

    def get_action_screen(self):
        screenshot = Image.open(BytesIO(self.__driver.get_screenshot_as_png()))
        screenshot.thumbnail(self.__image_size, Image.ANTIALIAS)
        img_byte = BytesIO()
        screenshot.save(img_byte, format='PNG')
        encoded_image = base64.b64encode(img_byte.getvalue())
        return encoded_image.decode('utf-8')

    @property
    def get_current_action(self):
        with self.lock:
            return self.__current_action

    @property
    def get_bot_info(self):
        with self.lock:
            return self.__bot

    @property
    def get_main_actions(self):
        with self.lock:
            return ActionModel.get_actions('main')

    @property
    def get_base_actions(self):
        with self.lock:
            return ActionModel.get_actions('base')

    @property
    def get_low_actions(self):
        with self.lock:
            return ActionModel.get_actions('low')

    @property
    def get_profile_actions(self):
        with self.lock:
            return ActionModel.get_actions('profile')

    @property
    def get_screen(self):
        with self.lock:
            return self.__driver.get_screenshot_as_png()

    # SQL
    @property
    def get_friends(self):
        with self.lock:
            return self.__sql.get_friends(self.__bot[0])

    @property
    def get_groups(self):
        with self.lock:
            return self.__sql.get_groups(self.__bot[0])

    @property
    def get_follow(self):
        with self.lock:
            return self.__sql.get_follow(self.__bot[0])

    @property
    def last_actions(self):
        with self.lock:
            return self.__sql.last_actions(self.__bot[0])

    @property
    def last_errors(self):
        with self.lock:
            return self.__sql.last_errors(self.__bot[0])

    def append_action(self, action):
        with self.lock:
            self.__append_next = action
