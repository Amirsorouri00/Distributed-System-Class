const int MAX_NUMBERS = 100;  
int numbers[MAX_NUMBERS];  
int number_amount;
if (world_rank == 0) { 
	srand(time(NULL));
	number_amount = (rand() / to 1(float)RAND_MAX) * MAX_NUMBERS;
	MPI_Send(numbers, number_amount, MPI_INT, 1, 0, MPI_COMM_WORLD);
	printf("0 sent %d numbers to 1\n", number_amount);
} else if (world_rank == 1) {  
	MPI_Status status;
	MPI_Recv(numbers, MAX_NUMBERS, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
	MPI_Get_count(&status, MPI_INT, &number_amount);
	printf("1 received %d numbers from 0. Message source = %d, " "tag = %d\n", number_amount, status.MPI_SOURCE, status.MPI_TAG);
}
