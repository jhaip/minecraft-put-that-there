import tornado.ioloop
import tornado.web
import tornado.websocket
from botchallenge import *
import os
import sys

robot = None
robot_ready = False

if len(sys.argv) == 2:
    MINECRAFT_USERNAME = str(sys.argv[1])
    MINECRAFT_SERVER = "localhost"
    try:
        robot = Robot(MINECRAFT_USERNAME, MINECRAFT_SERVER)
    except:
        print("")
        print("WARNING: Could not connect to Minecraft server")
        print("Did you really want to connect as "+MINECRAFT_USERNAME+" to the server at "+MINECRAFT_SERVER+"?")
        print("And make sure the Modified Bukkit Server is running!")
    else:
        robot_ready = True
        print("SUCCESS: Connected to Minecraft Server at "+MINECRAFT_SERVER+" with username "+MINECRAFT_USERNAME)
else:
    print("No Minecraft username given - skipping connection to server")


class Hello(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message("Hello web page")
        print("Said hello to the web page")

    def on_message(self, message):
        print("Received message: '"+message+"'")
        if robot_ready:
            robot.message_all(message)
            if "down" in message:
                robot.move(Dir.DOWN)
            if "up" in message:
                robot.move(Dir.UP)
            if "left" in message:
                robot.move(Dir.LEFT)
            if "right" in message:
                robot.move(Dir.RIGHT)
            if "forward" in message:
                robot.move(Dir.FORWARD)
            if "backward" in message or "back" in message:
                robot.move(Dir.BACKWARD)
            if "come" in message:
                ownerLoc = robot.get_owner_location()
                robot.message_owner("I'm coming from " + str(int(robot.get_location().distance(ownerLoc))) + " units away.")
                while robot.get_location().distance(ownerLoc) > 4:
                    direction = robot.find_path(ownerLoc)
                    robot.turn(direction)
                    robot.move(direction)
                robot.message_owner("I'm here!")
            if "stop" in message:
                pass
                #TODO
            if "hello" in message:
                robot.message_all("Hello, I'm Jack!  Let's play Minecraft together!")
            if "what" in message:
                robot.message_all("I do the things you tell me to, such as build a house or find coal.")
                
    def on_close(self):
        print("CLOSING SERVER")


class Main(tornado.web.RequestHandler):
    def get(self):
        # This could be a template, too.
        self.render("webspeechdemo.html")

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'debug': True, 
            'static_path': os.path.join(os.path.dirname(__file__), 'static')
        }
        handlers = [
            (r"/", Main),
            (r"/websocket", Hello),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    print("Starting Tornado Server at localhost:8888")
    tornado.ioloop.IOLoop.instance().start()