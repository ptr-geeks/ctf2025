#include <stdio.h>
#include <string.h>
#include <sys/random.h>
#include <stdbool.h>

struct User {
	  char name[50];
		long pin;
		char data[100];
		bool isAdmin;
};

struct User users[3];

long random_pin()
{
	long pin;
	if (getrandom(&pin, sizeof(pin), 0) == -1) {
		perror("getrandom");
		return -1;
	}
	return pin % 10000000000000000L;
}

int main()
{
	// Initialize users
	strcpy(users[0].name, "admin");
	users[0].pin = random_pin();
	users[0].isAdmin = true;
	strcpy(users[1].name, "user");
	users[1].pin = random_pin();
	users[1].isAdmin = false;
	strcpy(users[2].name, "guest");
	users[2].pin = 12345678; // Fixed pin for guest
	users[2].isAdmin = false;

  // Login
	char username[50];
	int pin;
	printf("Username: ");
	scanf("%s", username);
	printf("PIN: ");
	scanf("%d", &pin);

	// Find user
	int id = -1;
	for (int i = 0; i < 3; i++) {
		if (strcmp(users[i].name, username) == 0 && users[i].pin == pin) {
			id = i;
			break;
		}
	}
	if (id == -1) {
		printf("Invalid username or PIN.\n");
		return 1;
	}

	// Edit data
	printf("Welcome %s!\n", users[id].name);
	printf("Update data: ");
	scanf("%s", users[id].data);
  printf("Data updated successfully.\n");

	// Print flag
	if (users[id].isAdmin) {
		char flag[100];
		FILE *file = fopen("flag.txt", "r");
		if (file) {
			fgets(flag, sizeof(flag), file);
			fclose(file);
			printf("Flag: %s\n", flag);
		} else {
			printf("Error reading flag.\n");
		}
	}

	// Exit
	printf("Goodbye!\n");
	return 0;
}
