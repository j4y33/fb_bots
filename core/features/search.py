# Добавить поиск чего попало, просто, чтобы бот активничал
from actions.random_range import RR
from actions.scrolling import Scrolling
from core.coordination.navigator_mobile import Navigator


class Search(RR, Scrolling, Navigator):
    def __init__(self):
        super().__init__()
        self.__module = 'Search'

    def action(self, driver, bot):
        self.search(driver)
        #TODO