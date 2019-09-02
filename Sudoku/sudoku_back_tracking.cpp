/**************************************************************************
	Author: João V. Tristão
	Date: 
	Problem: 
	Approach:

**************************************************************************/

#include <cstdio>
#include <cstdlib>

#include "sudoku.h"

int main(int argc, char *argv[]){
	int sudoku[DIM][DIM];

	sudoku_input(sudoku);

	sudoku_back_tracking(sudoku, 0);

	return EXIT_SUCCESS;
}