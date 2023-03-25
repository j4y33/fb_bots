import requests
import base64
import io
import sys
from PIL import Image
from io import BytesIO
from pyvirtualdisplay import Display
from actions.cookies import Cookies
from browser.browser_properties import BrowserProperties
from browser.display_properties import DisplayProperties
from config.config import config
from database.bot_sql import BotSql
from logger.selenium_logger import logger
from selenium import webdriver
from tools.vpn_selector import VpnSelector


class BotRun(Cookies):
    def __init__(self):
        self._running = True
        self.sql = None
        self.bot = None
        self.__image_size = 720, 480
        self.__size = None
        self.__ua = None
        self.__login_status = False
        self.driver = None
        self.vpn = None
        self.proxy = None
        self.cookies = None
        self.user_data = None
        self.__vpn_region = None
        self.local_ip = None
        self.public_ip = None
        self.instance_id = None
        self.__module = "BotRun"

    def run(self, bot_core):
        if self._running:
            try:
                self.sql = BotSql()
            except Exception as e:
                self.sql.insert_log(None, '{0}: start bot failed, SQL error: {1}'.format(self.__module, e))
                logger.error('{0}: start bot failed, SQL error: {1}'.format(self.__module, e))
                raise Exception("{0}: start bot failed, SQL error: {1}".format(self.__module, e))
            if sys.platform == 'linux':
                try:
                    self.user_data = requests.get('http://169.254.169.254/latest/user-data').text
                    self.local_ip = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4').text
                    self.public_ip = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4').text
                    self.instance_id = requests.get('http://169.254.169.254/latest/meta-data/instance-id').text
                except Exception as e:
                    self.sql.insert_log(None, 'Get user data failed: {0} message {1}'.format(self.__module, e))
                    raise Exception('Get user data failed: {0} message {1}'.format(self.__module, e))
                self.bot = self.user_data
            else:
                self.bot = '+79913971829'
            try:
                self.bot = self.sql.get_bot_campaign(self.bot)
            except Exception as e:
                self.critical_error(
                    '{0}: get bot from Database failed: {1} message {2}'.format(self.__module, self.bot[0], e),
                    'Get bot from Database failed')
            if self.bot is not None:
                self.sql.update_bot_used_status(self.bot[0], True)
                self.sql.update_bot_instance_details(self.bot[0], self.local_ip, self.public_ip, self.instance_id)
                self.sql.insert_log(self.bot, '{0}: Start bot: {1}'.format(self.__module, self.bot[0]))
                logger.info('{0}: Start bot: {1}'.format(self.__module, self.bot[0]))
            else:
                self.critical_error('{0}: get bot from Database failed: {1}'.format(self.__module, self.bot),
                                    'Get bot from Database failed')
            # Check config
            if config.proxy == 'yes':
                if self.bot is not None:
                    self.proxy = self.bot[29]
                else:
                    self.proxy = None  # Select proxy
            else:
                if sys.platform == 'linux':
                    self.vpn = VpnSelector()
                    if self.bot[2] == 'torguard' or self.bot[2] == 'ipvanish' or self.bot[2] == 'nordvpn':
                        ca = None
                        if self.bot[2] == 'torguard':
                            ca = 'ca.crt'
                        elif self.bot[2] == 'ipvanish':
                            ca = 'ca.ipvanish.com.crt'
                        else:
                            ca = None
                        if self.vpn.connect_to_vpn(self.bot[2], self.bot[3], self.bot[4], self.bot[5], ca, self.bot[0], self.sql):
                            logger.info('{0}: connect to VPN success: {1}'.format(self.__module, self.bot[0]))
                        else:
                            self.critical_error('{0}: connect to VPN failed: {1}'.format(self.__module, self.bot[0]),
                                                'Connect to VPN failed')
                    else:
                        if self.vpn.connect_to_cyberghost(self.bot[3], self.bot[0], self.sql):
                            logger.info('{0}: connect to VPN success: {1}'.format(self.__module, self.bot[0]))
                        else:
                            self.critical_error('{0}: connect to VPN failed: {1}'.format(self.__module, self.bot[0]),
                                                'Connect to VPN failed')
            # Start display
            if sys.platform == 'disabled':
                if self.bot is not None:
                    self.__size = self.bot[16]
                    self.__size = tuple(self.__size.split('(')[1].split(')')[0].split(','))
                else:
                    self.__size = DisplayProperties().get_size()
                display = Display(visible=0, size=self.__size)
                display.start()
                self.__image_size = int(self.bot[16].split('(')[1].split(')')[0].split(',')[0]), int(self.bot[16].split('(')[1].split(')')[0].split(',')[1])
           # 2. Start browser
            try:
                if self.bot[15] is not None:
                    chrome_properties = BrowserProperties(disable_web_gl=True, canvas=True,
                                                          web_gl=False, disable_js=False, ua=self.bot[15])
                else:
                    chrome_properties = BrowserProperties(disable_web_gl=True, canvas=True,
                                                          web_gl=False, disable_js=False, ua=None)
                chrome_options, ua = chrome_properties.get_driver_options
                self.driver = webdriver.Chrome(executable_path=config.chromedriver, options=chrome_options)
                self.sql.update_user_agent(self.bot[0], ua)
            except Exception as e:
                self.critical_error('{0}: Start Browser Filed: {1} message {2}'.format(self.__module, self.bot[0], e),
                                    '{0}'.format(e))
            try:
                bot_core.run(self.bot, self.driver, self.sql, self.__login_status, self.__image_size)
            except Exception as e:
                self.critical_error('{0}: Core Critical Error: {1} message {2}'.format(self.__module, self.bot[0], e),
                                    '{0}'.format(e))
            #self.sql.update_bot_instance_details(self.bot[0], None, None, None)
            self.sql.update_bot_used_status(self.bot[0], False)
            self.save_cookies(self.driver, self.bot[0], self.sql)
            self.sql.update_bot_last_used_date(self.bot[0])
            self.sql.remove_running_bot_from_dst_group(self.bot[0])
            logger.info('{0}: Bot growing success: {1}'.format(self.__module, self.bot[0]))

    def critical_error(self, ex, error):
        logger.error('{0}'.format(ex))
        self.sql.insert_log(self.bot, '{0}'.format(ex))
        decoded_image = None
        try:
            screenshot = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
            screenshot.thumbnail(self.__image_size, Image.ANTIALIAS)
            img_byte = io.BytesIO()
            screenshot.save(img_byte, format='PNG')
            encoded_image = base64.b64encode(img_byte.getvalue())
            decoded_image = encoded_image.decode('utf-8')
        except Exception as e:
            pass
        #self.sql.update_bot_instance_details(self.bot[0], None, None, None)
        self.sql.add_error(self.bot[0], str(error), decoded_image)
        self.sql.remove_running_bot_from_dst_group(self.bot[0])
        self.sql.update_bot_errors(self.bot[0])
        self.sql.update_bot_last_used_date(self.bot[0])
        self.sql.update_bot_used_status(self.bot[0], False)
        raise Exception('{0}'.format(ex))