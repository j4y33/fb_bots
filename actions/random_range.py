import random


class RR:

    def __init__(self, sql, bot):
        self.__sql = sql
        self.__bot = bot
        self.__dst_id = self.__sql.get_tools_bot_dst_id(self.__bot)
        if self.__dst_id is not None:
            self.__dst_id = self.__dst_id[0]
            self.__account_actions = self.__sql.get_account_actions(self.__dst_id)
        else:
            self.__account_actions = None

        self.__use_session_settings = False
        self.__use_engagement_levels = False

        if self.__account_actions is not None:
            self.__high_percent = self.__account_actions[20]
            self.__middle_percent = self.__account_actions[21]
            self.__low_percent = self.__account_actions[22]
            # Delays
            self.__short_wait_range = [self.__account_actions[30], self.__account_actions[31]]
            self.__medium_wait_range = [self.__account_actions[32], self.__account_actions[33]]
            self.__long_wait_range = [self.__account_actions[34], self.__account_actions[35]]

            if self.__account_actions[23]:
                self.__use_session_settings = self.__account_actions[23]
                self.__long_session_time = [self.__account_actions[24], self.__account_actions[25]]
                self.__medium_session_time = [self.__account_actions[26], self.__account_actions[27]]
                self.__short_session_time = [self.__account_actions[28], self.__account_actions[29]]
            else:
                self.__long_session_time = [15, 20]
                self.__medium_session_time = [10, 15]
                self.__short_session_time = [5, 10]
            if self.__account_actions[36]:
                self.__use_engagement_levels = self.__account_actions[36]
                self.__strong_level = [self.__account_actions[37], self.__account_actions[38]]
                self.__moderate_level = [self.__account_actions[39], self.__account_actions[40]]
                self.__weak_level = [self.__account_actions[41], self.__account_actions[42]]
            else:
                self.__strong_level = [20, 30]
                self.__moderate_level = [10, 20]
                self.__weak_level = [5, 10]
        else:
            self.__high_percent = 5
            self.__middle_percent = 15
            self.__low_percent = 80

            self.__short_wait_range = [2, 4]
            self.__medium_wait_range = [7, 15]
            self.__long_wait_range = [20, 25]

            self.__long_session_time = [15, 20]
            self.__medium_session_time = [10, 15]
            self.__short_session_time = [5, 10]

            self.__strong_level = [20, 30]
            self.__moderate_level = [10, 20]
            self.__weak_level = [5, 10]

    @property
    def dst_id(self):
        return self.__dst_id

    @property
    def high_percent(self):
        return self.__high_percent

    @property
    def middle_percent(self):
        return self.__middle_percent

    @property
    def low_percent(self):
        return self.__low_percent

    @property
    def use_session_settings(self):
        return self.__use_session_settings

    @property
    def use_engagement_levels(self):
        return self.__use_engagement_levels

    @property
    def short_wait_range(self):
        return random.randrange(self.__short_wait_range[0], self.__short_wait_range[1])

    @property
    def medium_wait_range(self):
        return random.randrange(self.__medium_wait_range[0], self.__medium_wait_range[1])

    @property
    def long_wait_range(self):
        return random.randrange(self.__long_wait_range[0], self.__long_wait_range[1])

    @property
    def session_time(self):
        session_time = [random.randrange(self.__long_session_time[0], self.__long_session_time[1]),
                        random.randrange(self.__medium_session_time[0], self.__medium_session_time[1]),
                        random.randrange(self.__short_session_time[0], self.__short_session_time[1])]

        return random.choice(session_time)

    @property
    def engagement_level(self):
        engagement_level = [random.randrange(self.__strong_level[0], self.__strong_level[1]),
                            random.randrange(self.__moderate_level[0], self.__moderate_level[1]),
                            random.randrange(self.__weak_level[0], self.__weak_level[1])]

        return random.choice(engagement_level)
