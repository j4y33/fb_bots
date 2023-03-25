from fake_useragent import UserAgent
from selenium import webdriver
from config.config import config


class BrowserProperties:
    def __init__(self, disable_web_gl=False, canvas=True, web_gl=False, disable_js=False, ua=None, proxy=None):
        self.__disable_web_gl = disable_web_gl
        self.__canvas = canvas
        self.__web_gl = web_gl
        self.proxy = proxy
        self.__disable_js = disable_js
        self.__ua = ua

    @property
    def get_driver_options(self) -> [webdriver.ChromeOptions(), str]:
        """
        Get browser options and UA

        :rtype: webdriver.ChromeOptions, ua
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--start-fullscreen')
        # Disable notifications for web version
        chrome_options.add_argument("--disable-notifications")
        #if self.proxy is not None:
        #    chrome_options.add_argument("--proxy-server={0}".format(self.proxy))
        if self.__disable_web_gl:
            chrome_options.add_argument("--disable-webgl")
            chrome_options.add_argument("--disable-3d-apis")
        elif not self.__disable_web_gl and self.__web_gl:
            chrome_options.add_extension(config.web_gl)
        if self.__canvas:
            chrome_options.add_extension(config.canvas)
        if self.__disable_js:
            chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        chrome_options.add_argument("user-agent={0}".format(self.user_agent()))
        return chrome_options, self.user_agent()

    def user_agent(self):
        if self.__ua is not None:
            return self.__ua
        else:
            ua = UserAgent(use_cache_server=False, verify_ssl=False)
            while True:
                user_agent = ua.chrome
                if config.default_platform in user_agent:
                    self.__ua = user_agent
                    return self.__ua
                else:
                    continue
