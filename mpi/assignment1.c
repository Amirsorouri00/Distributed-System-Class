#include <mpi.h> 
#include <stdio.h>
#include <stdlib.h>

const int row_col = 64;
int mat_dim = 64*64;

void 
mat_init(int **A, int **B, int **C, int **D) {
    for (int i = 0; i< row_col; i++) {
        for (int j = 0;j<row_col;j++) {
            A[i][j] = i*j;
            B[i][j] = i*i;
            C[i][j] = -1;
            D[i][j] = -1;
        }
    } 
    return;
}

int 
merge(int **D, int **mat) {
    int cnt = 0;
    for (int i = 0; i< row_col; i++) {
        for (int j = 0;j<row_col; j++) {
            if (mat[i][j] != -1) {
                D[i][j] = mat[i][j];
                cnt++;
            }
        }
    }
    return cnt;        
}

void 
mat_multiplication(int **A, int **B, int **C, int size, int myRank) {
    int i,j,k, res = 0;
    for (i = 0; i < row_col; i++) {
      for (j = 0; j < row_col; j++) {
        if((row_col*i + j)%size == myRank) {
        // if((i+j)%slice == myRank) {
            for (k = 0; k < row_col; k++) {
               res = res + (A[i][k] * B[k][j]);
            }
            C[i][j] = res;
            res = 0;
        }
      }
    }
}

void 
print_mat(int **mat) {

    for (int i = 0; i<row_col; i++) {
        printf("[");
        for (int j = 0;j<row_col;j++) {
            printf("%d, ", mat[i][j]);
        }
        printf("]\n");
    }
    return;
}

int 
main(int argc, char **argv) {

    int **A, **B, **C, **D;
    A = (int**) malloc(sizeof(int *) * row_col);
    B = (int**) malloc(sizeof(int *) * row_col);
    C = (int**) malloc(sizeof(int *) * row_col);
    D = (int**) malloc(sizeof(int *) * row_col);
    
    for (int i = 0; i < row_col; i++)
    {
        A[i] = (int*) malloc(sizeof(int) * row_col);
        B[i] = (int*) malloc(sizeof(int) * row_col);
        C[i] = (int*) malloc(sizeof(int) * row_col);
        D[i] = (int*) malloc(sizeof(int) * row_col);
    }
    printf("%p\t%p\t%p\t%p\n", A, B, C, D);
    mat_init(A, B, C, D);        

    int myRank, size; 	
    MPI_Init(&argc, &argv);  
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Comm_rank(MPI_COMM_WORLD, &myRank); 

    if (myRank == 0) {  
    	int **res = (int**) malloc(sizeof(int *) * row_col);
        for (int i = 0; i < row_col; i++)
            res[i] = (int*) malloc(sizeof(int) * row_col);
        for (int i = 0; i < row_col; i++)
            for (int j = 0; j < row_col; j++)
                res[i][j] = -3;

        mat_multiplication(A, B, C, size, myRank);

        int merged = merge(res, C);
        print_mat(C);

        for (int i = 1; i <= size - 1; i++)
        {
            MPI_Status status; int number_amount;
            for (int j = 0; j < row_col; j++)
                MPI_Recv(&(D[j][0]), row_col, MPI_INT, i, 0, MPI_COMM_WORLD, &status);

            MPI_Get_count(&status, MPI_INT, &number_amount);
            int merged2 = merge(res, D);
            print_mat(D);
        }
            print_mat(res);

    } else {
        mat_multiplication(A, B, D, size, myRank);
        for (int i = 0; i < row_col; i++)
    	    MPI_Send(&(D[i][0]), row_col, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }
    MPI_Finalize();
    return 0;
}
