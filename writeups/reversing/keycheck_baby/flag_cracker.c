
#include <stdio.h>

int main(int argc, char *argv[]) {
    unsigned char magic0[] = { 0x1b, 0x51, 0x17, 0x2a, 0x1e, 0x4e, 0x3d, 0x10, 0x17, 0x46, 0x49, 0x14, 0x3d };
    unsigned char magic1[] = { 0xeb, 0x51, 0xb0, 0x13, 0x85, 0xb9, 0x1c, 0x87, 0xb8, 0x26, 0x8d, 0x07 };

    char flag[32];

    flag[0] = 'f';
    flag[1] = 'l';
    flag[2] = 'a';
    flag[3] = 'g';
    flag[4] = '{';

    for(int i = 0; i < 0xd; i++) {
        flag[i+5] = "babuzz"[i%6] ^ magic0[i];
    }

    char j = -0x45;
    for(int i = 0xd; i < 0xc + 0xd; i++) {
        flag[i+5] = magic1[i-0xd] - j;
        j = j + flag[i+5];
    }

    flag[30] = '}';
    flag[31] = '\0';
    printf("\n");

    printf("Decoded Flag: %s\n", flag);

    return 0;
}