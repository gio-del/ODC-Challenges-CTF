# free-as-in-beer

## Description

The website is a todo list. The user can add, edit and delete tasks. There is another page where the user can see the code of the website.

## Solution

The website takes a string from the cookie `todos` and if the first 32 characters are the md5 hash of the second part of the cookie, then the second part is unserialized.

Then, there is a class called `GPLSourceBloater` that basically prints out a license text and `this->source` (the source code of the website).

The idea is to craft a serialized object that will print the flag from the `flag.php` file by exploiting the `GPLSourceBloater` class and setting the `source` property to the `flag.php` file. Then, in python we create the cookie with the md5 hash of the serialized object and the serialized object and perform the request getting the flag.

The complete exploit is in the file [script.py](script.py).

The serialized payload is generated with [script.php](script.php).
