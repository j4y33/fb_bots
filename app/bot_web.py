from api.api import FlaskAppWrapper
from api.actions import *


class BotWeb:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, bot_core):
        if self._running:
            a = FlaskAppWrapper('wrap')
            api_actions = ApiActions(bot_core)
            a.add_endpoint(endpoint='/', endpoint_name='main',
                           handler=api_actions.main_action)
            a.add_endpoint(endpoint='/info', endpoint_name='info',
                           handler=api_actions.info)
            a.add_endpoint(endpoint='/screen', endpoint_name='screen',
                           handler=api_actions.screen_action)
            a.add_endpoint(endpoint='/stop_stream', endpoint_name='stop_stream',
                           handler=api_actions.stop_stream)
            a.add_endpoint(endpoint='/append_next', endpoint_name='append_next',
                           handler=api_actions.append_next)
            a.add_endpoint(endpoint='/get_main_actions', endpoint_name='get_main_actions',
                           handler=api_actions.get_main_actions)
            a.add_endpoint(endpoint='/get_base_actions', endpoint_name='get_base_actions',
                           handler=api_actions.get_base_actions)
            a.add_endpoint(endpoint='/get_low_actions', endpoint_name='get_low_actions',
                           handler=api_actions.get_low_actions)
            a.add_endpoint(endpoint='/get_profile_actions', endpoint_name='get_profile_actions',
                           handler=api_actions.get_profile_actions)
            a.add_endpoint(endpoint='/current_action', endpoint_name='current_action',
                           handler=api_actions.current_action)
            # SQL
            a.add_endpoint(endpoint='/friends', endpoint_name='friends',
                           handler=api_actions.friends)
            a.add_endpoint(endpoint='/groups', endpoint_name='groups',
                           handler=api_actions.groups)
            a.add_endpoint(endpoint='/follow', endpoint_name='follow',
                           handler=api_actions.follow)
            a.add_endpoint(endpoint='/last_actions', endpoint_name='last_actions',
                           handler=api_actions.last_actions)
            a.add_endpoint(endpoint='/last_errors', endpoint_name='last_errors',
                           handler=api_actions.last_errors)
            a.run(host='0.0.0.0', port=5000)