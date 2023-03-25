import json
from logger.selenium_logger import logger


class Cookies:

    def save_cookies(self, driver, bot, sql):
        cookies = driver.get_cookies()
        sql.update_bot_cookies(bot, json.dumps(cookies))

    def add_cookies(self, driver, cookies, bot):
        for cookie in cookies:
            print('Add cookie')
            try:
                if isinstance(cookie.get('expiry'), float):
                    cookie['expiry'] = int(cookie['expiry'])
                driver.add_cookie(cookie)
            except Exception as e:
                logger.error('Cookies: Add some cookie error: {0} message: {1}'.format(bot, e))
