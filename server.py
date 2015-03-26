import tornado.ioloop
import tornado.web
import tornado.websocket
from botchallenge import *

robot = Robot("jhaip","localhost")


class Hello(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message("Hello, world")
        print("WROTE MESSAGE")

    def on_message(self, message):
        print("RECEIVED MESSAGE")
        print(message)
        robot.message_all(message)
        if "down" in message:
            robot.move(Dir.DOWN)
        if "up" in message:
            robot.move(Dir.UP)

    def on_close(self):
        print("CLOSING SERVER")


class Main(tornado.web.RequestHandler):
    def get(self):
        # This could be a template, too.
        self.render("webspeechdemo.html")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", Main),
            (r"/websocket", Hello),
        ]
        tornado.web.Application.__init__(self, handlers)

if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()