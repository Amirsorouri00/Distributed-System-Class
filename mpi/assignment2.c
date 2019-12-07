#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <mpi.h> 

#define lower   10000
#define upper   100000

int  
generate_random(int l, int u, int myRank) { 
    srand(myRank);
    int i;
    int rand_num = (rand() % (u - l + 1)) + l;
    return rand_num;
}

int 
compute_p(int N, int myRank) {
    double x, y, z;
    int M = 0;
    srand(time(NULL));
    for (int i = 0; i < N; i++){
        x = rand() / (double) RAND_MAX;
        y = rand() / (double) RAND_MAX;
        z = (x*x) + (y*y);
        if(z <= 1) M++;
    }
    return M;
}

void
addsup(int myN_M [2], int N_M [2]) {
    myN_M[0] += N_M[0];
    myN_M[1] += N_M[1];
    return;    
}

int 
main(int argc, char **argv) {

    int myRank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Comm_rank(MPI_COMM_WORLD, &myRank);

    int myN_M [2] = {};
    int N_M[2] = {};
    myN_M[0] = generate_random(lower, upper, myRank);
    myN_M[1] = compute_p(myN_M[0], myRank);

    if (myRank == 0) {
        MPI_Status status; int number_amount;
        MPI_Recv(&N_M, 2, MPI_INT, myRank + 1, 0, MPI_COMM_WORLD, &status);
        addsup(myN_M, N_M);
        printf("Process %d: P number calculated by the whole system with size %d and M:N = %d:%d and finally ==> P = %f \n", myRank, size, myN_M[1], myN_M[0], 4*(double)myN_M[1]/myN_M[0]);

    } else if (myRank == size - 1) {
        MPI_Send(&myN_M, 2, MPI_INT, myRank - 1, 0, MPI_COMM_WORLD);
    } else {
        MPI_Status status; int number_amount;
        MPI_Recv(&N_M, 2, MPI_INT, myRank + 1, 0, MPI_COMM_WORLD, &status);
        addsup(myN_M, N_M);
        MPI_Send(&myN_M, 2, MPI_INT, myRank - 1, 0, MPI_COMM_WORLD);
    }
    MPI_Finalize();
    return 0;
}
