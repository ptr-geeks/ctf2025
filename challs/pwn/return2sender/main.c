#include <stdio.h>
#include <string.h>

void win() {
	char flag[100];
	FILE *f = fopen("flag.txt", "r");
	if (f == NULL) {
		perror("Failed to open flag.txt");
		return;
	}

	if (fgets(flag, sizeof(flag), f) != NULL) {
		printf("%s\n", flag);
	}

	fclose(f);
}

void vuln() {
	char fullname[64];
	char buffer[64];

	printf("Enter your name: ");
	fgets(buffer, sizeof(buffer), stdin);
	buffer[strcspn(buffer, "\n")] = 0;

	strcpy(fullname, buffer);
	strcat(fullname, " ");

	printf("Enter your surname: ");
	fgets(buffer, sizeof(buffer), stdin);
	buffer[strcspn(buffer, "\n")] = 0;

	strcat(fullname, buffer);
	printf("Hello %s, nice to meet you!\n", fullname);
}

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	vuln();
	return 0;
}
