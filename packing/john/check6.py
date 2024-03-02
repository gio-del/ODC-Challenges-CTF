from z3 import *
from pwn import *

data = [ 0x0b, 0x4c, 0x0f, 0x00, 0x01, 0x16, 0x10, 0x07, 0x09, 0x38, 0x00, 0x00 ]

# undefined4 check6(char *str,int n)

# {
#   size_t len;
#   undefined4 uVar1;
#   char *flag;
#   int i;
  
#   len = strlen(flag);
#   if (i + 22U < len) {
#     if ((char)(flag[i + 20] ^ (&DAT_0804a081)[i]) == flag[i + 21]) {
#       uVar1 = check6((char *)0xdeadb00b,-0x21524ff5);
#     }
#     else {
#       uVar1 = 0;
#     }
#   }
#   else {
#     uVar1 = 1;
#   }
#   return uVar1;
# }

dead_book = []

def check(key, i):
    ret = BitVecVal(0, 64)
    length = BitVecVal(len(key), 64)

    if(i >= len(key) - 1): return BitVecVal(1, 64)
    return z3.If((key[i] ^ data[i]) == key[i+1], check(key, i+1), BitVecVal(0,64))
    if(i < length - 1):
        if((key[i] ^ data[i]) == key[i+1]):
            ret = check(key, i+1)
        else:
            ret = BitVecVal(0, 64)
    else:
        ret = BitVecVal(1, 64)
    return ret


strlen = 12

s = Solver()

key = [BitVec("key%d" % i, 8) for i in range(strlen)]

# Constratints on the string
for i in key:
	s.add(i >= 0x20, i <= 0x7E) # Only Printable Characters

s.add(key[0] == ord('&')) # From Check 5
s.add(key[1] == ord('-')) # From Check 5
s.add(check(key, 0) == 1)

while(s.check() == sat):
    m = s.model()

    flag = ''
    for i in range(strlen):
    	flag += chr(m[key[i]].as_long())

    s.add(Or([key[i] != m[key[i]] for i in range(10)]))
    print('Flag:', flag)

