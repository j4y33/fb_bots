import random
import time
from selenium.webdriver.common.keys import Keys


class Mimic:
    def mimicType(self, obj, text, sendReturn=False):
        for char in text:
            obj.send_keys(char)
            time.sleep(random.randrange(1, 2))
        if sendReturn == True:
            obj.send_keys(Keys.RETURN)