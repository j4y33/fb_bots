from flask import Flask, Response


class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        return self.action()
        #return self.response


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)

    def run(self, host, port):
        self.app.run(host, port)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))