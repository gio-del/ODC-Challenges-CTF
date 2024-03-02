# Puppy Walk

- flag is into "/flag.txt"
- img.php does unserialize on the `puppy` parameter
- then the method `getImg()` is called on the object, we can search for an object with this method to exploit something, or we can some magic methods like `__destruct()`. Searching out I found that there is no object with method `getImg()` apart from the puppy
- IDEA: Pass as Quote a Quote Generator to exploit the `toString()` method of the quote generator that will take a random quote,
  obviously we need to pass a serialized object of the QuoteGenerator class that has a different quoteFile path, so we can read the flag.
- encode base64
- visit img.php?puppy=base64 and voilà

With `php script.php` I generated the serialized object for the exploit.

Flag: flag{what_a_nice_puppy_you_got!You_can_bring_him_home_now}
