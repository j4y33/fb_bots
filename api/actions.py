import time
from flask import render_template, Response, request, jsonify


class ApiActions:
    def __init__(self, bot_core):
        self.__run_status = False
        self.__bot_core = bot_core
        self.__module = "ApiActions"

    def main_action(self):
        return render_template('index.html')

    def info(self):
        bot = self.__bot_core.get_bot_info
        data = {
            'login': bot[0],
            'password': bot[1],
            'vpn_provider': bot[2],
            'vpn_region': bot[3],
            'first_name': bot[9],
            'last_name': bot[10],
            'gender': bot[11],
            'city': bot[17],
            'school': bot[18],
            'university': bot[19],
            'creation_date': bot[23],
            'total_errors': bot[28]
        }
        return jsonify(result=data)

    def append_next(self):
        self.__bot_core.append_action(request.args.get("state"))
        return ('', 204)

    def get_main_actions(self):
        actions = []
        main_actions = self.__bot_core.get_main_actions
        for i in main_actions:
            actions.append(i)
        return jsonify(result=actions)

    def get_base_actions(self):
        actions = []
        base_actions = self.__bot_core.get_base_actions
        for i in base_actions:
            actions.append(i)
        return jsonify(result=actions)

    def get_low_actions(self):
        actions = []
        low_actions = self.__bot_core.get_low_actions
        for i in low_actions:
            actions.append(i)
        return jsonify(result=actions)

    def get_profile_actions(self):
        actions = []
        profile_actions = self.__bot_core.get_profile_actions
        for i in profile_actions:
            actions.append(i)
        return jsonify(result=actions)

    def stop_stream(self):
        if request.args.get("state") == "Stop":
            self.__run_status = False
            return ('', 204)
        else:
            return render_template('index.html')

    def screen_action(self):
        self.__run_status = True
        return Response(self.gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    # Generator for screenshots
    def gen(self):
        while self.__run_status:
            screen = self.__bot_core.get_screen
            time.sleep(2)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + screen + b'\r\n')

    def current_action(self):
        def generate():
            yield self.__bot_core.get_current_action
        return Response(generate(), mimetype='text/plain')

    def friends(self):
        friends = []
        friends_list = self.__bot_core.get_friends
        for i in friends_list:
            friends.append(i)
        return jsonify(result=friends)

    def groups(self):
        groups = []
        groups_list = self.__bot_core.get_groups
        for i in groups_list:
            groups.append(i)
        return jsonify(result=groups)

    def follow(self):
        follow = []
        following_list = self.__bot_core.get_follow
        for i in following_list:
            follow.append(i)
        return jsonify(result=follow)

    def last_actions(self):
        last_actions = []
        last_actions_list = self.__bot_core.last_actions
        for i in last_actions_list:
            last_actions.append(i)
        return jsonify(result=last_actions)

    def last_errors(self):
        last_errors = []
        last_errors_list = self.__bot_core.last_errors
        for i in last_errors_list:
            last_errors.append(i)
        return jsonify(result=last_errors)
