# ratelimited

- create an account
- login
- send a lot of concurrent likes (race condition on rate limit check) + some stupid post to heavy the server and make the race win more likely to happen
- get the flag

The script I used for the exploit is `/race/script.py`.

Flag: flag{You_like_your_post_very_much!}
