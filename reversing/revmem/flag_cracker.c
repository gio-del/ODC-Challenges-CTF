
#include <stdio.h>

int main(int argc, char *argv[]) {
    unsigned char key[] = { 0x66, 0x0a, 0x0d, 0x06, 0x1c, 0x0f, 0x1c, 0x01, 0x1a, 0x2c, 0x28, 0x16, 0x12, 0x2c, 0x3e, 0x0f, 0x31, 0x3a, 0x04, 0x12, 0x0a, 0x26, 0x2d, 0x17, 0x13, 0x13, 0x17, 0x01, 0x16, 0x18, 0x6a, 0x17, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

    char flag[30];

    char tmp = 0;

    for(int i = 0; i < 0x1e; i++) {
    	flag[i] = key[i] ^ tmp;
    	tmp = flag[i];
    }

    printf("Decoded Flag: %s\n", flag);

    return 0;
}