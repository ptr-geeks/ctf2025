#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/random.h>
#include <stdbool.h>

enum { WALL = '#', PATH = ' ' };
char steps[1024];

void maze_step(char** maze, int N, int x, int y)
{
    // Directions: up, down, left, right
    int dx[] = { 0, 0, -2, 2 };
    int dy[] = { -2, 2, 0, 0 };
    int dirs[] = { 0, 1, 2, 3 };

    // Shuffle directions to ensure random traversal
    for (int i = 0; i < 4; i++) {
        int j = rand() % 4;
        int tmp = dirs[i];
        dirs[i] = dirs[j];
        dirs[j] = tmp;
    }

    for (int i = 0; i < 4; i++) {
        int dir = dirs[i];
        int nx = x + dx[dir];
        int ny = y + dy[dir];

        // Check bounds
        if (nx > 0 && nx < N - 1 && ny > 0 && ny < N - 1 && maze[nx][ny] == WALL) {
            // Carve path through wall
            maze[x + dx[dir] / 2][y + dy[dir] / 2] = PATH;
            maze[nx][ny] = PATH;
            maze_step(maze, N, nx, ny);
        }
    }
}

char** gen(unsigned int seed, int N)
{
	srand(seed);

	char** maze = malloc(N * sizeof(char*));
	for (int i = 0; i < N; i++) {
		maze[i] = malloc(N * sizeof(char));
		memset(maze[i], WALL, N * sizeof(char));
	}

	int x = 1, y = 1;
	maze[x][y] = PATH;
	maze_step(maze, N, x, y);

	return maze;
};

void print(char** maze, int N, int px, int py)
{
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			if (i == 1 && j == 1)
				putchar('S');
			else if (i == N - 2 && j == N - 2)
				putchar('E');
			else if (i == px && j == py)
				putchar('P');
			else
				putchar(maze[i][j]);
		}
		putchar('\n');
	}
}

bool walk(char** maze, int N, char *steps)
{
	int x = 1, y = 1;

	for (int step = 0;; step++) {
    //printf("Step %d: %c\n", step, steps[step]);
		//print(maze, N, x, y);

		if (steps[step] == 'U') x--;
		else if (steps[step] == 'D') x++;
		else if (steps[step] == 'L') y--;
		else if (steps[step] == 'R') y++;
		else return false;

		if (maze[x][y] == WALL) return false;
		if (x == N - 2 && y == N - 2) return true;
	}

	return false;
}

int main(int argc, char** argv)
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	for (int i = 0; i < 5; i++) {
    int N = 11 + i*10;

		unsigned int seed = 0;
		getrandom(&seed, sizeof(seed), 0);
		printf("%u\n", seed);

		char** maze = gen(seed, N);
		//print(maze, N, -1, -1);

		fgets(steps, sizeof(steps), stdin);
    if (!walk(maze, N, steps))
			return 1;

		for (int i = 0; i < N; i++)
			free(maze[i]);
		free(maze);
	}

	FILE* f = fopen("flag.txt", "r");
	if (f == NULL) {
		perror("Failed to open flag.txt");
		return 1;
	}

	char flag[256];
	if (fgets(flag, sizeof(flag), f) == NULL) {
		perror("Failed to read flag");
		fclose(f);
		return 1;
	}
	printf("%s\n", flag);

	fclose(f);
	return 0;
}
