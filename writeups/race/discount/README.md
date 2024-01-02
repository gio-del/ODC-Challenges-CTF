# discount

## Description

The site is an e-commerce site where a user get a discount code upon registration. The discount code is valid for 1 use and it is only valid for the user that created it (so we cannot spawn a lot of users and use their discount code).

The flag is one of the items in the shop, but it costs 10000$ and we only have 5$.

## Solution

Checking the source code we can note that there is a TOCTOU (Time Of Check Time Of Use) vulnerability in the discount code. The code is checked when the user clicks on the "Buy" button, but the discount code is only marked as used after the payment is processed.

This means that if we use the discount code in the same time as the server is checking it, we can use it multiple times, and we can now afford the flag (actually the whole shop).

The complete exploit is in [script.py](script.py).
