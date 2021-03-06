import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
from botchallenge import *
import os
import sys
import subprocess
import signal
import ssl
import random
from enum import Enum
from random import randint

class Questions(Enum):
    [Hello, How, WhatCan, WhatCant, WhatShould, What, Why, Where, MarcoPolo, ThankYou] = range(10)

class Actions(Enum):
    [Build, Get, Give, Stop, Come, Go, Teleport, Follow, FaceMe, ObeyGravity,
     Flatten, Craft, Place, CheckInventory, Do, Dance] = range(16)

actionToString = {Actions.Build: "build", Actions.Get: "gather",
                  Actions.Give: "give", Actions.Stop: "stop",
                  Actions.Go: "go", Actions.Teleport: "teleport",
                  Actions.Follow: "follow", Actions.Flatten: "flatten",
                  Actions.Craft: "craft", Actions.Place: "place",
                  Actions.Dance: "dance"}

class Objects(Enum):
    [House, Tunnel, Tree, Coal, Dirt, Sand, Water, Stone, Iron, Diamond,
     Grass, Seeds, Jack, That, There, Current_Action, Your_Name, Thing] = range(18)

objToBlockTypes = {Objects.Tree: [BlockType.LOG, BlockType.LOG_2],
                   Objects.Coal: [BlockType.COAL_BLOCK, BlockType.COAL_ORE, BlockType.COAL],
                   Objects.Dirt: [BlockType.DIRT, BlockType.GRASS],
                   Objects.Sand: [BlockType.SAND, BlockType.GRAVEL],
                   Objects.Water: [BlockType.WATER, BlockType.STATIONARY_WATER],
                   Objects.Stone: [BlockType.STONE, BlockType.COBBLESTONE],
                   Objects.Iron: [BlockType.IRON_ORE],
                   Objects.Diamond: [BlockType.DIAMOND_ORE, BlockType.DIAMOND_BLOCK],
                   Objects.House: [BlockType.COBBLESTONE],
                   Objects.Grass: [BlockType.LONG_GRASS],
                   Objects.Seeds: [BlockType.SEEDS]}

question = False
action = False
obj = False

robot = None
robot_ready = False

proc = False
should_follow = True

waiting_to_reset = False

class States:
    IDLE = "doing nothing"
    FOLLOWING = "following you"
    BUILD_HOUSE = "building a house"
    BUILD_TUNNEL = "mining a tunnel"
    GATHER = "gathering"
    GIVE = "giving you something"
    GO_THERE = "going over there"
    COME_TO_PLAYER = "going to where you are"
    OBEY_GRAVITY = "obeying gravity"
    CHECK_INVENTORY = "checking my inventory"
    MAKE_FLAT = "making this area flat"
    PLACE = "placing a block"
    DO_SOMETHING = "doing something"
    DANCE = "dancing"

robot_state = States.IDLE

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
        proc = False
else:
    print("No Minecraft username given - skipping connection to server")


def message_has_substring(message, substring_list):
    return any(substr in message for substr in substring_list)

def run_new_command(command_line_array):
    global proc
    if proc is not False:
        print("found a command already running in the background")
        proc.terminate()
        proc.wait()
        print("It's killed now")
    command_line_array[0] = "command-scripts/"+command_line_array[0]
    command_line_array = ['python3']+command_line_array
    proc = subprocess.Popen(command_line_array)

def message_all(robot, text):
    Utilities.speak()
    robot.message_all(text)


