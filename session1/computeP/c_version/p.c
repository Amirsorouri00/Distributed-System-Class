#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define n   300000

int main(){
    double x, y, z;
    int m = 0;
    srand(time(NULL));
    for (int i = 0; i < n; i++){
        x = rand() / (double) RAND_MAX;
        y = rand() / (double) RAND_MAX;
        z = pow(x,2) + pow(y,2);
        if(z < 1) m++;
    }
    printf("m = %d\n", m);
    printf("final Value is: %f\n", 4*(double)m/(double)n);
    return 0;
}
