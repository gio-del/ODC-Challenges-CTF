# lolshop

## Solution

`unserialize()` is called and on the unserialized object the method `toDict()` is called. Then we can pass to the unserialize an object that has the method `toDict()` to get something executed. This class is `Product` that has the `toDict()` method. When called this method will call the inner `getPicture()` method that returns the content of the file specified in the `this->picture` attribute. We can set this attribute to do some path traversal and get the flag.

The complete exploit is in the file [script.py](script.py).

The serialized payload is generated with [script.php](script.php).
