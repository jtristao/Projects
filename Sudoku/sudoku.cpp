#include "sudoku.h"

void sudoku_input(int sudoku[DIM][DIM]){
	for(int i = 0; i < DIM; i++)
		for(int j = 0; j < DIM; j++)
			scanf("%d", &sudoku[i][j]);
}

void sudoku_full_print(int sudoku[DIM][DIM]){
	for(int i = 0; i < DIM; i++){
		for(int j = 0; j < DIM; j++)
			printf("%6d(%2d) ", sudoku[i][j], i*DIM + j);
		printf("\n");
	}
}

void sudoku_print(int sudoku[DIM][DIM]){
	for(int i = 0; i < DIM; i++){
		for(int j = 0; j < DIM; j++){
			printf("%6d", sudoku[i][j]);
			if(j % ROOT == ROOT-1)
				printf("\t");
		}
		printf("\n");
		if(i % ROOT == ROOT-1)
			printf("\n");
	}
}

bool is_over(int pos){
	return pos == DIM*DIM-1 ? true : false;
}

void find_possible_numbers(unordered_set<int> &movements, int sudoku[DIM][DIM], int pos){
	int start = ((pos/DIM)/ROOT)*(DIM*ROOT) + ((pos%DIM)/ROOT)*ROOT;

	for(int i = 0; i < DIM; i++)
		movements.insert(i+1);

	for(int i = 0; i < DIM; i++){
		// Procura a linha relacionada com aquela posição
		if(sudoku[lin(pos)][i] != 0)
			movements.erase(sudoku[lin(pos)][i]);

		// Procura a col relacionada com aquela posição
		if(sudoku[i][col(pos)] != 0)
			movements.erase(sudoku[i][col(pos)]);

		// Procura a diagonal relacionada com aquela posição
		if(sudoku[lin(start)][col(start)] != 0)
			movements.erase(sudoku[lin(start)][col(start)]);

		start++;
		if(i%ROOT == ROOT-1)
			start+=(DIM-ROOT);
	}
}

void sudoku_back_tracking(int sudoku[DIM][DIM], int pos){
	
	if(is_over(pos)){
		sudoku_print(sudoku);
		exit(0);
	}
	else if(sudoku[lin(pos)][col(pos)] != 0)
		sudoku_back_tracking(sudoku, pos+1);
	else{
		unordered_set<int> movements;
		find_possible_numbers(movements, sudoku, pos);
		for(unordered_set<int>::iterator it = movements.begin(); it != movements.end(); it++){
			sudoku[lin(pos)][col(pos)] = *it;
			sudoku_back_tracking(sudoku, pos+1);
			sudoku[lin(pos)][col(pos)] = 0;		
		}
	}
}