class Hello(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        # allow any websockets connections to connect
        return True

    def open(self):
        self.write_message("Hello web page")
        print("Said hello to the web page")

    def on_message(self, message):
        global proc
        global robot_state
        global should_follow
        global waiting_to_reset
        final_transcript = False
        recognized_command = False
        print("Received message: '"+message+"'")
        if message == "C0nfirm3d":
            print("Web page is successfully communicating with the python server! :)")
            return
        if message == "R3SETTING":
            print("Speech Recongition confirmed it's starting to reset.")
            return
        if message == "FRESH START":
            print("Speech Recognition is live again.")
            waiting_to_reset = False
            return
        if robot_ready and waiting_to_reset == False:
            if message[0] == ";":
                final_transcript = True
            # message = message[1:] # get rid of the first character flag for the message type
            message = message.replace(";","!!! ").lower()
            # robot.message_all(message)
            if "up" in message:
                robot.move(Dir.UP)
            if "left" in message:
                robot.move(Dir.LEFT)
            if "right" in message:
                robot.move(Dir.RIGHT)
            if "forward" in message:
                robot.move(Dir.FORWARD)
            if "backward" in message:
                robot.move(Dir.BACKWARD)
                
            # Detecting Question
            question = False
            if (message_has_substring(message, ["hello","howdy","high","hi jack"])
                  or (message_has_substring(message, ["hi"]) and len(message) == 2)):
                question = Questions.Hello
            elif message_has_substring(message, ["how"]):
                question = Questions.How
            elif message_has_substring(message, ["what can't","not able","can't you"]):
                question = Questions.WhatCant
            elif message_has_substring(message, ["what can you", "what can jack"]):
                question = Questions.WhatCan
            elif message_has_substring(message, ["what should"]):
                question = Questions.WhatShould
            elif message_has_substring(message, ["what","who"]):
                question = Questions.What
            elif message_has_substring(message, ["why"]):
                question = Questions.Why
            elif message_has_substring(message, ["where"]):
                question = Questions.Where
            elif message_has_substring(message, ["marco"]):
                question = Questions.MarcoPolo
            elif message_has_substring(message, ["thank"]):
                question = Questions.ThankYou
            else:
                question = False
            
            # Detecting Action
            action = False
            if message_has_substring(message, ["stop","quit","stay","don't","do not"]):
                action = Actions.Stop
            elif message_has_substring(message, ["build","make"]):
                action = Actions.Build
            elif message_has_substring(message, ["find","search","look for","get","gather","collect","cut","mine","pick","obtain","destroy","dig","chop","bring"]):
                action = Actions.Get
            elif message_has_substring(message, ["follow"]):
                action = Actions.Follow
            elif message_has_substring(message, ["flat","clear","flatten"]):
                action = Actions.Flatten
            elif message_has_substring(message, ["give","drop","throw"]):
                action = Actions.Give
            elif message_has_substring(message, ["face","look at me","look this way","look toward me"]):
                action = Actions.FaceMe
            elif message_has_substring(message, ["down","gravity"]):
                action = Actions.ObeyGravity
            elif message_has_substring(message, ["craft"]):
                action = Actions.Craft
            elif message_has_substring(message, ["teleport"]):
                action = Actions.Teleport
            elif message_has_substring(message, ["come"]):
                action = Actions.Come
            elif message_has_substring(message, ["dance"]):
                action = Actions.Dance
            elif message_has_substring(message, ["go"]): #keep this near end
                action = Actions.Go
            elif message_has_substring(message, ["place","put"]):
                action = Actions.Place
            elif message_has_substring(message, ["do you have","inventory","how much","how many"]):
                action = Actions.CheckInventory
            elif message_has_substring(message, ["do"]): #keep at end to avoid substring matching
                action = Actions.Do
            else:
                action = False

            # Detecting object
            obj = False
            if message_has_substring(message, ["house","hut","shelter","place to sleep","fort","home","building","structure"]):
                obj = Objects.House
            elif message_has_substring(message, ["tunnel","cave"]):
                obj = Objects.Tunnel
            elif message_has_substring(message, ["tree","wood","log"]):
                obj = Objects.Tree
            elif message_has_substring(message, ["coal","goal","cool","cold","cole","coke","call"]):
                obj = Objects.Coal
            elif message_has_substring(message, ["dirt","ground","earth"]):
                obj = Objects.Dirt
            elif message_has_substring(message, ["sand"]):
                obj = Objects.Sand
            elif message_has_substring(message, ["water"]):
                obj = Objects.Water
            elif message_has_substring(message, ["stone","rock","mountain","gray","grey"]):
                obj = Objects.Stone
            elif message_has_substring(message, ["iron"]):
                obj = Objects.Iron
            elif message_has_substring(message, ["diamond"]):
                obj = Objects.Diamond
            elif message_has_substring(message, ["grass","weed"]):
                obj = Objects.Grass
            elif message_has_substring(message, ["seed"]):
                obj = Objects.Seeds
            elif message_has_substring(message, ["this","that","those","these"]):
                obj = Objects.That
            elif message_has_substring(message, ["there","they're","their"]):
                obj = Objects.There
            elif message_has_substring(message, ["your name"]):
                obj = Objects.Your_Name
            elif message_has_substring(message, ["you doing","jack doing"]):
                obj = Objects.Current_Action
            elif message_has_substring(message, ["thing","something","it"]):
                obj = Objects.Thing
            elif message_has_substring(message, ["you","jack"]): #keep this last
                obj = Objects.Jack
            else:
                obj = False

            # Before doing an action, check whether command is a question
            if question is Questions.Hello:
                message_all(robot, "Hello, I'm Jack!  Let's play Minecraft together!")
                recognized_command = True
            elif question is Questions.How:
                if action is Actions.CheckInventory:
                    question = False
                elif action is not False and action is not Actions.Do:
                    action_phrase = actionToString.get(action, "do that")
                    message_all(robot, "I can't explain how to " + action_phrase
                                + ", but I might be able to do it for you.")
                    recognized_command = True
            elif question is Questions.What:
                if action is Actions.CheckInventory:
                    Utilities.get_inventory(robot)
                    recognized_command = True
                elif obj is Objects.That:
                    owner_target_block = robot.get_owner_target_block()
                    owner_target_block_type = robot.get_block_type_at(owner_target_block)
                    if owner_target_block_type is not None:
                        owner_target_block_type_str = str(owner_target_block_type).replace("_","").lower().replace("stationary","")
                        if owner_target_block_type_str[-1] in "0123456789":
                            owner_target_block_type_str = owner_target_block_type_str[:-1]
                        if owner_target_block_type_str == "pumpkin":
                            if owner_target_block == robot.get_location():
                                owner_target_block_type_str = "me"
                            else:
                                owner_target_block_type_str = "my cousin"
                        message_all(robot, "That is "+owner_target_block_type_str)
                    recognized_command = True
                elif obj is Objects.Current_Action:
                    message_all(robot, "I am "+robot_state)
                    recognized_command = True
                elif obj is Objects.Your_Name:
                    message_all(robot, "My name is Jack.")
                    recognized_command = True
            elif question is Questions.WhatCan:
                # if obj is Objects.Jack:
                message_all(robot, "I can move around and place and mine blocks.")
                message_all(robot, "I can tell what you are looking at.")
                message_all(robot, "I know how to find and build common Minecraft things.")
                message_all(robot, "I try to understand what you say so we can get along and have fun together! :)")
                recognized_command = True
            elif question is Questions.WhatCant:
                # if obj is Objects.Jack:
                message_all(robot, "I don't mess with living things... I'm a pumpkin.")
                message_all(robot, "I can't craft things and I always carry a diamond pickaxe.")
                message_all(robot, "And I'm still learning English so speak clearly and simply please. :)")
                recognized_command = True
            elif question is Questions.WhatShould:
                random_value = randint(0,4)
                if random_value == 0:
                    message_all(robot, "How about finding some coal?")
                elif random_value == 1:
                    message_all(robot, "Build a house.")
                elif random_value == 2:
                    message_all(robot, "Let's find some diamond.")
                elif random_value == 3:
                    message_all(robot, "We need more iron. You can never have enough iron.")
                elif random_value == 4:
                    message_all(robot, "Let's destroy a mountain.")
                recognized_command = True
            elif question is Questions.Why:
                message_all(robot, "I don't know why.")
                recognized_command = True
            elif question is Questions.Where:
                if obj is Objects.Jack:
                    dist = round(robot.get_location().distance(robot.get_owner_location()), 2)
                    direction = str(robot.get_owner_location().direction(robot.get_location()))
                    message_all(robot, "I am " + str(dist) + " units away from you "+direction+".")
                    recognized_command = True
                elif final_transcript is True:
                    message_all(robot, "I don't know how to tell you where that is.")
                    recognized_command = True
            elif question is Questions.MarcoPolo:
                dist = round(robot.get_location().distance(robot.get_owner_location()), 2)
                direction = str(robot.get_owner_location().direction(robot.get_location()))
                message_all(robot, "Polo! I am " + str(dist) + " units away from you "+direction+".")
                recognized_command = True
            elif question is Questions.ThankYou:
                message_all(robot, "You're welcome!")
                recognized_command = True
                    

            # Making Jack do thing based on an action, obj combo
            if question is False:
                if action is Actions.Build:
                    if obj is Objects.House:
                        robot_state = States.BUILD_HOUSE
                        run_new_command(['buildhut.py', MINECRAFT_USERNAME])
                        recognized_command = True
                    elif obj is Objects.Tunnel: #hack to recognize "dig a tunnel"
                        robot_state = States.BUILD_TUNNEL
                        # Mine a tunnel to layer 15 and not stopping for any particular block type
                        run_new_command(['minetunnel.py', MINECRAFT_USERNAME, "15", "[]"])
                        recognized_command = True
                    elif final_transcript is True:
                        message_all(robot, "I don't know how to build that, but I can help "
                                + "you gather materials if you tell me what to find.")
                        recognized_command = True
                elif action is Actions.Craft:
                    message_all(robot, "I don't know how to craft things, but I can help "
                            + "you gather materials if you tell me what to find.")
                    recognized_command = True
                elif action is Actions.Get:
                    if obj is Objects.Tunnel: #hack to recognize "dig a tunnel"
                        robot_state = States.BUILD_TUNNEL
                        # Mine a tunnel to layer 15 and not stopping for any particular block type
                        run_new_command(['minetunnel.py', MINECRAFT_USERNAME, "15", "[]"])
                        recognized_command = True
                    elif obj in objToBlockTypes:
                        robot_state = States.GATHER
                        run_new_command(['gatherblock.py', 
                                        MINECRAFT_USERNAME, 
                                        str(objToBlockTypes[obj]).replace(' ','')])
                        recognized_command = True
                    elif obj is Objects.That:
                        blockType = Utilities.get_that_block_type(robot)
                        if blockType is not None:
                            robot_state = States.GATHER
                            run_new_command(['gatherthat.py', #todo
                                            MINECRAFT_USERNAME, 
                                            str([blockType])])
                            recognized_command = True
                    elif final_transcript is True:
                        message_all(robot, "I don't know how to get that.")
                        recognized_command = True
                elif action is Actions.Stop:
                    if proc is not False:
                        should_follow = False
                        proc.terminate() # if not forceful enough use .kill()
                        proc.wait()
                        proc = False
                        robot_state = States.IDLE
                    recognized_command = True
                elif action is Actions.Give:
                    if obj in objToBlockTypes:
                        robot_state = States.GIVE
                        run_new_command(['giveblock.py',
                                        MINECRAFT_USERNAME, 
                                        str(objToBlockTypes[obj]).replace(' ','')])
                        recognized_command = True
                    elif obj is Objects.That:
                        blockType = Utilities.get_that_block_type(robot)
                        if blockType is not None:
                            robot_state = States.GIVE
                            run_new_command(['giveblock.py', 
                                            MINECRAFT_USERNAME,
                                            str([blockType])])
                            recognized_command = True
                    elif final_transcript is True:
                        message_all(robot, "I can give you items from my inventory if you tell me what to give you.")
                        recognized_command = True
                elif action is Actions.Place:
                    if obj in objToBlockTypes and obj is not Objects.House:
                        robot_state = States.PLACE
                        run_new_command(['placeblock.py',
                                        MINECRAFT_USERNAME, 
                                        str(objToBlockTypes[obj]).replace(' ','')])
                        recognized_command = True
                elif action is Actions.Go or action is Actions.Teleport:
                    if obj is Objects.There or obj is Objects.That:
                        should_follow = False
                        robot_state = States.GO_THERE
                        if action is Actions.Teleport:
                            run_new_command(['gothere.py', MINECRAFT_USERNAME, '0'])
                        else:
                            run_new_command(['gothere.py', MINECRAFT_USERNAME])
                        recognized_command = True
                    elif final_transcript is True:
                        message_all(robot, "You can point to a location and tell me to go there.")
                        recognized_command = True
                elif action is Actions.Come:
                    robot_state = States.COME_TO_PLAYER
                    run_new_command(['comehere.py', MINECRAFT_USERNAME])
                    recognized_command = True
                elif action is Actions.FaceMe:
                    direction = robot.find_path(robot.get_owner_location())
                    robot.turn(direction)
                    recognized_command = True
                elif action is Actions.ObeyGravity:
                    should_follow = False
                    robot_state = States.OBEY_GRAVITY
                    run_new_command(['obeygravity.py', MINECRAFT_USERNAME])
                    recognized_command = True
                elif action is Actions.Follow:
                    should_follow = True
                    robot_state = States.FOLLOWING
                    run_new_command(['follow.py', MINECRAFT_USERNAME])
                    recognized_command = True
                elif action is Actions.Flatten:
                    robot_state = States.MAKE_FLAT
                    run_new_command(['flatten.py', MINECRAFT_USERNAME])
                    recognized_command = True
                elif action is Actions.CheckInventory:
                    if obj in objToBlockTypes:
                        robot_state = States.CHECK_INVENTORY
                        run_new_command(['checkinventory.py', 
                                        MINECRAFT_USERNAME, 
                                        str(objToBlockTypes[obj]).replace(' ','')])
                        recognized_command = True
                    elif obj is Objects.That:
                        blockType = Utilities.get_that_block_type(robot)
                        if blockType is not None:
                            robot_state = States.CHECK_INVENTORY
                            run_new_command(['checkinventory.py', 
                                            MINECRAFT_USERNAME, 
                                            str([blockType])])
                            recognized_command = True
                    elif final_transcript is True:
                        Utilities.get_inventory(robot)
                        recognized_command = True
                elif action is Actions.Do:
                    if obj is Objects.Thing:
                        robot_state = States.DO_SOMETHING
                        run_new_command(['dosomething.py', MINECRAFT_USERNAME])
                        recognized_command = True
                elif action is Actions.Dance:
                    robot_state = States.DANCE
                    run_new_command(['dance.py', MINECRAFT_USERNAME])
                    recognized_command = True

        if recognized_command:
            if final_transcript is False:
                # send command back to web page to end the transcript
                self.write_message(u"end transcript")
                print("------ sending message to end transcript")
                waiting_to_reset = True

    def on_close(self):
        print("CLOSING SERVER")

class Utilities:
    def get_inventory(robot):
        inventoryItems = [str(key).lower() for (key, val) in robot.get_inventory()]
        message_all(robot, "In my inventory, I have: "
                + str(inventoryItems).strip('[').strip(']').replace("'", ""))
    def get_that_block_type(robot):
        owner_target_block = robot.get_owner_target_block()
        return robot.get_block_type_at(owner_target_block)
    def speak():
        num = random.randint(1,3)
        audio_file = "sounds/voice-short-"+str(num)+".wav"
        return_code = subprocess.call(["afplay", audio_file])
                    
class Main(tornado.web.RequestHandler):
    def get(self):
        # This could be a template, too.
        self.render("index.html")

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

def is_background_process_dead():
    # called once every second
    global proc
    global robot_state
    global should_follow
    # print("checking to see if background process is dead")
    if proc is not False:
        proc_returncode = proc.poll() # Check if child process has terminated. Set and return returncode attribute.
        if proc_returncode is not None:
            print("background process ended!")
            proc = False
            if (robot_state is not States.GO_THERE
                and robot_state is not States.OBEY_GRAVITY
                and robot_state is not States.CHECK_INVENTORY):
                should_follow = True
            robot_state = States.IDLE
    if robot_state is States.IDLE and should_follow:
        run_new_command(['follow.py', MINECRAFT_USERNAME])
        robot_state = States.FOLLOWING

if __name__ == "__main__":
    app = Application()
    data_dir = os.path.dirname(__file__)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    print("Starting Tornado Server at localhost:8888")
    pc = tornado.ioloop.PeriodicCallback(is_background_process_dead, 1000)
    pc.start()
    tornado.ioloop.IOLoop.instance().start()
