#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>

char password[] = {
	-50, 69, -56, 76, -38, 67, -29, 101,
	-11, 127, -33, 67, -35, 76, -20, 97,
	-5, 101, -2, 94, -43, 66, -44, 88,
	-8, 126, -18, 100, -60, 90, -41, 77,
	-19, 125, -20, 112, -22, 74, -44, 76,
	-46, 68, -43, 117, -23, 100, -6, 102,
	-14, 104, -13, 113,
};

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	bool correct = true;

	char pwd[100];
	printf("Flag: ");
	scanf("%99s", pwd);
	
	printf("Checking password ");
	char prev = 0x41;
	for (int i = 0; i < 52; i++) {
		pwd[i] = pwd[i] ^ prev;
		pwd[i] = ~pwd[i];
		prev = pwd[i];
		if (pwd[i] != password[i]) {
			correct = false;
			break;
		}
		printf(". ");
		sleep(1);
	}

	if (correct) {
		printf("Correct!\n");
	} else {
		printf("Incorrect!\n");
	}

	return 0;
}
