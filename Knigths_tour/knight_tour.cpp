#include <bits/stdc++.h> 

using namespace std;

// transofrmar create em um construtor


class Horse{
	private:
		int x, y;
		
	public:
		int moves[8][2] = { {-2, -1},
							{-1, -2},
						  	{ 1, -2},
							{ 2, -1},
							{ 2,  1},
							{ 1,  2},
							{-1,  2},
							{-2,  1} };

		Horse(){
			this->x = 0;
			this->y = 0;
		}

		Horse(int a, int b){
			this->x = a;
			this->y = b;
		}

		void move(pair<int, int> coord){
			this->x += coord.first;
			this->y += coord.second;
		}

		void un_move(pair<int, int> coord){
			this->x -= coord.first;
			this->y -= coord.second;
		}

		int get_x(){
			return this->x;
		}

		int get_y(){
			return this->y;
		}

		void print(){
			cout << "(" << this->x << ", " << this->y << ")" << endl;
		}
};


class Board{
	private:
		vector<vector<int>> table;
		int dimension;
		int n_free;

	public:
		void create(int dim){
			for(int i = 0; i < dim; i++){
				vector<int>aux(dim, 0);
				this->table.push_back(aux);
			}
			this->n_free = dim*dim;
			this->dimension = dim;
		}

		int get_dimension(){
			return this->dimension;
		}

		void print(){
			for(int i = 0; i < this->dimension; i++){
				for(int j = 0; j < this->dimension; j++)
					cout << this->table[i][j] << " ";
				cout << endl;
			}
			cout << endl;
		}

		bool over(){
			if(this->n_free == 0)
				return true;
			else
				return false;
		}

		void update(Horse h, int i){
			int pos = this->table[h.get_x()][h.get_y()]; 
			if(pos == 0){
				this->table[h.get_x()][h.get_y()] = i;
				this->n_free--;
			}else{
				this->table[h.get_x()][h.get_y()] = i;
				this->n_free++;
			}
		}

		bool is_free(int x, int y){
			if(x >= 0 && x < this->dimension && y >= 0 && y < this->dimension){
				if(this->table[x][y] == 0)
					return true;
			}

			return false;	
		}
};

vector<pair<int, int>> find_movements(Board b, Horse h){
	vector<pair<int, int>> ret;
	pair<int, int> aux;

	for(int i = 0; i < 8; i++){
		aux.first = h.moves[i][0];
		aux.second = h.moves[i][1];
		
		if(b.is_free(h.get_x()+aux.first, h.get_y()+aux.second)){
			ret.push_back(aux);
		}
	}

	return ret;			
}

int counter = 0;
void knights_tour(Board b, Horse h, int n){
	if(b.over() == true){
		b.print();
		counter+=1;
	} else {
		vector<pair<int, int>> temp = find_movements(b, h);
		for(auto i : temp){
			h.move(i);
			b.update(h, n);

			knights_tour(b, h, n+1);

			b.update(h, 0);
			h.un_move(i);
		}
	}
}


int main(int argc, char *argv[]){
	Board b;
	b.create(5);

	Horse h(0, 0);
	b.update(h, 1);

	b.print();
	knights_tour(b, h, 2);

	cout << counter << endl;	

	return EXIT_SUCCESS;
}