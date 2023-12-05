from z3 import *
import time

s = Solver()

input = [BitVec("flag%d" % i, 8) for i in range(23)]

# Constratints on the string
for i in input:
	s.add(i >= 0x20, i <= 0x7f) # Only Printable Characters

s.add(input[0] == ord('f'))
s.add(input[1] == ord('l'))
s.add(input[2] == ord('a'))
s.add(input[3] == ord('g'))
s.add(input[4] == ord('{'))
s.add(input[22] == ord('}'))

# Constraints from Ghidra

s.add(      input[0xb] * -0x19 +
      input[8] * 0x31 + input[10] * 0xbb + -0x9c2a + input[1] * 0x39 + input[2] * 3 +
      input[0x16] * 0xd7 + input[9] * -0xbd + input[0xc] * -0x47 + input[0xd] * 0xb7 +
      input[0xf] * -0x9b + input[3] * 0x73 + input[0x13] * -0x95 + input[0xe] * 0xc6 +
      input[4] * 0x9a + input[0x11] * -0x66 + input[0x10] * 0x7c + input[0x12] * 0xb9 +
      input[6] * -0xaa + input[5] * -0x6a + input[0x15] * 0xe1 + input[0x14] * -0xa6 +
      input[7] * -0xb5 + input[0] * -0xb7 == 0)

s.add(        input[0x15] * -0x55 +
        input[0xe] * -0xe5 +
        input[8] * -0xae + input[6] * -0x58 + input[0x14] * 0x7d + input[1] * -0x3c +
        input[0xf] * 0xe0 + input[10] * 0xfc + input[2] * -0x5e + input[0x12] * -0xe0 +
        input[5] * 0xee + input[0x10] * 0xe7 + input[7] * -0x61 + input[0xb] * -0x89 +
        input[4] * -0x80 + input[0] * -0xfd + input[0xc] * -0x9e + 0x9a2e +
        input[0x16] * 2 + input[0x16] * -0x10 + input[0x13] * -0x11 + input[0x11] * 0x30 +
        input[0xd] * 0x83 + input[9] * -0xde + input[3] * 0xe2 == 0)

s.add(          input[0x10] * -0x39 +
          input[0x16] * 0xc6 +
          input[0x15] * -0x6c + input[9] * 0xd4 + input[0xf] * -0xe2 + input[0xd] * 0xc5 +
          input[0x14] * 0x91 + input[2] * 0x84 + input[1] * 0x32 + input[0xe] * 0x86 + -0x3124d +
          input[5] * 0xd2 + input[0x11] * 0xea + input[0xb] * 0x1b + input[0x12] * 0x97 +
          input[3] * 0xf0 + input[4] * -0x8a + input[0xc] * 0x95 + input[0x13] * 0x9f +
          input[7] * -0x29 + input[8] * 0xb3 + input[0] * -0x31 + input[10] * 0xd1 + input[6] * 0x32
          == 0)

s.add(            input[7] * 0x5f +
            input[10] * 0x60 +
            input[0x14] * 0x8d + input[0xc] * 0xab + input[6] * -0x1a + input[0xe] * 0xcb +
            input[2] * 0x57 + input[0x13] * -0x8d + input[0x16] * -0xba + input[0xf] * 0xa9 +
            input[0x10] * -0x14 + input[5] * 0x52 + input[0x11] * -0x23 + input[1] * -0x68 +
            input[0x15] * 199 + input[0x12] * 0x57 + input[0xd] * 0xeb + input[8] * -0xa8 +
            input[9] * 0x85 + input[0] * -0x62 + -0x20c1e + input[4] * 0xaf + input[3] * -0x26 +
            input[0xb] * 0xfb == 0)

