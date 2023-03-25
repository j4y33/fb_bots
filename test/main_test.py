import time

from test.core_test import BotTest
from test.bot_run_test import BotRunTest


def main():
    bot_core = BotTest()  # Init with None
    bot = BotRunTest()
    bot.run(bot_core, 'share', 'high')
    print('after run')
    time.sleep(10000)


if __name__ == '__main__':
    main()
