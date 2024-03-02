# I have a binary called 'john' that takes a flag from argv and checks it through various checks.
# I know that the flag starts with 'flag{packer' and I'm stuck at the 5 checks that checks the next 10 characters.
# One can understand what the 5th check is doing or just bruteforce it since it's only 10 characters but checked one by one (so no exponential complexity here).

# We will use gdb script to bruteforce the 5th check.

addr_check = 0x0804945e
addr_check_ret = 0x0804951e # The address of the ret instruction of the function `at `addr_check``

# The function at the address `addr_check` is called for each character of the flag, it puts 1 in eax if the character is correct and 0 otherwise.

# We will use gdb to bruteforce the 5th check.

import gdb
import string
import os

gdb.execute("file john")

gdb.execute("hb *{}".format(addr_check_ret))

flag = "flag{packer"
strlen = 33

def send_gdb_with_file(flag, c):
    _flag = flag + c + 'a'*(strlen-len(flag)-2) + '}'
    print('Try', _flag)

    with open("flag.txt", "w") as f:
        f.write(_flag)

    # Send the flag to the program as argv
    gdb.execute("r `cat flag.txt`")

def check(i):
    # If right hand side is 1, then the character is correct
    # Do not assume that the left hand side is $1, it can be $2, $3, etc.

    # Avoid the i characters that we already know
    for _ in range(i):
        gdb.execute("c")

    return gdb.execute("p $eax", to_string=True)[-2] == "1"

for i in range(11):
    for c in range(0x20,0x7f):
        if(i==6 and c & 1 == 0): continue # This is because the check5 early exit if (flag+17 & 1 == 0), we do not want that
        send_gdb_with_file(flag, chr(c))
        if check(i):
            flag += chr(c)
            print('Got new char', flag)
            break
        else:
            print("Wrong, retry")

print('Flag:', flag)
os.remove("flag.txt")