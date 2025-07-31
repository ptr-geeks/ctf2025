#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>

char *password = "ptr{if_you_can_read_this_you_are_cracked}";

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	bool correct = true;

	char pwd[100];
	printf("Flag: ");
	scanf("%99s", pwd);
	
	printf("Checking password ");
	for (int i = 0; i < strlen(password); i++) {
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