s.add(              input[0xb] * 0x23 +
              input[3] * -0x80 + input[0x12] * 0xd0 + input[0xd] * 0x8a + -0x1b8ed + input[0] * -0x51
              + input[2] * 0x8c + input[1] * 4 + input[0x13] * 0x86 + input[4] * 0xf0 +
              input[5] * -0xc4 + input[9] * -0x55 + input[0x14] * 0xd8 + input[0x11] * -0xb5 +
              input[0xe] * -0x14 + input[7] * 0xea + input[10] * -0xc3 + input[8] * 0xeb +
              input[0xf] * 0xba + input[0x10] * -0xf5 + input[0x15] * 0xe7 + input[0xc] * 0x97 +
              input[0x16] * 0x97 + input[6] * -0x4e == 0)

s.add(                input[0xc] * 0xd6 +
                input[0x11] * -0x80 +
                input[3] * 0x21 + input[0xf] * -0xe8 + input[10] * 0xd + input[4] * -0x7b +
                input[0x12] * 0x5a + input[0x13] * 0xda + input[6] * -0x66 + input[1] * -0x98 +
                input[8] * 0x23 + input[0x14] * 0x16 + input[0x15] * -0x89 + input[9] * -0xba +
                input[7] * 0x53 + input[0xb] * 0x6e + input[2] * 0x8e + input[5] * -0xe5 +
                input[0xd] * 0xc5 + input[0x10] * -7 + input[0x16] * -0xee + input[0] * 0xed +
                input[0xe] * 0xab + -0x3da5 == 0)

s.add(                  input[1] * 0xa8 +
                  input[7] * -0xa6 +
                  ((input[6] * 0x7a + input[2] * -0x50 + input[0x12] * 0xdd + input[4] * -0xa7 +
                    input[5] * 0x8b + input[0xc] * -0x26 + input[8] * -0x8c + input[0x10] * -0x9f +
                   input[10] * -0xc6) - input[0x16]) + input[0xe] * -0x35 + input[9] * 0xe +
                  input[0x14] * -0x6f + input[0xb] * 0x91 + 0xb2a6 + input[0x11] * -0x8d +
                  input[0xd] * -0xd + input[3] * 0x39 + input[0] * -0xcc + input[0xf] * -0x45 +
                  input[0x13] * 0xe9 + input[0x15] * -0x6a == 0)

s.add(                    input[0xe] * 0xe +
                    input[0x15] * 0xeb +
                    input[10] * 0x12 + input[0x13] * 0xa3 + input[3] * 0xa5 + input[4] * 0xb3 +
                    input[0xf] * -0x10 + input[0xc] * -0x4d + input[2] * -0x65 + input[0x10] * 0xc1
                    + input[0x16] * 0x43 + -0x20fdc + input[0x11] * 0xeb + input[0x14] * 0xb4 +
                    input[5] * 0x33 + input[0xd] * -0xe7 + input[9] * 0x7a + input[0] * -0x42 +
                    input[1] * 0xca + input[7] * 0xca + input[8] * 0x35 + input[0xb] * 0x4e +
                    input[0x12] * 0x4d + input[6] * -0xbe == 0)

s.add(                      input[0x11] * -199 +
                      input[10] * -0x4e +
                      input[5] * -0xd8 + input[0xd] * -0x17 + input[7] * 0xc5 + input[0xe] * 0x43 +
                      input[0x10] * 0xc4 + input[0xf] * 0xaa + 0x4867 + input[1] * -0xf5 +
                      input[3] * -0xa1 + input[9] * 0x55 + input[0x15] * 0x67 + input[0xc] * -0x4e +
                      input[0x13] * 8 + input[0] * -0xd3 + input[0x16] * -0xb2 + input[8] * 0x2d +
                      input[0xb] * -0xf + input[4] * 0xd1 + input[6] * 0xf2 + input[2] * 0xf0 +
                      input[0x14] * -0x5b + input[0x12] * 0x47 == 0)

