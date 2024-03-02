from z3 import *
import time
from pwn import *

strlen = 30

str_convert = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

s = Solver()

flag_idx = [BitVec("flag_idx%d" % i, 64) for i in range(strlen)]

# Constratints on the string
for i in flag_idx:
	s.add(i >= 0x0, i <= len(str_convert)-1) # Only Valid indexes

# Constraints from Ghidra
s.add(
    And(
        (flag_idx[18] * -10 + flag_idx[0] * 6 + flag_idx[8] + flag_idx[10] * 4 + flag_idx[14] * -0x1a == -0x37b),
        (((flag_idx[23] * -10 + (flag_idx[1] - flag_idx[2]) + flag_idx[6] * -0x46 + flag_idx[7] * -4 + flag_idx[12] * -0x46 + flag_idx[17] * -10) - flag_idx[26]) - flag_idx[28] == -0x1027),
        (flag_idx[28] + flag_idx[2] + flag_idx[6] * 0x46 + flag_idx[7] * 4 + flag_idx[12] * 0x46 + flag_idx[17] * 10 + flag_idx[23] * 10 + flag_idx[26] == 0x1057),
        flag_idx[29] * -0xc + (flag_idx[7] + flag_idx[3] * 3) * 4 + flag_idx[14] * 0x1b == 0x4e2,
        (flag_idx[24] + (flag_idx[14] - (flag_idx[13] + (flag_idx[4] * 6 - flag_idx[8]))) + flag_idx[18] * -10 + flag_idx[21] * -0x48 == -0xe67),
        flag_idx[26] + ((flag_idx[13] * -6 + (flag_idx[0] - flag_idx[1]) + flag_idx[5] * 5 + flag_idx[6] * 0x46 + flag_idx[7] * 4 + flag_idx[12] * 0x46) - flag_idx[14]) + flag_idx[17] * 10 + flag_idx[18] * 10 + flag_idx[21] * -0x48 + flag_idx[23] * 10 + flag_idx[24] == 0x58f,
        flag_idx[29] * -10 + ((flag_idx[21] * 0x48 + flag_idx[0] * -10 + flag_idx[6] * 0x46 + flag_idx[10] * 4 + flag_idx[12] * 0x46 + flag_idx[13] + flag_idx[14] * 2 + flag_idx[18] * -0x14) - flag_idx[24]) == 0x1282,
        flag_idx[7] == 5,
        flag_idx[8] == 0x15,
        flag_idx[18] * -10 + flag_idx[4] * -6 + flag_idx[9] + flag_idx[14] == -0x1c2,
        (flag_idx[18] * -10 + flag_idx[10] * 4 + flag_idx[14] == -0x15c),
        (flag_idx[29] + (((flag_idx[26] + (-flag_idx[3] - flag_idx[1]) + flag_idx[6] * 0x45 + flag_idx[11] * 7 + flag_idx[12] * 0x42 + flag_idx[14] * -3 + flag_idx[17] * 9 + flag_idx[21] * 0x48 + flag_idx[23] * 10) - flag_idx[27]) - flag_idx[28]) == 0x1c0d),
        flag_idx[25] + ((flag_idx[21] * 0x48 + ((flag_idx[14] + flag_idx[12] * 3 + 5 + flag_idx[13]) - flag_idx[15]) + flag_idx[18] * -10) - flag_idx[24]) == 0xb6b,
        (flag_idx[25] * 0x48 + ((flag_idx[23] * 0x48 + ((flag_idx[14] * 0xd8 + flag_idx[6] * 0x1f8 + 0x168 + flag_idx[12] * 0x1f8 + flag_idx[13] * 0x49) - flag_idx[19])) - flag_idx[24]) == 0x8b8b),
        flag_idx[14] == 0x22,
        (flag_idx[15] + -5) - flag_idx[25] == 0xc,
        (flag_idx[25] * -0x48 + flag_idx[0] * 6 + flag_idx[6] * -0x1f8 + flag_idx[10] * 4 + flag_idx[12] * -0x1f8 + flag_idx[13] * -0x48 + -0x2177 + flag_idx[15] * -8 + flag_idx[16] * 8 + flag_idx[18] * -10 + flag_idx[23] * -0x48 == -0x8fcb),
        flag_idx[23] * 0x5a + (flag_idx[12] + flag_idx[6]) * 0x276 + flag_idx[17] * 0x5a == 0x8dae,
        flag_idx[24] + (-0x22 - flag_idx[13]) + flag_idx[18] * 10 + flag_idx[21] * -0x48 == -0xb14,
        (flag_idx[24] + (flag_idx[19] - flag_idx[13]) == 0x3d),
        (flag_idx[29] * -3 + (flag_idx[3] * 3 - flag_idx[13]) + flag_idx[19] + flag_idx[20] * 9 + flag_idx[24] == 0x24d),
        flag_idx[24] * -3 + (flag_idx[9] + flag_idx[4] * -6) * 2 + flag_idx[13] * 3 + 0x66 + flag_idx[18] * -0x1e + flag_idx[21] * 0xd8 == 0x20a8,
        (flag_idx[22] + (flag_idx[4] * 6 - flag_idx[12]) == 0x83),
        (flag_idx[23] + (flag_idx[6] + flag_idx[12]) * 7 + -0x396 == -0x234),
        flag_idx[28] + (flag_idx[23] * 10 - (flag_idx[17] * -10 + (flag_idx[12] * -0x46 - ((flag_idx[2] - flag_idx[1]) + flag_idx[6] * 0x46 + 0x14)) + flag_idx[13])) + flag_idx[24] + flag_idx[26] == 0x1043,
        ((flag_idx[28] + ((flag_idx[25] + ((flag_idx[21] * -0x48 + flag_idx[1] + flag_idx[3] + flag_idx[4] * -6 + flag_idx[6] * -0x45 + flag_idx[12] * -0x44 + 0xbc + flag_idx[17] * -9) - flag_idx[22]) + flag_idx[23] * -10) - flag_idx[26]) + flag_idx[27]) - flag_idx[29] == -0x1b76),
        (flag_idx[28] + flag_idx[1] * -0x29 + flag_idx[3] + flag_idx[6] * 0xb37 + flag_idx[12] * 0xb37 + 0x66 + flag_idx[17] * 0x19b + flag_idx[21] * -0x48 + flag_idx[23] * 0x19a + flag_idx[26] * 0x29 + flag_idx[27]) - flag_idx[29] == 0x27b6a,
        flag_idx[27] + ((flag_idx[24] * -8 + flag_idx[1] + flag_idx[4] * 0x30 + flag_idx[6] * -0x45 + flag_idx[12] * -0x45 + flag_idx[13] * 8 + -0x152 + flag_idx[17] * -9 + flag_idx[18] * 0x50 + flag_idx[21] * 0x1f8 + flag_idx[23] * -10) - flag_idx[26]) == 0x579d,
        (flag_idx[28] + ((flag_idx[23] * -10 + flag_idx[1] + flag_idx[3] + flag_idx[6] * -0x45 + flag_idx[12] * -0x45 + 0x66 + flag_idx[17] * -9 + flag_idx[21] * -0x48) - flag_idx[26]) + flag_idx[27]) - flag_idx[29] == -0x1b66,
        (flag_idx[29] == 0x18)
    )
)

print(s.check())
m = s.model()

# print(m)

flag_idx_str = ''
for i in range(strlen):
	flag_idx_str += str_convert[int(m[flag_idx[i]].as_long())]

print('Flag', flag_idx_str)

