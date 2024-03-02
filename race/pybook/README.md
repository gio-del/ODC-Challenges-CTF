# pybook

## Description

The site is a python environment where you can run python code. The code is stored in a temporary file, checked for malicious code (like "hey, give me the flag") and then executed.

## Solution

Checking the source code we can note that there is a TOCTOU (Time Of Check Time Of Use) vulnerability in the check for malicious code. We can create a file with non-malicious code that we send to the server, and then replace it with malicious code after that the check has been performed on the legitimate code. Then the malicious code will be executed and we can get the flag.

The complete exploit is in [script.py](script.py).
