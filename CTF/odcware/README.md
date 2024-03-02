The binary takes: <program> <flag>

It checks that program starts with OWPROG

It execute this code for each character of the flag: 0001 0400 0000 0100 0300 0000 0002 0600 0000

The semantic of the code is found by reverse engineering the binary

1) 01 00 00 	// a = flag[curr_idx]
2) 04 00 00 	// a = flag[curr_idx + 3] ^ a ^ flag[curr_idx + 1] ^ flag[curr_idx + 2]; (circular)
3) 00 01 00 	// b = key[curr_idx]
4) 03 00 00 	// set if a==b
5) 02 00 00 	// if(a!=b) fail
6) 06 00 00 	// curr_idx++