s.add(                        input[0x15] * 0xed +
                        input[0xe] * 0x5b +
                        input[4] * -0xf + input[9] * -0xfd + input[6] * 99 + input[2] * -0xd1 +
                        input[0] * 0xf7 + input[0x13] * 0xc3 + input[0xf] * -0x6f + input[8] * 0xca +
                        input[0x10] * 0x4a + input[0x14] * 0xf9 + input[3] * 0xd3 + -0x130f0 +
                        input[0x11] * -0xfc + input[0x16] * -0xda + input[5] * 0x56 +
                        input[10] * 0x3b + input[0xb] * 0x87 + input[0xd] * -0x3a +
                        input[0xc] * -0xa9 + input[0x12] * 0xbb + input[1] * 0xb4 + input[7] * 0x8f
                        == 0)

s.add(                          input[0xf] * -0x20 +
                          input[0x16] * -0x22 +
                          input[0x15] * -0x7b + input[0xb] * -99 + input[0x13] * 0x86 +
                          input[0xe] * 0x9c + input[5] * 0x89 + input[0xd] * 0xe3 +
                          input[0x10] * -0x7c + input[3] * -0x9c + 0x8354 + input[0] * -0x45 +
                          input[1] * -0x51 + input[0x11] * -0x7d + input[7] * -0xa7 +
                          input[6] * 0xaf + input[8] * -0xcf + input[0x12] * -0xbf +
                          input[0x14] * 0x22 + input[4] * -0x3a + input[10] * -0x47 +
                          input[0xc] * -0x5d + input[2] * 0xfe + input[9] * 0xc9 == 0)

s.add(                            input[10] * 0xcc +
                            input[0x13] * 0x33 +
                            input[2] * -0x69 + input[3] * -0xa3 + input[0x10] * 0x60 +
                            input[5] * 0xea + input[0xb] * -0xb5 + input[0xc] * 0x2a +
                            input[0x14] * 0xf1 + input[6] * 0xb1 + input[0xe] * -0x14 +
                            input[9] * 0x86 + input[0x12] * -0x65 + -0x53c7 + input[1] * -0x48 +
                            input[4] * -0x30 + input[0xf] * -0xde + input[0x15] * -0x3e +
                            input[0] * 0x57 + input[8] * -0x37 + input[0xd] * 0x5a +
                            input[0x16] * 0x6c + input[0x11] * 0xd6 + input[7] * -0xe2 == 0)

s.add(                              input[4] * 0x39 +
                              input[8] * 0x23 +
                              input[3] * -0x4e + input[0xb] * -0x99 + input[0xe] * 0x47 +
                              input[6] * -0xa7 + input[9] * 0x74 + input[0x14] * 2 + 0x2d4f +
                              input[0x12] * -0x50 + input[0xd] * -0xb8 + input[0x16] * -0x4f +
                              input[0x10] * -0x31 + input[0xf] * 0xf2 + input[0] * -7 +
                              input[0xc] * -0xa4 + input[0x11] * 0xc4 + input[7] * -0x28 +
                              input[0x13] * -0xb8 + input[5] * 0xf0 + input[1] * 0x1a +
                              input[2] * -0x84 + input[10] * 0x8d + input[0x15] * -2 == 0)

s.add(                                input[4] * 0xa8 +
                                input[7] * 0xe1 +
                                input[0x12] * -0x1a + input[2] * -0x3d + input[0xf] * -0xc9 +
                                input[0x16] * -0x7f + input[0] * 0x2c + 0xeb6 + input[0xb] * 0x71 +
                                input[0x13] * -0x8f + input[0x10] * -0xdd + input[10] * -0xe1 +
                                input[6] * -0xbb + input[0x14] * 0x48 + input[0xe] * -0xb6 +
                                input[0xd] * 0xdc + input[3] * 0xf2 + input[0x15] * -0x88 +
                                input[0xc] * -0x2e + input[0x11] * 3 + input[5] * 0xb8 +
                                input[9] * 0x8c + input[8] * -0x77 + input[1] + input[1] * -8
                                == 0)

