import time
import json
import random
import string
import secrets
import calendar
import requests
from selenium.webdriver.common.keys import Keys
from actions.mimic_type import Mimic
from datetime import datetime
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from actions.random_range import RR
from config.config import config
from logger.selenium_logger import logger
from registration.location_generator import LocationGenerator
from tools.sms_verification import SmsVerification
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class FacebookRegistration(Mimic, RR):
    def __init__(self, driver, bot_sql, screen_size, ua, vpn_region, proxy):
        super().__init__()
        self.driver = driver
        self.sql = bot_sql
        self.__gender = ["Female", "Male"]
        self.__bot_gender = None
        self.__first_name = None
        self.__last_name = None
        self.__proxy = proxy
        self.__vpn_region = vpn_region
        self.__ua = ua
        self.__screen_size = screen_size
        self.__module = 'FacebookRegistration'

    def set_option(self, el, set_value):
        for option in el.find_elements_by_tag_name('option'):
            if option.get_attribute('value') == str(set_value):
                option.click()
                break

    def move_to_rand_point(self, el):
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(el, random.randint(3, 5), random.randint(3, 5))
        action.click()
        action.perform()

    def next_button_click(self, tag_name, button_text):
        submit_buttons = self.driver.find_elements_by_tag_name(tag_name)
        for button in submit_buttons:
            if button.text == button_text:
                button.click()
                return True
        return False

    def ok_button_click(self, tag_name, button_text):
        submit_buttons = self.driver.find_elements_by_tag_name(tag_name)
        for button in submit_buttons:
            if button.text == button_text:
                button.click()
                return True
        return False

    def get_first_name(self):
        with open(config.bot_first_names) as bots_file:
            names = bots_file.read().splitlines()
        return random.choice(names).split(',')

    def get_last_name(self):
        with open(config.bot_last_names) as bots_file:
            last_names = bots_file.read().splitlines()
        return random.choice(last_names)

    def get_num(self, apiKey):
        data = {'apikey': apiKey, 'service': 'facebook', 'country': config.country_code, 'form': '1'}
        r = requests.post('http://onlinesim.ru/api/getNum.php',
                          data=data)
        return r.json()

    def create_account(self, t_zid):
        #open google page before open config.facebook_page_mobile
        self.driver.get('https://www.google.com/')
        google_query = self.driver.find_element_by_name('q')
        self.mimicType(google_query, 'mobile facebook')
        time.sleep(self.mean_range)
        google_query.send_keys(Keys.RETURN)
        time.sleep(self.mean_range)
        self.driver.get(config.facebook_page_mobile)
        time.sleep(self.mean_range)
        if not self.next_button_click("span", "English (US)"):
            self.next_button_click("span", "English (UK)")
        time.sleep(self.mean_range)
        logger.info('Open facebook page complete')
        # 2. click on create account (id="signup-button")
        self.driver.find_element_by_id('signup-button').click()
        logger.info('Click on signup-button')
        # 3. First Name (id="firstname_input") and Last Name (id="lastname_input")
        while True:
            self.__bot_gender = random.choice(self.__gender)
            first_name = self.get_first_name()
            if self.__bot_gender == "Male":
                self.__first_name = first_name[2]
            else:
                self.__first_name = first_name[1]
            self.__last_name = self.get_last_name()
            if self.sql.check_bot_exist(self.__first_name, self.__last_name) is None:
                break
        time.sleep(self.mean_range)
        elem = self.driver.find_element_by_id('firstname_input')
        self.mimicType(elem, self.__first_name)
        time.sleep(self.shirt_range)
        elem = self.driver.find_element_by_id('lastname_input')
        self.mimicType(elem, self.__last_name)
        time.sleep(self.mean_range)
        # 4. Click Next(type="submit" value = "Next")
        self.next_button_click("button", "Next")
        logger.info('{0}: Firs/Last name input success'.format(self.__module))
        time.sleep(self.mean_range)
        # 5. Birth day(rundom shuffle day month and year) (id="day", id="month", id="year")
        day = self.driver.find_element_by_id('day')
        day.click()
        time.sleep(1)
        birth_day = random.randint(1, 28)
        self.set_option(day, birth_day)
        time.sleep(self.shirt_range)
        month = self.driver.find_element_by_id('month')
        month.click()
        time.sleep(1)
        get_month = lambda x: calendar.month_name[x][:4] if x == 9 else calendar.month_name[x][:3]
        birth_month = random.randint(1, 12)
        self.set_option(month, birth_month)
        time.sleep(self.shirt_range)
        year = self.driver.find_element_by_id('year')
        year.click()
        time.sleep(1)
        birth_year = random.randint(1975, 2000)
        self.set_option(year, birth_year)
        time.sleep(self.mean_range)
        # 6. Click Next (type="submit" value="Next") or Enter ?
        self.next_button_click("button", "Next")
        time.sleep(self.mean_range)
        # Check if confirm form exist
        self.next_button_click("a", "Yes")
        time.sleep(self.shirt_range)
        logger.info('{0}: Birth day success'.format(self.__module))
        # 7. Phone, got a new phone number from api and paste to form (id="contactpoint_step_input")
        sms_verification = SmsVerification(config.apikey, config.country_code)
        state = sms_verification.get_state(t_zid)
        try:
            phone_number = state[0]['number']
            phone_elem = self.driver.find_element_by_id('contactpoint_step_input')
            time.sleep(self.mean_range)
            self.mimicType(phone_elem, phone_number)
            time.sleep(self.mean_range)
            self.next_button_click("button", "Next")
        except Exception as e:
            logger.error('{0}: Get phone number error: {1}'.format(self.__module, t_zid))
            raise Exception(e)
        time.sleep(self.mean_range)
        logger.info('{0}: Phone number setup success'.format(self.__module))
        # 9. Gender (id="Female", id="Male") click
        bot_gender_elem = self.driver.find_element_by_id(self.__bot_gender)
        # move_to = ActionChains(self.driver).move_to_element(bot_gender_elem)
        # move_to.perform()
        bot_gender_elem.click()
        time.sleep(self.shirt_range)
        self.next_button_click("button", "Next")
        time.sleep(self.mean_range)
        logger.info('{0}: Gender setup success'.format(self.__module))
        # 10. Password (id="password_step_input")
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(random.randint(12, 17)))
        password_elem = self.driver.find_element_by_id('password_step_input')
        self.mimicType(password_elem, password)
        time.sleep(self.long_range)
        logger.info('{0}: Password setup success'.format(self.__module))
        # 11. Click Next (type="submit" value="Signup") or Enter ?
        self.next_button_click("button", "Sign Up")
        time.sleep(self.long_range)
        logger.info('{0}: Sign up click success'.format(self.__module))
        # 12. Save password (type="submit" value="OK")
        ok_button = False
        retries = 0
        while not ok_button:
            registration_failed = None
            try:
                registration_failed = self.driver.find_element_by_id('signup-button')
            except Exception as e:
                pass
            try:
                errors = self.driver.find_elements_by_tag_name('span')
                for failed in errors:
                    if failed.text == 'Registration Error':
                        print(phone_number)
                        print(password)
                        raise Exception('Registration Failed')
            except Exception as e:
                pass
            if registration_failed is not None:
                print(phone_number)
                print(password)
                raise Exception('Registration Failed')
            ok_button = self.ok_button_click("button", "OK")
            retries += 1
            if retries == 30:
                logger.error('{0}: Registration Failed'.format(self.__module))
                print(phone_number)
                print(password)
                raise Exception('Registration Failed')
            time.sleep(5)
        logger.info('{0}: Registration success'.format(self.__module))
        # 13. Wait for sms and put to (input name="c" type="number") sms_verification.get_state(t_zid['tzid'])['msg']
        try:
            time.sleep(self.long_range)
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.NAME, "c"))
            )
            logger.info('{0}: SMS verification form loaded'.format(self.__module))
        except Exception as e:
            logger.error('{0}: SMS verification form error: message {0}'.format(self.__module, e))
            raise Exception(e)
        sms_wait = 0
        while sms_wait <= 120:
            sms_code = sms_verification.get_state(t_zid)
            if 'msg' in sms_code[0]:
                sms_elem = self.driver.find_element_by_name('c')
                self.mimicType(sms_elem, sms_code[0]['msg'])
                break
            elif sms_wait == 120:
                logger.error('{0}: No SMS error'.format(self.__module))
                raise Exception('No SMS error')
            if sms_wait == 20:
                self.next_button_click("a", "I didn't get the code")
                time.sleep(2)
                self.next_button_click("a", "Send Code Again")
                time.sleep(self.mean_range)
                logger.info('{0}: Send code again success'.format(self.__module))
                sms_wait += 1
            else:
                sms_wait += 1
                time.sleep(5)
        sms_verification.set_operation_ok(t_zid)
        time.sleep(self.mean_range)
        # 14. Confirm <a href="#" class="_6if8 _56bs _26vk _56bx _56bu" use="primary">Confirm</a>
        self.next_button_click("a", "Confirm")
        logger.info('{0}: Confirm account success'.format(self.__module))
        # Check Next buttons after Confirm
        time.sleep(self.long_range)
        self.next_button_click("button", "Next")
        # Firsh on picture add
        # 15. Skip add friends (id="nux-nav-button").click wait for dialog frame and (id="qf_skip_dialog_skip_link").click
        try:
            time.sleep(self.long_range)
            nux_nav = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, "nux-nav-button"))
            )
            time.sleep(1)
            nux_nav.click()
            time.sleep(1)
            skip_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "qf_skip_dialog_skip_link"))
            )
            time.sleep(1)
            skip_elem.click()
        except Exception as e:
            logger.error('{0}: No skip friends form error: message {1}'.format(self.__module, e))
        time.sleep(self.long_range)
        try:
            time.sleep(1)
            nux_nav = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, "nux-nav-button"))
            )
            time.sleep(1)
            nux_nav.click()
        except Exception as e:
            logger.error('{0}: No nux-nav-button error: message {1}'.format(self.__module, e))
        time.sleep(self.mean_range)
        cookies = self.driver.get_cookies()
        city = LocationGenerator.get_city_and_school()
        hometown = city.split(',')[0]
        school = city.split(',')[random.randint(1, len(city.split(',')))]
        university = LocationGenerator.get_university()
        bot = (phone_number,                                    # 0 login
               password,                                        # 1 password
               config.vpn_provider,                             # 2 vpn_provider
               self.__vpn_region,                               # 3 vpn_region
               config.vpn_login,                                # 4 vpn_login
               config.vpn_password,                             # 5 vpn_password
               json.dumps(cookies),                             # 6 cookies
               True,                                            # 7 used_status
               'active',                                        # 8 block_status
               self.__first_name,                               # 9 bot_first_name
               self.__last_name,                                # 10 bot_last_name
               self.__bot_gender,                               # 11 bot_gender
               birth_day,                                       # 12 bot_birth_day
               birth_month,                                     # 13 bot_birth_month
               birth_year,                                      # 14 bot_birth_year
               self.__ua,                                       # 15 user_agent
               self.__screen_size,                              # 16 screen
               hometown,                                        # 17 city
               school,                                          # 18 school
               university,                                      # 19 university
               None,                                            # 20 job
               None,                                            # 21 profile_picture
               None,                                            # 22 bot_images_list
               datetime.now().strftime('%Y-%m-%d_%H:%M:%S'),    # 23 creation_date
               'infinity',                                      # 24 last_used_date
               0,                                               # 25 total_friends
               0,                                               # 26 scraped_profiles
               0,                                               # 27 total_actions
               0,                                               # 28 total_errors
               self.__proxy                                     # 29 proxy
               )
        self.sql.add_bot(bot)
        logger.info('{0}: Save bot information to database success'.format(self.__module))
        return bot
