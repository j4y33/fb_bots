from datetime import datetime


class Tracker:
    def __init__(self, engagement_level, session_time, sql, bot, use_session_settings, use_engagement_levels, date):
        self.__e_level = engagement_level
        self.__s_time = session_time
        self.__use_session_settings = use_session_settings
        self.__use_engagement_levels = use_engagement_levels
        self.__start_date = date
        self.__sql = sql
        self.__bot = bot
        self.__total_actions = 0

    def track_action(self, action_id):
        # Calculate a progress
        self.__total_actions += 1
        running_percent = 0
        if self.__use_session_settings and self.__use_engagement_levels:
            running_percent = self.__total_actions / self.__e_level * 100
        elif self.__use_session_settings:
            time_delta = (datetime.now() - self.__start_date)
            total_seconds = time_delta.total_seconds()
            minutes = int(total_seconds / 60)
            running_percent = minutes / self.__s_time * 100
        else:
            running_percent = self.__total_actions / self.__e_level * 100
        # Update track
        self.__sql.update_track(self.__bot, action_id, int(running_percent))

    def add_new_track(self):
        self.__sql.insert_track(self.__bot, 'login', 0)