
end_deoff = 0x55555555536f
addr_check_first16 = 0x555555555401 # The address of the ret instruction of the function `at `addr_check``
addr_check_second16 = 0x555555555406
# In the for cycle, for each character of the flag, it puts 1 in eax if the character is correct and 0 otherwise.

# We will use gdb to bruteforce this check.

import gdb
import string
import os

gdb.execute("file chall")

gdb.execute("hb *{}".format(addr_check_first16))

# flag = "flag{y0ur_n3xt_s0lv3_1s...y7m3v}"
flag = ''
strlen = 32

def send_gdb_with_file(flag, c):
    _flag = flag + c + 'a'*(strlen-len(flag)-1)
    print('Try', _flag)

    with open("flag.txt", "w") as f:
        f.write(_flag)

    # Send the flag to the program as argv
    gdb.execute("r < flag.txt")

def check(i):
    # If right hand side is 1, then the character is correct
    # Do not assume that the left hand side is $1, it can be $2, $3, etc.

    # Avoid the i characters that we already know
    for _ in range(i):
        gdb.execute("c")

    return gdb.execute("p $rax", to_string=True)[-2] == "1"

for i in range(16):
    for c in range(0x20,0x7f):
        send_gdb_with_file(flag, chr(c))
        if check(i):
            flag += chr(c)
            print('Got new char', flag)
            break
        else:
            print("Wrong, retry")
# gdb.execute("info break")
gdb.execute("del 2")
# gdb.execute("info break")
gdb.execute("hb *{}".format(addr_check_second16))
for i in range(16):
    for c in range(0x20,0x7f):
        send_gdb_with_file(flag, chr(c))
        if check(i):
            flag += chr(c)
            print('Got new char', flag)
            break
        else:
            print("Wrong, retry")

print('Flag:', flag)
# os.remove("flag.txt")
