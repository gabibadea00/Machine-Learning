import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import uuid
import json
from ast import literal_eval
from covid_detector import covid_detector

class Controller(object):
    def __init__(self):
        print("SERVER is on!!")
        self.players = set()
        self.connections = set()
        self.json_array = []

class InitMessageHandler(tornado.web.RequestHandler):
    def get(self):
        print("Client has asked for initial details")   
        user_data = {}
        self.write((user_data))

class GameHandler(tornado.websocket.WebSocketHandler):

    json_array = []
    detector = covid_detector("config.json")

    def open(self):
        # called anytime a new connection with this server is opened
        print("Client connected") 
        print("Client sent: ", self)
        if self not in self.application.controller.connections:
            self.application.controller.connections.add(self)

    def on_message(self, message):
        # called anytime a new message is received
        res = literal_eval(message)
        if res['type'] == 'J':

            print("Received from client, msg = json_array")
            print("Now starting proccesing data from client!!")

            self.json_array = json.loads(res['message'])
            msg = json.dumps(self.detector.predict(self.json_array))
            self.write_message((msg))

            print("ENDING proccesing data from client!!")

        elif res['type'] == 'M':
            print("Received from client, msg = ", message)
            msg = "Server: " + message
            self.write_message((msg))

    def on_close(self):
        # called a websocket connection is closed
        if self in self.application.controller.connections:
            self.application.controller.connections.remove(self)

class Server(tornado.web.Application):
    def __init__(self):
        self.controller = Controller()
        handlers = [
            (r"/join", InitMessageHandler),
            (r"/game", GameHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    try:
        application = Server()
        server = tornado.httpserver.HTTPServer(application)
        server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
        print("Server closed") 