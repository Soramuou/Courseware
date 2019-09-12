#include <stdio.h>
#define WriteLine() printf("\n");
#define WriteLong(x) printf(" %lld", (long)x);
#define ReadLong(a) if (fscanf(stdin, "%lld", &a) != 1) a = 0;
#define long long long

const long n = 270;

long i, j, maxi;
long k, max;


void main(){//sdfs
  max = 0; /*sdfsdf*/
  i = 5;
  while (max < n) {
    k = 0;
    j = i;
    while (j != 4) {
      if ((j % 2) == 1) {
        j = (j+j+j+1) / 2;
        k = k + 2;
      } else {
        j = j / 2;
        k = k + 1;
      }
    }
    if (k > max) {
      max = k;
      maxi = i;
      WriteLong(max+2);
      WriteLong(maxi);
      WriteLine();
    }
    i = i + 1;
  }
  WriteLong(max+2);
  WriteLong(maxi);
  WriteLine();
}
