# aart

## Description

Checking the source code we can note that there is a time window in which the user is created but not deprived of privileges. If we get to login in that window we can get the flag.

Obviously if the race fails we can just try again with a new session and a new user.

The complete exploit is in [script.py](script.py).
