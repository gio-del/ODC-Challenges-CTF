from z3 import *
from pwn import *

# mag = [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xdf, 0xb0, 0x08, 0x99, 0x00, 0x00, 0x00, 0x00 ]
# *(ulong *)(mag.3808 + (ulong)((uint)*smth & 1) * 8) -> if *smth & 1 then mag[8]
def mag(num):
    return z3.If(num == 0, z3.BitVecVal(0x0, 32), z3.BitVecVal(0x9908b0df, 32))

def m_seedRand(s, seed):
    s[0] = seed & 0xffffffff
    s[0x270] = 1
    while (s[0x270] < 0x270):
        s[s[0x270]] = (s[s[0x270] - 1] * 0x17b5)
        s[0x270] = s[0x270] + 1
    return s

def genRandLong(s):
  if ((0x26f < s[0x270]) or s[0x270] < 0):
     if ((0x270 < s[0x270]) or s[0x270] < 0):
       m_seedRand(s, 0x1105)

     for i in range(0xe3):
       uVar2 = s[i + 1]
       s[i] = (s[i + 0x18d] ^ LShR((uVar2 & 0x7fffffff | s[i] & 0x80000000), 1) ^ mag(uVar2 & 1))

     for i in range(0xe3, 0x26f):
       uVar2 = s[i + 1]
       s[i] = (s[i - 0xe3] ^ LShR((uVar2 & 0x7fffffff | s[i] & 0x80000000), 1) ^ mag(uVar2 & 1))

     uVar2 = s[0]
     s[0x26f] = (s[0x18c] ^ LShR((uVar2 & 0x7fffffff | s[0x26f] & 0x80000000), 1) ^ mag(uVar2 & 1))
     s[0x270] = 0
  uVar2 = s[0x270]
  s[0x270] = uVar2 + 1
  uVar1 = (s[uVar2] ^ LShR(s[uVar2], 0xb))
  uVar1 = (uVar1 ^ (uVar1 << 7) & 0x9d2c5680)
  uVar1 = (uVar1 ^ (uVar1 << 0xf) & 0xefc60000)
  return s, (uVar1 ^ z3.LShR(uVar1, 0x12))

s = [0]*0x271
seed = BitVec("seed", 32)

s = m_seedRand(s, seed)

for _ in range(1000):
    s, n = genRandLong(s)

s, n = genRandLong(s)

solver = Solver()

p = remote("bin.training.jinblack.it", 2020)

rand_num = str(p.recvuntil(b',')[2:-1],'utf-8')
print(rand_num)

rand_num = int(rand_num, 16)

solver.add(n == rand_num)

if solver.check() == sat:
    m = solver.model()
    seed = m[seed].as_long()
    print(seed)

    p.recvuntil(b"guess the seed:\n")
    p.sendline(b"%d" % seed)
    flag = p.recv()
    
    print(flag)