import subprocess
import sys
import time
from threading import Thread
from app.bot_run import BotRun
from app.bot_web import BotWeb
from core.coordination.core import Bot


def main():
    bot_core = Bot()  # Bot core class, required for BotRun, init None
    # Start bot API
    api = BotWeb()
    # Run bot
    bot = BotRun()
    api_t = Thread(target=api.run, args=(bot_core,), daemon=True)
    bot_t = Thread(target=bot.run, args=(bot_core,))
    # Start bot thread
    bot_t.start()
    # Start api thread
    api_t.start()

    # Join to bot thread, api running in background
    bot_t.join()
    # After bot finish, kill VPN app
    if sys.platform == 'linux':
        kill_vpn = subprocess.Popen(["sudo", "killall", "openvpn"])
        kill_vpn.wait()


if __name__ == '__main__':
    main()
