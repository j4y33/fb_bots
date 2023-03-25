import time


class Scrolling:
    def __init__(self, random_range):
        self.random_range = random_range
        self.__module = 'Scrolling'

    def scroll_down(self, pause, driver):
        SCROLL_PAUSE_TIME = pause
        last_height = driver.execute_script("return document.body.scrollHeight")
        error_rate = 0
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                time.sleep(self.random_range.short_wait_range)
                error_rate = error_rate + 1
                if error_rate > 5:
                    break
            last_height = new_height

    def scroll_down_limited(self, pause, limit, driver):
        for i in range(limit):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)

    def scroll_up(self, pause, driver):
        SCROLL_PAUSE_TIME = pause
        last_height = driver.execute_script("return document.body.scrollWidth")
        error_rate = 0
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollWidth);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollWidth")
            if new_height == last_height:
                time.sleep(self.random_range.short_wait_range)
                error_rate = error_rate + 1
                if error_rate > 5:
                    break
            last_height = new_height

    def scroll_up_limited(self, pause, limit, driver):
        for i in range(limit):
            driver.execute_script("window.scrollBy(0,-250);")
            time.sleep(pause)
