from pwn import *
import ctypes

libc = ctypes.CDLL("libc.so.6")
libc.rand.restype = ctypes.c_int
libc.srand.argtypes = [ctypes.c_uint]

WALL = "#"
PATH = " "

def maze_step(maze, N, x, y):
    dx = [0, 0, -2, 2]
    dy = [-2, 2, 0, 0]
    dirs = [0, 1, 2, 3]

    # Shuffle directions using libc.rand
    for i in range(4):
        j = libc.rand() % 4
        dirs[i], dirs[j] = dirs[j], dirs[i]

    for dir in dirs:
        nx = x + dx[dir]
        ny = y + dy[dir]

        if 0 < nx < N - 1 and 0 < ny < N - 1 and maze[nx][ny] == WALL:
            maze[x + dx[dir] // 2][y + dy[dir] // 2] = PATH
            maze[nx][ny] = PATH
            maze_step(maze, N, nx, ny)

def gen(seed, N):
    libc.srand(seed)

    # Initialize maze with WALLs
    maze = [[WALL for _ in range(N)] for _ in range(N)]

    x, y = 1, 1
    maze[x][y] = PATH
    maze_step(maze, N, x, y)

    return maze

def print_maze(maze):
    for row in maze:
        print(''.join(row))

# Find a path in the maze using DFS and return the path as a string containing U, D, L, R
def find_path(maze, N):
    start = (1, 1)
    end = (N - 2, N - 2)
    path = []

    def dfs(x, y):
        if (x, y) == end:
            return True
        maze[x][y] = WALL
        for dx, dy, direction in [(0, 1, 'R'), (0, -1, 'L'), (1, 0, 'D'), (-1, 0, 'U')]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N and maze[nx][ny] == PATH:
                path.append(direction)
                if dfs(nx, ny):
                    return True
                path.pop()
        maze[x][y] = PATH
        return False

    dfs(start[0], start[1])
    return path

p = remote("localhost", 1337)
for i in range(5):
    N = 11 + i*10
    seed = int(p.recvline().strip().decode())
    libc.srand(seed)

    maze = gen(seed, N)
    print_maze(maze)

    path = find_path(maze, N)
    path = ''.join(path)
    print("Path:", path)

    p.sendline(path.encode())

flag = p.recvline().strip().decode()
print("Flag:", flag)

p.interactive()
