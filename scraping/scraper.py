import sys
import time
import json
import random
import subprocess
from datetime import datetime
from pathlib import Path
from save_photo import SavePhoto
from selenium_logger import logger
from vpn_selector import VpnSelector
from facebook_configuration import config
from save_account_info import SaveAccountInfo
from selenium.webdriver.common.keys import Keys


class FacebookImagesScraper:

    def __init__(self, driver, display, bot_sql):
        self.display = display
        self.driver = driver
        self.links = []
        self.main_account = None
        self.bot = None
        self.bot_sql = bot_sql
        self.vpn = None

    def __del__(self):
        self.driver.quit()
        self.bot_sql.update_bot_used_status(self.bot[0], False)
        self.bot_sql.close()
        if sys.platform == 'linux':
            kill_vpn = subprocess.Popen(["sudo", "killall", "openvpn"])
            kill_vpn.wait()
            self.display.stop()

    def mimicType(self, obj, text, sendReturn=False):
        for char in text:
            obj.send_keys(char)
            time.sleep(random.random())
        if sendReturn == True:
            obj.send_keys(Keys.RETURN)

    def vpn_connect(self, bot):
        if sys.platform == 'linux':
            self.vpn = VpnSelector()
            if bot[2] == 'CyberGhost':
                if self.vpn.check_vpn():
                    return True
                else:
                    vpn_connection = self.vpn.connect_to_cyberghost()
                    return vpn_connection
            else:
                if bot[3] is None:
                    vpn_file = self.vpn.find_vpn_region()
                    vpn_connection = self.vpn.connect_to_rand_vpn(vpn_file)
                    if vpn_connection:
                        self.bot_sql.update_bot_vpn_region(self.bot[0], vpn_file)
                        self.bot_sql.update_bot_last_used_date(self.bot[0])
                    return vpn_connection
                else:
                    vpn_connection = self.vpn.connect_to_vpn(bot[3])
                    self.bot_sql.update_bot_last_used_date(self.bot[0])
                    return vpn_connection
        else:
            return True

    def log_bot_error(self, block_status, exit_status):
        logger.error('Bot error, shutting down...: {0}'.format(self.bot[0]))
        self.bot_sql.update_bot_block_status(self.bot[0], block_status)
        self.bot_sql.update_bot_used_status(self.bot[0], False)
        self.driver.close()
        if sys.platform == 'linux':
            self.display.stop()
            kill_vpn = subprocess.Popen(["sudo", "killall", "openvpn"])
            kill_vpn.wait()
        sys.exit(exit_status)

    def login(self):
        self.bot = self.bot_sql.get_bot()
        if self.bot is None:
            self.bot = self.bot_sql.get_bot_creation_date()
            if self.bot is None:
                self.driver.close()
                self.display.stop()
                kill_vpn = subprocess.Popen(["sudo", "killall", "openvpn"])
                kill_vpn.wait()
                logger.info('No bot in database, stop ...')
                sys.exit(1)
        logger.info('Process bot {0}'.format(self.bot[0]))
        try:
            self.bot_sql.update_bot_used_status(self.bot[0], True)
        except Exception as e:
            logger.error('Update bot used status error {0} {1}'.format(self.bot[0], e))
        if self.vpn_connect(self.bot):
            self.main_account = self.bot[0]
            try:
                self.driver.get(config.facebook_page)
            except Exception as e:
                logger.error('Get main facebook page error {0} {1}'.format(self.bot[0], e))
            if self.bot[6] != "None":
                cookies = json.loads(self.bot[6])
                for cookie in cookies:
                    try:
                        if isinstance(cookie.get('expiry'), float):
                            cookie['expiry'] = int(cookie['expiry'])
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        self.driver.save_screenshot(
                            'debug/Cookies-Error-{}.png'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
                        logger.error('Adding cookies error {0} {1}'.format(self.bot[0], e))
            else:
                try:
                    elem = self.driver.find_element_by_id('m_login_email')
                    elem.click()
                    self.mimicType(elem, self.bot[0], sendReturn=False)
                    elem = self.driver.find_element_by_id('m_login_password')
                    self.mimicType(elem, self.bot[1])
                    elem = self.driver.find_element_by_name('login')
                    elem.click()
                    time.sleep(5)
                except Exception as e:
                    self.driver.save_screenshot(
                        'debug/login-{}.png'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
                    logger.error('Login Failed {0} {1}'.format(self.bot[0], e))
                    self.log_bot_error("vpn error", 1)
            # Setup language
            try:
                time.sleep(random.randrange(3, 7))
                self.driver.get('https://m.facebook.com/home.php')
            except Exception as e:
                self.driver.save_screenshot(
                    'debug/login-{}.png'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
                logger.error('Login Failed {0} {1}'.format(self.bot[0], e))
                self.log_bot_error("blocked before login", 1)
            try:
                time.sleep(random.randrange(3, 7))
                self.driver.get("https://m.facebook.com/language.php?n=%2Fhome.php")
                elem = self.driver.find_elements_by_tag_name("input")
                for search in elem:
                    try:
                        time.sleep(random.randrange(2, 4))
                        self.mimicType(search, "US")
                    except:
                        logger.info('Searching for input element')
                time.sleep(random.randrange(3, 7))
                language = self.driver.find_element_by_class_name("_d01")
                language.click()
                time.sleep(random.randrange(3, 7))
            except Exception as e:
                self.driver.save_screenshot(
                    'debug/login-{}-bot-blocked.png'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
                logger.error('Bot blocked {0} {1}'.format(self.bot[0], e))
                self.log_bot_error("blocked before login", 1)
            logger.info('Login Success'.format(self.bot[0]))
            try:
                cookies = self.driver.get_cookies()
                self.bot_sql.update_bot_cookies(self.bot[0], json.dumps(cookies))
            except Exception as e:
                logger.error('Update bot cookies error {0} {1}'.format(self.bot[0], e))
        else:
            logger.error('Login Failed VPN ERROR {0}'.format(self.bot[0]))
            self.log_bot_error("vpn error", 1)

    def scroll_down(self, start, stop):
        SCROLL_PAUSE_TIME = random.randrange(start, stop)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        error_rate = 0
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                time.sleep(3)
                error_rate = error_rate + 1
                if error_rate > 5:
                    break
            last_height = new_height

    def scroll_down_limited(self, start, stop, limit):
        SCROLL_PAUSE_TIME = random.randint(start, stop)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(limit):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def search(self, name):
        self.driver.get('https://m.facebook.com/friends/center/search')
        time.sleep(1)
        elem = self.driver.find_element_by_name('q')
        self.mimicType(elem, name)
        time.sleep(random.randint(3, 7))
        self.scroll_down_limited(1, 3, 10)
        elem = self.driver.find_elements_by_class_name('darkTouch')
        for link in elem:
            try:
                self.bot_sql.add_account(link.get_attribute("href"), self.main_account, False)
                self.links.append(link.get_attribute("href"))
            except Exception as e:
                logger.error('Victim exist {0}'.format(e))
        time.sleep(random.randrange(3, 7))

    def get_my_friends_list(self):
        self.driver.get('https://m.facebook.com/friends/center/friends')
        try:
            self.scroll_down(5, 15)
            time.sleep(random.randrange(3, 7))
            elem = self.driver.find_elements_by_class_name('darkTouch')
            for link in elem:
                try:
                    self.bot_sql.add_account(link.get_attribute("href"), self.main_account, True)
                except Exception as e:
                    logger.error('Get_my_friends_list SQL duplicate {0} {1}'.format(self.bot[0], e))
        except Exception as e:
            self.driver.save_screenshot(
                'debug/get_my_friends_list-{}.png'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
            logger.error('Get_my_friends_list Failed {0} {1}'.format(self.bot[0], e))
            self.log_bot_error("blocked before login", 1)
        try:
            cookies = self.driver.get_cookies()
            self.bot_sql.update_bot_cookies(self.bot[0], json.dumps(cookies))
        except Exception as e:
            self.driver.save_screenshot(
                'debug/get_my_friends_list-{}.png'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
            logger.error('Get_my_friends_list SQL ERROR {0} {1}'.format(self.bot[0], e))
            self.log_bot_error("active", 1)

    def get_list_of_friends_peer_a(self, storage):
        friends = self.links
        if storage == 'db':
            friends = self.bot_sql.select_my_friends(self.main_account)
        accounts_error = 0
        for friend in friends:
            time.sleep(random.randrange(10, 20))
            if storage == 'db':
                if '&' in friend[0]:
                    find_account = 'https://m.facebook.com/profile.php?v=friends&id={0}'.format(
                        friend[0].split('=')[1].split('&')[0])
                elif '?' in friend[0]:
                    find_account = 'https://m.facebook.com/profile.php?v=friends&id={0}'.format(friend[0].split('=')[1])
                else:
                    find_account = friend[0].split('?')[0] + '/friends'
            else:
                print(friend)
                if '&' in friend:
                    find_account = 'https://m.facebook.com/profile.php?v=friends&id={0}'.format(
                        friend.split('=')[1].split('&')[0])
                else:
                    find_account = friend.split('?')[0] + '/friends'
            try:
                self.driver.get(find_account)
                self.scroll_down(5, 15)
                elem = self.driver.find_elements_by_class_name('darkTouch')
                for link in elem:
                    try:
                        self.bot_sql.add_account(link.get_attribute("href"), self.main_account, False)
                    except Exception as e:
                        logger.error('Get_list_of_friends_peer_a SQL duplicate {0} {1}'.format(self.bot[0], e))
                        self.bot_sql.roll_back()
            except Exception as e:
                self.driver.save_screenshot(
                    'debug/get_list_of_friends_peer_a-{}.png'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
                logger.error('Get_list_of_friends_peer_a Failed {0} {1}'.format(self.bot[0], e))
                accounts_error = accounts_error + 1
                if accounts_error > 10:
                    self.log_bot_error("blocked after scraping", 1)
        cookies = self.driver.get_cookies()
        self.bot_sql.update_bot_cookies(self.bot[0], json.dumps(cookies))

    def get_friends_fotos_web(self, accounts_to_run):
        time.sleep(random.randint(3, 7))
        try:
            self.driver.get('https://m.facebook.com/')
        except Exception as e:
            logger.error('Get main Facebook page Error: {0}'.format(e))
        error_rate = 0
        run_date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        for i in range(accounts_to_run):
            if error_rate == accounts_to_run - 1:
                self.log_bot_error("blocked after scraping", 1)
            #fake action
            time.sleep(random.randint(3, 5))
            try:
                self.driver.get('https://m.facebook.com/friends/center/requests')
                self.scroll_down_limited(1, 3, random.randint(3, 5))
            except Exception as e:
                logger.error('Fake action Error: {0}'.format(e))
            time.sleep(random.randint(3, 5))
            account = self.bot_sql.get_account()
            if account is None:
                logger.error('No available accounts ERROR {0}'.format(e))
                self.log_bot_error("no accounts", 1)

            info = SaveAccountInfo(self.driver)
            photo = SavePhoto(self.driver)
            # Save Account info
            account_name, about_link = info.get_account_name(account)
            about_file = Path('image_data/{0}/{0}.json'.format(account_name))
            if about_file.is_file():
                with open('image_data/{0}/{0}.json'.format(account_name)) as account_file:
                    about_to_json = json.load(account_file)
                    try:
                        total_downloaded_photos = about_to_json['total_downloaded_photos']
                    except Exception as e:
                        logger.error('No information about total photos in json: {0}'.format(e))
                        total_downloaded_photos = 0
            else:
                about_to_json = info.get_info(account)
                total_downloaded_photos = 0
            if about_to_json is not None:
                time.sleep(random.randrange(5, 7))
                try:
                    photo_links, total_photo_with, total_albums = photo.get_photos_links(account)
                    if photo_links == 0:
                        self.bot_sql.set_parsed_status_error(True, account[0])
                        error_rate = error_rate + 1
                        logger.error('No photo links Error')
                        self.driver.save_screenshot('debug/get-photos-link-error{}.png'.format(
                            datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
                        continue
                except Exception as e:
                    logger.error('Scrapper Error: get photos links error {0}'.format(e))
                    self.bot_sql.set_parsed_status_error(True, account[0])
                    error_rate = error_rate + 1
                    continue
                about_to_json['total_photos'] = len(photo_links)
                about_to_json['total_photo_with'] = total_photo_with
                about_to_json['total_albums'] = total_albums
                photos_error_rate = 0
                total_photos = len(photo_links)
                for photo_link in photo_links:
                    try:
                        total_photos = total_photos - 1
                        logger.info('Scrapper Photo: {0} photos left'.format(total_photos))
                        saved_status = photo.save_photo(photo_link.replace('m.facebook.com', 'facebook.com'),
                                                        [account[0], account[1]], self.main_account, run_date)
                        if saved_status:
                            total_downloaded_photos = total_downloaded_photos + 1
                            try:
                                cookies = self.driver.get_cookies()
                                self.bot_sql.update_bot_cookies(self.bot[0], json.dumps(cookies))
                            except Exception as e:
                                self.driver.save_screenshot(
                                    'debug/Save-cookies-error-{}.png'.format(
                                        datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
                                logger.error('Save cookies error {0} {1}'.format(self.bot[0], e))
                    except Exception as e:
                        logger.error('Scrapper Photo Error: {0}'.format(e))
                        # Check vpn connection
                        if self.vpn.check_vpn():
                            logger.info('Check VPN connection success')
                            try:
                                self.driver.save_screenshot('debug/scrapper-photo-error-{}.png'.format(
                                    datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))
                                photos_error_rate += 1
                            except Exception as e:
                                logger.error('Scrapper Photo Error: browser timeout, no screenshot {0}'.format(e))
                                self.driver.refresh()
                            if photos_error_rate > 15:
                                logger.error(
                                    'Scrapper Photo: blocked after scraping, shutting down...: {0}'.format(e))
                                try:
                                    self.bot_sql.set_parsed_status_error(True, account[0])
                                    about_to_json['total_downloaded_photos'] = total_downloaded_photos
                                    self.write_about_to_json(account_name, about_to_json)
                                except Exception as e:
                                    logger.error('Scrapper Photo Error: error in sql or json {0}'.format(e))
                                self.log_bot_error("blocked after scraping", 1)
                        else:
                            logger.error('Scrapper Photo: VPN lost connection: {0}'.format(self.vpn.check_vpn()))
                            vpn_connect = self.vpn.connect_to_vpn()
                            if vpn_connect:
                                logger.info('Scrapper Photo: VPN connection restored {0}'.format(self.vpn.check_vpn()))
                                self.bot_sql.set_parsed_status_error(True, account[0])
                            else:
                                logger.error(
                                    'Scrapper Photo: VPN connection filed, shutting down...: {0}'.format(self.vpn.check_vpn()))
                                self.bot_sql.set_parsed_status_error(True, account[0])
                                about_to_json['total_downloaded_photos'] = total_downloaded_photos
                                self.write_about_to_json(account_name, about_to_json)
                                self.log_bot_error("vpn error", 1)
                    time.sleep(random.randrange(5, 15))
                about_to_json['total_downloaded_photos'] = total_downloaded_photos
                if len(photo_links) != 0:
                    self.write_about_to_json(account_name, about_to_json)
                    try:
                        self.bot_sql.set_parsed_status(True, account[0])
                        logger.info('Bot set_parsed_status success: {}'.format(account[0]))
                        count = self.bot_sql.get_scraped_profiles(self.main_account)
                        logger.info('Bot current accounts scrapped: {}'.format(count[0]))
                        self.bot_sql.update_bot_scraped_profiles(self.main_account, count[0] + 1)
                        logger.info('Scrapper Success! update_bot_scraped_profiles for: {}'.format(account[0]))
                    except Exception as e:
                        logger.error('Scrapper Photo Error: bot SQL Error {0}'.format(e))
                else:
                    self.bot_sql.set_parsed_status(False, account[0])
                    self.bot_sql.set_parsed_status_error(True, account[0])
                    logger.error('Scrapper Error: No photos {0}'.format(account[0]))
                    error_rate = error_rate + 1
            else:
                self.bot_sql.set_parsed_status(False, account[0])
                self.bot_sql.set_parsed_status_error(True, account[0])
                logger.error('Scrapper Error: about info is None')
                error_rate = error_rate + 1


    def write_about_to_json(self, account_name, about_to_json):
        file_name = 'image_data/{0}/{0}.json'.format(account_name)
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(about_to_json, f, ensure_ascii=False)
            f.write("\n")
