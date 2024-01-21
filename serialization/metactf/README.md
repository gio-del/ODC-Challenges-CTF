# metactf

## Description

The website lets us register, login, save the user (will create a file with the serialized user object) and upload a file with the serialized user object that will be unserialized.

## Solution

There is a class `Challenge` that on destruction will call the inner `stop()` method. The `stop()` method will execute the `exec()` with the `this->stop_cmd` as argument. We can serialize a `Challenge` object and upload it to the server. The `stop_cmd` is set to `cat /flag.txt` so we can get the flag by uploading the serialized object.

The serialized payload is generated with [script.php](script.php).
