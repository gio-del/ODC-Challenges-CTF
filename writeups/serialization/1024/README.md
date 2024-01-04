# 1024

## Description

The website is an implementation of the famous 2048 game. There is a page where the user can save the game state in a local file that contains the serialized game state. The user can also load a game state from a file.

The problem? Well, there is no public source code.

## Solution: part 1 (Getting the source code)

When one see a `?color=blue.css`, the first thing that comes to mind is LFI (Local File Inclusion) and Path Traversal. Basically, whatever is in the color parameter it's downloaded by the server and sent back to the client to be inserted in the style tag of the page. So, if we can make the server download a file that we control, we can get the source code.

## Solution: part 2 (Getting the flag)

Analyzing the source code, we can see that there is an `unserialize` function that per-se is already a vulnerability. But we have no way to exploit it to get code execution. However, we can see that there is a class called `Ranking` that on destruction it will write something that (that we can control) somewhere (that we can control). So we have arbitrary file write. We can only write to files in the directory `/games`, since that directory is made writable to store the ranking.

The idea is to write a PHP code to print the environment variables (where the flag is) to a `flag.php` file. Then, we can GET from the server the endpoint `/games/flag.php` and get the flag.

The complete exploit is in the file [script.py](script.py).

The serialized payload is generated with [script.php](script.php).
