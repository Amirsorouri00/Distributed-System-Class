#include <stdio.h>

int a [64][64] = {};
int b [64][64] = {};


void 
print_mat(int (*mat)[64]) {

    for (int i = 0; i< 64; i++) {
        printf("[");
        for (int j = 0;j<64;j++) {
            printf("%d, ", mat[i][j]);
        }
        printf("]\n");
    }
    return;
}


int 
main(int argc, char **argv) {

    for (int i = 0; i< 64; i++)
        for (int j = 0;j<64;j++) 
            a[i][j] = i*j;
    
    for (int i = 0; i< 64; i++)
        for(int j = 0; j< 64; j++)
            b[i][j] = i*i;
    
	printf("matrix a: \n");
    print_mat(a);
	printf("\n matrix b: \n");
    print_mat(b);

	return 0;
}
