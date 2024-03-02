# goodluck

The idea is to try the same payload (basic shellcode from pwnlib) until the fliprandom function doesn't do anything to the important part of it.

For a lot of the time, I taught that the challenge was to guess the random by exploiting the srand, and then flipping the payload according to this random value, so that when the fliprandom function is called, it fixes the payload.

The problem was that the clock was monotonic, so I (suppose) can't guess the srand value.

But hey, the challenge is called goodluck, so I tried to just try the same payload until it works, and it did.

The script is in `/goodluck/script.py`.

Flag: flag{you_crafted_your_luck_very_good.}
