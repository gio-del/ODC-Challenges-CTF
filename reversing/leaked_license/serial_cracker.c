#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]) {
	int i,k;
	unsigned long long license_byte;

	char license_ptr[] = { 0x5e, 0x0e, 0xd4, 0x8d, 0x00, 0x00, 0x00, 0x00, 0x28, 0xb8, 0x27, 0xcd, 0x00, 0x00, 0x00, 0x00, 0xf3, 0x54, 0x60, 0x37, 0x00, 0x00, 0x00, 0x00, 0x3a, 0xc8, 0x50, 0xf1, 0x00, 0x00, 0x00, 0x00, 0x82, 0xa5, 0x8c, 0xa5, 0x00, 0x00, 0x00, 0x00, 0x30, 0x69, 0x4b, 0xb8, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x5f, 0xfe, 0x4a, 0x00, 0x00, 0x00, 0x00, 0x9e, 0x45, 0x39, 0x91, 0x00, 0x00, 0x00, 0x00, 0x16, 0xb3, 0xb2, 0x88, 0x00, 0x00, 0x00, 0x00, 0x72, 0xbe, 0x5d, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x35, 0x4c, 0xa3, 0xd2, 0x00, 0x00, 0x00, 0x00, 0xd8, 0x55, 0xa4, 0x13, 0x00, 0x00, 0x00, 0x00, 0x1c, 0xa6, 0xec, 0x00, 0x00, 0x00, 0x00, 0x00, 0x31, 0x8d, 0x14, 0xb7, 0x00, 0x00, 0x00, 0x00, 0xfb, 0x0b, 0xc8, 0x5b, 0x00, 0x00, 0x00, 0x00, 0xf1, 0x3f, 0x03, 0xc5, 0x00, 0x00, 0x00, 0x00, 0x84, 0x73, 0xd7, 0x76, 0x00, 0x00, 0x00, 0x00, 0x5e, 0xe4, 0x19, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x42, 0x12, 0x4d, 0x00, 0x00, 0x00, 0x00, 0xcf, 0x88, 0xe8, 0x94, 0x00, 0x00, 0x00, 0x00, 0x41, 0xd1, 0x72, 0xd4, 0x00, 0x00, 0x00, 0x00, 0x12, 0x86, 0x3c, 0xae, 0x00, 0x00, 0x00, 0x00, 0x44, 0x5e, 0x1e, 0x86, 0x00, 0x00, 0x00, 0x00, 0xb8, 0x9d, 0xde, 0xf3, 0x00, 0x00, 0x00, 0x00, 0x96, 0x05, 0x0e, 0x19, 0x00, 0x00, 0x00, 0x00, 0x78, 0x3b, 0xc6, 0xd6, 0x00, 0x00, 0x00, 0x00, 0x3d, 0x47, 0x9e, 0xc7, 0x00, 0x00, 0x00, 0x00, 0xad, 0x84, 0xf3, 0x82, 0x00, 0x00, 0x00, 0x00, 0x52, 0xf3, 0xec, 0xbf, 0x00, 0x00, 0x00, 0x00, 0x73, 0xa2, 0xe5, 0x19, 0x00, 0x00, 0x00, 0x00, 0x53, 0x88, 0x24, 0x05, 0x00, 0x00, 0x00, 0x00, 0x36, 0x0d, 0x38, 0x64, 0x00, 0x00, 0x00, 0x00, 0x23, 0x2d, 0x56, 0x10, 0x00, 0x00, 0x00, 0x00, 0x37, 0xf2, 0xe0, 0x51, 0x00, 0x00, 0x00, 0x00, 0xb5, 0xd5, 0xa4, 0xfe, 0x00, 0x00, 0x00, 0x00, 0xb2, 0x3f, 0xe6, 0x62, 0x00, 0x00, 0x00, 0x00, 0x45, 0xb6, 0x9f, 0xbc, 0x00, 0x00, 0x00, 0x00, 0x89, 0xaf, 0x43, 0xec, 0x00, 0x00, 0x00, 0x00, 0x56, 0x42, 0x8d, 0x1f, 0x00, 0x00, 0x00, 0x00, 0x17, 0x74, 0x9f, 0xc2, 0x00, 0x00, 0x00, 0x00, 0x3a, 0xfa, 0x72, 0x6d, 0x00, 0x00, 0x00, 0x00, 0xd5, 0x52, 0xed, 0x8e, 0x00, 0x00, 0x00, 0x00, 0xfb, 0x0f, 0x98, 0x58, 0x00, 0x00, 0x00, 0x00, 0x3f, 0x29, 0x88, 0xc8, 0x00, 0x00, 0x00, 0x00, 0xc3, 0xeb, 0x9f, 0xd9, 0x00, 0x00, 0x00, 0x00, 0x72, 0xd0, 0xbd, 0xaa, 0x00, 0x00, 0x00, 0x00, 0x1b, 0xb6, 0xac, 0x6d, 0x00, 0x00, 0x00, 0x00, 0x60, 0x0a, 0xa7, 0x82, 0x00, 0x00, 0x00, 0x00, 0xe0, 0xba, 0x48, 0x35, 0x00, 0x00, 0x00, 0x00, 0x87, 0x6a, 0x28, 0x73, 0x00, 0x00, 0x00, 0x00, 0x23, 0x35, 0xe6, 0xab, 0x00, 0x00, 0x00, 0x00, 0x59, 0xc6, 0xa0, 0x5c, 0x00, 0x00, 0x00, 0x00, 0x2a, 0xa0, 0x62, 0x38, 0x00, 0x00, 0x00, 0x00, 0x8f, 0x7b, 0x6e, 0xc5, 0x00, 0x00, 0x00, 0x00, 0xe7, 0xd3, 0xd7, 0x2f, 0x00, 0x00, 0x00, 0x00, 0xd2, 0xce, 0x45, 0x09, 0x00, 0x00, 0x00, 0x00, 0x16, 0xd5, 0xe4, 0xc3, 0x00, 0x00, 0x00, 0x00, 0x6b, 0x97, 0x5d, 0x47, 0x00, 0x00, 0x00, 0x00, 0xc9, 0x5d, 0x8c, 0x2e, 0x00, 0x00, 0x00, 0x00, 0xe0, 0xf6, 0x81, 0x6b, 0x00, 0x00, 0x00, 0x00, 0x58, 0x0c, 0xa1, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd8, 0xde, 0x18, 0x14, 0x00, 0x00, 0x00, 0x00, 0xd7, 0xe2, 0x0b, 0x67, 0x00, 0x00, 0x00, 0x00, 0x80, 0x22, 0x2d, 0xda, 0x00, 0x00, 0x00, 0x00, 0xbf, 0xc6, 0x9d, 0x56, 0x00, 0x00, 0x00, 0x00, 0x09, 0xbf, 0x5b, 0xf4, 0x00, 0x00, 0x00, 0x00, 0x40, 0x91, 0x42, 0xc8, 0x00, 0x00, 0x00, 0x00, 0xe6, 0x76, 0x94, 0x43, 0x00, 0x00, 0x00, 0x00, 0x59, 0xf5, 0x90, 0x43, 0x00, 0x00, 0x00, 0x00, 0x19, 0x50, 0x14, 0xd2, 0x00, 0x00, 0x00, 0x00, 0xbb, 0x65, 0x28, 0x99, 0x00, 0x00, 0x00, 0x00, 0xec, 0x57, 0x62, 0x65, 0x00, 0x00, 0x00, 0x00, 0xa0, 0xc9, 0x0d, 0xa1, 0x00, 0x00, 0x00, 0x00, 0x97, 0xab, 0xfb, 0x1d, 0x00, 0x00, 0x00, 0x00, 0x9f, 0x7a, 0xd5, 0x61, 0x00, 0x00, 0x00, 0x00, 0x34, 0x0a, 0xe7, 0x30, 0x00, 0x00, 0x00, 0x00, 0xa6, 0xee, 0x68, 0xc9, 0x00, 0x00, 0x00, 0x00, 0x14, 0x8b, 0x8a, 0xe2, 0x00, 0x00, 0x00, 0x00, 0x66, 0x17, 0x64, 0x8b, 0x00, 0x00, 0x00, 0x00, 0x1e, 0xf9, 0x5b, 0xba, 0x00, 0x00, 0x00, 0x00, 0x45, 0xea, 0x1c, 0xae, 0x00, 0x00, 0x00, 0x00, 0xf6, 0x8a, 0xa7, 0x29, 0x00, 0x00, 0x00, 0x00, 0x98, 0xdc, 0x9a, 0x6f, 0x00, 0x00, 0x00, 0x00, 0xdb, 0xe0, 0x32, 0xce, 0x00, 0x00, 0x00, 0x00, 0x3a, 0xb2, 0xbd, 0x9e, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x80, 0x04, 0xd0, 0x00, 0x00, 0x00, 0x00, 0xdd, 0xf5, 0x2b, 0xad, 0x00, 0x00, 0x00, 0x00, 0xde, 0x51, 0x2b, 0xed, 0x00, 0x00, 0x00, 0x00, 0xbf, 0x0f, 0x9f, 0x6d, 0x00, 0x00, 0x00, 0x00, 0xad, 0xfa, 0xd7, 0xb8, 0x00, 0x00, 0x00, 0x00, 0xcf, 0xd2, 0xd1, 0x21, 0x00, 0x00, 0x00, 0x00, 0x37, 0x13, 0x12, 0x4d, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x1e, 0x82, 0xd0, 0x00, 0x00, 0x00, 0x00, 0x55, 0x91, 0xef, 0x57, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x79, 0xc0, 0xbb, 0x00, 0x00, 0x00, 0x00, 0xfc, 0x32, 0xf9, 0x93, 0x00, 0x00, 0x00, 0x00, 0xfa, 0x08, 0xd1, 0x24, 0x00, 0x00, 0x00, 0x00, 0x03, 0x56, 0x47, 0xb4, 0x00, 0x00, 0x00, 0x00, 0x77, 0xa9, 0xc2, 0x0d, 0x00, 0x00, 0x00, 0x00, 0x59, 0x38, 0xee, 0xe1, 0x00, 0x00, 0x00, 0x00, 0xd5, 0xcd, 0x2f, 0xe7, 0x00, 0x00, 0x00, 0x00, 0x6c, 0xb8, 0x29, 0x14, 0x00, 0x00, 0x00, 0x00, 0x03, 0xa7, 0xe9, 0x41, 0x00, 0x00, 0x00, 0x00, 0xd6, 0x61, 0x3b, 0x91, 0x00, 0x00, 0x00, 0x00, 0xa5, 0xbd, 0xa4, 0x3b, 0x00, 0x00, 0x00, 0x00, 0xc5, 0xa5, 0x5b, 0x5f, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x53, 0x5b, 0x3f, 0x00, 0x00, 0x00, 0x00, 0x59, 0xc7, 0x6e, 0xfa, 0x00, 0x00, 0x00, 0x00, 0x54, 0xa1, 0xd6, 0x68, 0x00, 0x00, 0x00, 0x00, 0xeb, 0x00, 0x45, 0x1b, 0x00, 0x00, 0x00, 0x00, 0x24, 0x88, 0xcb, 0xf1, 0x00, 0x00, 0x00, 0x00, 0xea, 0x04, 0xc5, 0x8e, 0x00, 0x00, 0x00, 0x00, 0xf6, 0xa4, 0xc1, 0xc4, 0x00, 0x00, 0x00, 0x00, 0x3b, 0xd3, 0xe8, 0x6c, 0x00, 0x00, 0x00, 0x00, 0xc2, 0xc4, 0x34, 0xec, 0x00, 0x00, 0x00, 0x00, 0xd5, 0x92, 0x3c, 0x70, 0x00, 0x00, 0x00, 0x00, 0xb3, 0x99, 0xd8, 0x9f, 0x00, 0x00, 0x00, 0x00, 0x1c, 0x81, 0x50, 0x99, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xff, 0xd3, 0x23, 0x00, 0x00, 0x00, 0x00, 0xd1, 0x68, 0x0b, 0x59, 0x00, 0x00, 0x00, 0x00, 0x09, 0x9e, 0xe9, 0x66, 0x00, 0x00, 0x00, 0x00, 0xa9, 0x19, 0x02, 0xa3, 0x00, 0x00, 0x00, 0x00, 0xfc, 0x96, 0xaf, 0x78, 0x00, 0x00, 0x00, 0x00, 0x48, 0x49, 0x5f, 0x56, 0x00, 0x00, 0x00, 0x00, 0x0e, 0xb5, 0x00, 0x31, 0x00, 0x00, 0x00, 0x00, 0x85, 0xb7, 0x90, 0xe5, 0x00, 0x00, 0x00, 0x00, 0x45, 0xf6, 0xb4, 0xd4, 0x00, 0x00, 0x00, 0x00, 0xa9, 0xd7, 0x0a, 0x75, 0x00, 0x00, 0x00, 0x00, 0x64, 0xce, 0x97, 0xd1, 0x00, 0x00, 0x00, 0x00, 0x65, 0x87, 0x87, 0x26, 0x00, 0x00, 0x00, 0x00, 0xa7, 0xe9, 0x6f, 0x6a, 0x00, 0x00, 0x00, 0x00, 0x6d, 0xd9, 0x93, 0xd6, 0x00, 0x00, 0x00, 0x00, 0xf5, 0x01, 0xf5, 0xb5, 0x00, 0x00, 0x00, 0x00, 0xa3, 0x6d, 0x72, 0xd8, 0x00, 0x00, 0x00, 0x00, 0xf4, 0xc6, 0x4c, 0x25, 0x00, 0x00, 0x00, 0x00, 0xf5, 0x79, 0x76, 0x23, 0x00, 0x00, 0x00, 0x00, 0xe0, 0x6f, 0xbf, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0xa1, 0x9a, 0x65, 0x00, 0x00, 0x00, 0x00, 0x4a, 0x85, 0x65, 0x43, 0x00, 0x00, 0x00, 0x00, 0xd9, 0xfe, 0x66, 0x34, 0x00, 0x00, 0x00, 0x00, 0x83, 0xc0, 0xb8, 0x86, 0x00, 0x00, 0x00, 0x00, 0x19, 0x47, 0xce, 0x1d, 0x00, 0x00, 0x00, 0x00, 0x9c, 0x6f, 0x3d, 0xa0, 0x00, 0x00, 0x00, 0x00, 0x8b, 0xd4, 0x7e, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf3, 0x88, 0x5f, 0x45, 0x00, 0x00, 0x00, 0x00, 0xa5, 0x24, 0x17, 0x13, 0x00, 0x00, 0x00, 0x00, 0xc4, 0x99, 0x61, 0xc5, 0x00, 0x00, 0x00, 0x00, 0xc9, 0x9d, 0x76, 0x16, 0x00, 0x00, 0x00, 0x00, 0x53, 0xf0, 0x6c, 0xec, 0x00, 0x00, 0x00, 0x00, 0x57, 0xb8, 0x7c, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x7a, 0xc2, 0x20, 0x00, 0x00, 0x00, 0x00, 0x8c, 0x25, 0xad, 0xde, 0x00, 0x00, 0x00, 0x00, 0xa6, 0x67, 0xa6, 0x35, 0x00, 0x00, 0x00, 0x00, 0x60, 0xfe, 0xf9, 0x60, 0x00, 0x00, 0x00, 0x00, 0x08, 0xc3, 0x9c, 0x33, 0x00, 0x00, 0x00, 0x00, 0xb2, 0x27, 0x26, 0x8e, 0x00, 0x00, 0x00, 0x00, 0x46, 0x5e, 0xee, 0xf3, 0x00, 0x00, 0x00, 0x00, 0x55, 0x37, 0x48, 0x64, 0x00, 0x00, 0x00, 0x00, 0xa1, 0xbc, 0xe4, 0xb4, 0x00, 0x00, 0x00, 0x00, 0xcb, 0x63, 0x14, 0x4a, 0x00, 0x00, 0x00, 0x00 };
	char license_ptr_target[1279];

	char target_license[] = "726cfc2d26c6defedb06562199f5c7d0da4f4930";
	for (i = 0; i < 5; i = i + 1) {
    	license_byte = 0;
    	for (k = 0; k < 32; k = k + 1) {
      		license_byte = license_byte << 1 |
                     (unsigned long)(*(long *)(license_ptr + (long)(k + i * 32) * 8) << ((char)k & 63)) >> 31 & 1;
            printf("%04llx\n",license_byte);
    }
    	printf("\n\n%04llx\n",license_byte);
  }

  	target_license_bytes = "726cfc2d" // troviamo license_ptr_target per generare 726cfc2d*5
  	for(i=0; i<5; i++) {
  		for(k=0; k < 32; k++) {
  			license_ptr[(k+i*32)*8] = ??
  		}
  	}
}