s.add(                                  input[3] * 0xad +
                                  input[2] * 0x82 + input[0xf] * 0xa7 + input[7] * 0xd0 +
                                  input[0x14] * -0x4f + input[0xc] * -0x91 + input[0x11] * -0x5a +
                                  input[0x13] * -0x100 + input[0x10] * 0x27 + input[8] * 0xec +
                                  input[0xb] * 0x3c + input[6] * -0x4a + input[5] * -0x1b +
                                  input[4] * -0x47 + input[9] * 0x8c + input[0] * -0x8e +
                                  input[0x16] * 0x65 + input[10] * -0xb9 + input[0x15] * 0x74 +
                                  input[0xd] * -0x86 + input[0xe] * 0x9e + input[1] * 0xbb +
                                  input[0x12] * -0x48 == 0x6469)

s.add(                                    input[0x12] * -0xc0 +
                                    input[4] * 0xe7 +
                                    input[5] * 9 + input[8] * 0xa4 + input[0x15] * 0xf6 +
                                    input[2] * 0xd9 + input[0x11] * 0x57 + input[0xc] * -0x88 +
                                    input[3] * 0xdd + input[0x10] * -0x8a + input[6] * -0x97 +
                                    input[1] * 0x57 + input[0x13] * 0xe2 + input[7] * 0x61 +
                                    input[0x16] * 0x6c + input[0x14] * -0xd0 + -0x1e27d +
                                    input[0xf] * 0x46 + input[9] * 0xf0 + input[0] * 0x5a +
                                    input[0xd] * -0x52 + input[10] * 0xb9 + input[0xb] * 0xb4 +
                                    input[0xe] * -0xf8 == 0)

s.add(                                      input[3] * 0xc +
                                      input[0xe] * 0x85 +
                                      input[6] * -0xa9 + input[0xb] * -0x36 + input[0x13] * -0x93 +
                                      input[8] * -0x17 + input[5] * 6 + input[0x14] * 0x99 +
                                      input[0x10] * 0xd4 + input[0xf] * 0xf2 + input[0xc] * 0xb5 +
                                      input[10] * -0xb8 + input[2] * -0x35 + input[9] * -0x98 +
                                      input[0xd] * -0xe5 + -0x65d + input[4] * 0x3f + input[0] * 0x9d
                                      + input[1] * 0xe + input[0x11] * 0xe + input[0x16] * -0xdb +
                                      input[0x12] * 0x61 + input[7] * 0x1b + input[0x15] * -0x97 ==
                                      0)

s.add(                                        input[9] * 0xf6 +
                                        input[4] * -0x28 + 0x11400 + input[0xc] * -0xb2 +
                                        input[10] * -0xe2 + input[0xd] * -0x90 + input[0x16] * 0x62
                                        + input[6] * 0xd3 + input[0x11] * -0x7a + input[0xb] * -0xad
                                        + input[8] * 0x1d + input[0x14] * 0x48 + input[2] * -0x17 +
                                        input[7] * -0x34 + input[3] * 0x9b + input[0x13] * -0x12 +
                                        input[0xf] * 0x7a + input[0x15] * -0x83 + input[0x10] * 0xac
                                        + input[5] * -0xe3 + input[0xe] * -0xb5 +
                                        input[0x12] * -0x8f + input[0] * 0xfc == 0)

s.add(                                          input[0x12] * -0x32 +
                                          input[0x13] * 0x50 +
                                          input[4] * -0x4f + input[0xb] * 0x4f + input[0] * 0x33 +
                                          input[3] * -0xab + input[8] * -0x98 + input[0x15] * -0xcb
                                          + input[0x16] * 0x6a + input[9] * 0x95 + 0xfde0 +
                                          input[2] * -0xc1 + input[6] * -0x99 + input[5] * -0x40 +
                                          input[0x14] * -0x72 + input[0xf] * -0xf9 +
                                          input[0xc] * -0xfb + input[1] * 0xdc + input[0xe] * -0xf9
                                          + input[0x11] * 0x17 + input[0x10] * -0x14 +
                                          input[7] * 0x7a + input[0xd] * 0x3d + input[10] * 0xdd ==
                                          0)

