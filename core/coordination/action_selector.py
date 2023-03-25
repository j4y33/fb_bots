import base64
from PIL import Image
from io import BytesIO
from core.coordination.model import ActionModel


class ActionSelector:
    def __init__(self, sql, bot, driver, image_size, range_selector):
        self.__sql = sql
        self.__bot = bot
        self.__driver = driver
        self.__image_size = image_size
        self.random_range = range_selector
        self.__module = 'ActionSelector'

    def calculate_action(self, tracker):

        actions = self.__sql.get_actions(self.__bot[0], self.random_range.short_wait_range)
        if not actions:
            act = ActionModel.get_random_action('low')
            start = act[1](self.__driver, self.__bot, self.__sql, self.random_range)
            start.action()
            self.__sql.add_action(self.__bot[0], 'low', act[0], True,
                                  self.get_action_screen())
            tracker.track_action(act[0])
        else:
            total_low, total_middle, total_high = ([] for i in range(3))
            for action in actions:
                if action[4] == 'low':
                    total_low.append('low')
                elif action[4] == 'middle':
                    total_middle.append('middle')
                elif action[4] == 'high':
                    total_high.append('high')

            total_actions = len(total_low) + len(total_middle) + len(total_high)
            # MIDDLE actions
            if int((len(total_middle) / total_actions * 100)) < self.random_range.middle_percent:
                act = ActionModel.get_random_action('middle')
                start = act[1](self.__driver, self.__bot, self.__sql, self.random_range)
                start.action()
                self.__sql.add_action(self.__bot[0], 'middle', act[0], True,
                                      self.get_action_screen())
                tracker.track_action(act[0])
            # HIGH actions
            elif int((len(total_high) / total_actions * 100)) < self.random_range.high_percent:
                # Check DB for HIGH actions
                status = False
                acts = ActionModel.get_actions('high')
                for act in acts:
                    if not any(act in x for x in actions):
                        start = acts[act](self.__driver, self.__bot, self.__sql, self.random_range)
                        start.action()
                        self.__sql.add_action(self.__bot[0], 'high', act, True,
                                              self.get_action_screen())
                        tracker.track_action(act)
                        status = True
                        break
                    else:
                        continue
                if not status:
                    self.__sql.add_action(self.__bot[0], 'high', 'none', False,
                                          self.get_action_screen())
                    tracker.track_action('none')
            # LOW actions
            else:
                act = ActionModel.get_random_action('low')
                start = act[1](self.__driver, self.__bot, self.__sql, self.random_range)
                start.action()
                self.__sql.add_action(self.__bot[0], 'low', act[0], True,
                                      self.get_action_screen())
                tracker.track_action(act[0])

    def get_action_screen(self):
        screenshot = Image.open(BytesIO(self.__driver.get_screenshot_as_png()))
        screenshot.thumbnail(self.__image_size, Image.ANTIALIAS)
        img_byte = BytesIO()
        screenshot.save(img_byte, format='PNG')
        encoded_image = base64.b64encode(img_byte.getvalue())
        return encoded_image.decode('utf-8')