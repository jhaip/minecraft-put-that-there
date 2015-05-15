# Minecraft Put-That-There
Play Minecraft with Jack the AI!

Remember to use python3 and pip3 to install things!

**First, install stuff:**

1. Get a 1.8.3 Craftbukkit/Spigot Server running
2. Follow the "How to build the server plugin" on our fork of the botchallenge Github (https://github.com/jhaip/botchallenge)
3. Run the Server and see that there are no errors.  Run minecraft and connect to your own server by doing Multiplayer and connecting to localhost:<INSERT PORT NAME>.  Press t and type /spawnrobot to create a Jack
4. Get the python botchallenge module by following the "Setting up" instructions here: http://katharosada.github.io/botchallenge/.
5. Connect to your localhost server to try it out by following these instructions.  There are other servers in the EU and AU but we will be using servers running on our computers.
6. Try setting up the minecraft-put-that-there code and install any requirements it complains about. (https://github.com/jhaip/minecraft-put-that-there)
7. See if it all works:
Run the Bukkit Server with botchallenge plugin
Connect to your server and create a Jack from Minecraft multiplayer
Run the server.py from our code (python3 server.py jhaip)
Open the webspeechdemo.html from our code in Chrome
See if it works!

**To run the code:**

1. run the spigot server by running start.command from the spigot-server directory
2. start Minecraft and join the server
3. run server.py with Python
in Minecraft, type /spawnrobot, then right-click to spawn Jack
4. go to https://jhaip.scripts.mit.edu/minecraft/ and click start to enable the microphone

**Common problems:**

If you don’t have the sound package (afplay), server.py will crash as soon as Jack tries to speak.  You can play without sound by commenting out the following two lines in server.py and command-scripts/pathFindingUtils.py:

```
audio_file = "sounds/voice-short-"+str(num)+".wav"
return_code = subprocess.call(["afplay", audio_file])
```