s.add(                                            input[0x16] * -0xfd +
                                            input[4] * 0x85 +
                                            input[0xb] * -0x29 + input[0x11] * 0x2a + input[0] * 0xe3
                                            + input[1] * -0x84 + input[9] * 0xad + input[6] * 0x4c +
                                            input[0x14] * 0xf4 + input[5] * -0x2d + -0x21cf +
                                            input[7] * -0xc6 + input[0xe] * 0x4c +
                                            input[0x15] * -0x5a + input[3] * 0x65 +
                                            input[0xf] * -0xfe + input[8] * -0x29 + input[2] * -0x17
                                            + input[0x13] * 0x8a + input[0xd] * -0x78 +
                                            input[0x10] * 0x6d + input[0x12] * -0x30 +
                                            input[10] * 0xa1 + input[0xc] * 0x8a == 0)

s.add(                                              input[10] * -0xb +
                                              input[0xe] * 0x54 +
                                              input[0x14] * 0x5b + input[2] * 0xda +
                                              input[3] * -0x8e + input[0x13] * 0x4c +
                                              input[0x15] * -0xec + input[0x10] * -0x81 +
                                              input[9] * -0x5c + input[0x16] * -0xdd +
                                              input[4] * 0xac + input[0xf] * 0xe5 + input[7] * -0xf9
                                              + input[8] * -0x32 + input[5] * 0xbd +
                                              input[0x12] * -0xbd + input[0xd] * -100 +
                                              input[0xb] * 0x5d + input[1] * 0x8b +
                                              input[0xc] * 0x89 + input[0] * -0x1e +
                                              input[0x11] * -0x7c + -0x9bf + input[6] * -0x1e == 0)

s.add(                                                input[0xb] * -0xe2 +
                                                input[6] * -0x4b +
                                                input[0x15] * -10 + input[8] * 0x33 +
                                                input[0x16] * 0x72 + input[0x14] * -0x80 +
                                                input[5] * -0xdf + input[7] * 0xf9 + input[4] * 0x11
                                                + input[0x11] * -0xc1 + input[0] * 0x74 +
                                                input[0x12] * 0xf6 + input[0x10] * 0xdc +
                                                input[0xf] * 0x65 + input[0xe] * 0xb2 +
                                                input[0xc] * -0x42 + input[10] * -0x42 +
                                                input[2] * 0x24 + input[9] * -0xd4 +
                                                input[0x13] * 0x73 + input[0xd] * -0x86 +
                                                input[3] * 0xd7 + -0xe3f6 + input[1] * 0x76 == 0)

s.add(                                                  input[0x10] * -0x9c +
                                                  input[2] * 0x67 +
                                                  input[0xc] * -0x23 + input[8] * -0x48 +
                                                  input[6] * -0xd7 + input[7] * -0x84 +
                                                  input[1] * 10 + input[0xe] * -0xd7 +
                                                  input[0xb] * 0x62 + input[0xf] * -0x51 +
                                                  input[0] * 0xbc + input[0x16] * -0x4c + 0xd3bb +
                                                  input[0x13] * -0x98 + input[0xd] * -0x53 +
                                                  input[0x11] * -0x77 + input[0x15] * -0x6c +
                                                  input[3] * 0x74 + input[0x14] * 0x38 +
                                                  input[5] * 0x46 + input[9] * -0x9c +
                                                  input[4] * 0xdb + input[10] * -0x76 +
                                                  input[0x12] * 0x2e == 0)
print('CRACK')

print(s.check())
m = s.model()
print(m)

flag = ''
for i in range(23):
	flag += chr(m[input[i]].as_long())

print(flag)