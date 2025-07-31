#include <iostream>
#include <ostream>
#include <cstring>

class Pokemon {
	public:
		char name[40];

		int level;
		int xp;

		int life;
		int attack;
		int defense;
		int speed;

		virtual ~Pokemon() = default;

		void print() {
			std::cout << "Pokemon: " << name << " (Level: " << level << ", XP: " << xp << ")" << std::endl;
			std::cout << "Stats - Life:    " << life << std::endl 
				        << "        Attack:  " << attack << std::endl
					      << "        Defense: " << defense << std::endl
								<< "        Speed:   " << speed << std::endl;
		}

		void rename_random(const char* namefile) {
			FILE* file = fopen(namefile, "r");
			if (file) {
				char line[40];
				int lineCount = 0;
				while (fgets(line, sizeof(line), file)) {
					lineCount++;
				}
				rewind(file);
				int randomLine = rand() % lineCount;
				for (int i = 0; i <= randomLine; i++) {
					fgets(line, sizeof(line), file);
				}
				line[strcspn(line, "\n")] = 0;
				strcpy(name, line);
				fclose(file);
			} else {
				std::cerr << "Error opening name file." << std::endl;
			}
		}

		virtual void rename(char* newName) {
			newName[39] = '\0';
			strcpy(name, newName);
		}
		virtual void cry() = 0;
		virtual void evolve() = 0;
};

class Charmander : public Pokemon {
	public:
		Charmander() {
			strcpy(name, "Charmander");
			level = 5;
			xp = 0;
			life = 39;
			attack = 52;
			defense = 43;
			speed = 65;
		}

		void cry() override {
			std::cout << "Charmander cries: Char! Char!" << std::endl;
		}

		void evolve() override {
			std::cout << "Charmander evolves into Charmeleon!" << std::endl;
			strcpy(name, "Charmeleon");
			life += 10;
			attack += 15;
			defense += 10;
			speed += 5;
		}
};

class Squirtle : public Pokemon {
	public:
		Squirtle() {
			strcpy(name, "Squirtle");
			level = 5;
			xp = 0;
			life = 44;
			attack = 48;
			defense = 65;
			speed = 43;
		}

		void cry() override {
			std::cout << "Squirtle cries: Squirt! Squirt!" << std::endl;
		}

		void evolve() override {
			std::cout << "Squirtle evolves into Wartortle!" << std::endl;
			strcpy(name, "Wartortle");
			life += 10;
			attack += 15;
			defense += 10;
			speed += 5;
		}
};

class Bulbasaur : public Pokemon {
	public:
		Bulbasaur() {
			strcpy(name, "Bulbasaur");
			level = 5;
			xp = 0;
			life = 45;
			attack = 49;
			defense = 49;
			speed = 45;
		}

		void cry() override {
			std::cout << "Bulbasaur cries: Bulba! Bulba!" << std::endl;
		}

		void evolve() override {
			std::cout << "Bulbasaur evolves into Ivysaur!" << std::endl;
			strcpy(name, "Ivysaur");
			life += 10;
			attack += 15;
			defense += 10;
			speed += 5;
		}
};

class PokedexEntry {
	public:
		long pad = 0;
		long pad2 = 0;
		Pokemon* pokemon;
		PokedexEntry* next;

		PokedexEntry(Pokemon* p) : pokemon(p), next(nullptr) {}
		~PokedexEntry() {
			delete pokemon;
		}
	
		void print() {
			if (pokemon) {
				pokemon->print();
			} else {
				std::cout << "Empty entry." << std::endl;
			}
		}

		std::string getName() {
			return pokemon ? pokemon->name : "Empty";
		}
};

class Pokedex {
	private:
		Pokemon *pokedex[6];

	public:
		Pokedex() {
			for (int i = 0; i < 6; ++i) {
				pokedex[i] = nullptr;
			}
		}

		~Pokedex() {
			for (int i = 0; i < 6; ++i) {
				if (pokedex[i]) {
					delete pokedex[i];
				}
			}
		}

