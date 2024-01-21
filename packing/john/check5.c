#include <stdio.h>
#include <math.h>

int inner_check5(int a5, long int a6)
{
  long double v6;
  long double v7;
  long int v8;
 
  v6 = sqrt((double)a5);
  v7 = powl((long double)a5, v6);
  if ( v7 >= 9.223372036854775808e18 )
  {
    v8 = (long int)(v7 - 9.223372036854775808e18);
    v8 ^= 0x8000000000000000;
  }
  else
  {
    v8 = (long int)v7;
  }
  return a6 == v8 + 21;
}

long int list[] = {0x0000001ca66fe7dd, 0x227357afcf8, 0x15,
				    0x0000016c5c156c54, 0x1ca66fe7dd, 0x9de93ece66,
				    0x16c5c156c54, 0x16c5c156c54, 0x756f3444241,
				    0x14660a4c5, 0x1ca66fe7dd
				  };

int main() {
  int result;

  printf("%s", "Flag: flag{packer"); // FOUND FROM STEP 1,2,3

  char c;
  for(int i=0; i<11; i++) {
  	for(char j = 0x20; j <= 0x7e; j++) {
  		result = inner_check5(j, list[i]);
  		if(result == 1) {
  			printf("%c", j);
  			break;
  		}
  	}
  }

  printf("%s", "annoying__}\n"); // FOUND FROM STEP 6

  return 0;
}