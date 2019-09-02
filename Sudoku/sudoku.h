#ifndef _SUDOKU_H_
#define _SUDOKU_H_

#include <stdio.h>
#include <stdlib.h>
#include <unordered_set>

#define lin(pos) pos/DIM
#define col(pos) pos%DIM

#define DIM 9
#define ROOT 3

using namespace std;

/* Le uma matriz de tamanho DIM */
void sudoku_input(int sudoku[DIM][DIM]);

/* Verifica se o jogo já acabou */
bool is_over(int pos);

/* Resolve o tabuleiro de forma recursiva usando back_tracking */
void sudoku_back_tracking(int sudoku[DIM][DIM], int pos);

/* Procura o tabuleiro por possíveis valores em certa posição */
void find_possible_numbers(unordered_set<int> &movements, int sudoku[DIM][DIM], int pos);

/* Imprime uma matriz de tamanho DIM e suas posições */
void sudoku_full_print(int sudoku[DIM][DIM]);

/* Imprime o tabuleiro */
void sudoku_print(int sudoku[DIM][DIM]);


#endif