		void listEntries() {
			for (int i = 0; i < 6; ++i) {
				if (pokedex[i]) {
					std::cout << i << ": " << pokedex[i]->name << std::endl;
				} else {
					std::cout << i << ": Empty" << std::endl;
				}
			}
		}

		void addPokemon(Pokemon* pokemon) {
			for (int i = 0; i < 6; ++i) {
				if (pokedex[i] == nullptr) {
					pokedex[i] = pokemon;
					std::cout << "Pokemon added at index " << i << std::endl;
					return;
				}
			}

			std::cout << "Pokedex is full. Cannot add more Pokemon." << std::endl;
		}

		void removePokemon(int index) {
			if (index < 0 || index >= 6) {
				std::cout << "Invalid index. Please enter a number between 0 and 5." << std::endl;
				return;
			}

			delete pokedex[index];
			pokedex[index] = nullptr;
			std::cout << "Pokemon removed from index " << index << std::endl;
		}

		Pokemon* getPokemon(int index) {
			return pokedex[index];
		}
};

void pokemon_loop(Pokemon* pokemon) {
	std::cout << "1. Print pokemon name" << std::endl
						<< "2. Rename pokemon" << std::endl
						<< "3. Select random name" << std::endl
						<< "4. Print pokemon stats" << std::endl
						<< "5. Make pokemon cry" << std::endl
						<< "6. Evolve pokemon" << std::endl
						<< "> ";
	int choice;
	std::cin >> choice;

	switch (choice) {
		case 1:
			std::cout << "Pokemon name: " << pokemon->name << std::endl;
			break;
		case 2: {
			std::cout << "Enter new name: ";
			std::string newName;
			std::cin >> newName;
			pokemon->rename((char*)newName.c_str());
			break;
		}
		case 3: {
			pokemon->rename_random("names.txt");
			std::cout << "Pokemon renamed to: " << pokemon->name << std::endl;
			break;
		}
		case 4:
			pokemon->print();
			break;
		case 5:
			pokemon->cry();
			break;
		case 6:
			pokemon->evolve();
			break;
		default:
			std::cout << "Invalid choice." << std::endl;
	}
}

bool pokedex_loop(Pokedex* pokedex) {
	std::cout << "1. List Pokedex entries" << std::endl
						<< "2. Add Pokemon" << std::endl
						<< "3. Remove Pokemon" << std::endl
						<< "4. Retrieve Pokemon" << std::endl
						<< "5. Exit" << std::endl
						<< "> ";
	int choice;
	std::cin >> choice;
	if (choice == 5) {
		return false;
	}

	switch (choice) {
		case 1: {
			pokedex->listEntries();
			break;
		}
		case 2: {
			std::cout << "Choose a Pokemon to add (1. Charmander, 2. Squirtle, 3. Bulbasaur): ";
			int pokemonChoice;
			std::cin >> pokemonChoice;

			Pokemon* newPokemon = nullptr;
			if (pokemonChoice == 1) {
				newPokemon = new Charmander();
			} else if (pokemonChoice == 2) {
				newPokemon = new Squirtle();
			} else if (pokemonChoice == 3) {
				newPokemon = new Bulbasaur();
			} else {
				std::cout << "Invalid choice." << std::endl;
				break;
			}

			pokedex->addPokemon(newPokemon);
			break;
		}
		case 3: {
			std::cout << "Enter index of Pokemon to remove: ";
			int index;
			std::cin >> index;
			pokedex->removePokemon(index);
			break;
		}
		case 4: {
			std::cout << "Enter index of Pokemon to retrieve: ";
			int index;
			std::cin >> index;
			Pokemon* pokemon = pokedex->getPokemon(index);
			if (pokemon) {
				pokemon_loop(pokemon);
			} else {
				std::cout << "No Pokemon found at index " << index << std::endl;
			}
			break;
		}
		default:
			std::cout << "Invalid choice." << std::endl;
	}

	return true;
}

int main() {
  Pokedex *pokedex = new Pokedex();
	while(pokedex_loop(pokedex)) {}
	delete pokedex;
	return 0;
}


