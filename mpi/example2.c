#include <mpi.h> 
#include <stdio.h>

int main(int argc, char **argv)
{
	MPI_Init(&argc, &argv);  
	int myRank, size;
	MPI_Comm_size(MPI_COMM_WORLD,&size);
	MPI_Comm_rank(MPI_COMM_WORLD, &myRank); 
	int number; 
	if (myRank == 0) {  
		number = 10;  
		printf("Process 0 has number %d and my rank is = %d.\n", number, myRank);
		MPI_Send(&number, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
	} else if (myRank == 1) {
		MPI_Recv(&number, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		printf("Process 1 received number %d from process 0 and myRank is = %d. \n", number, myRank);
	}
	MPI_Finalize();
	return 0;
}
