import random

WALL_TOP    = 0b00001
WALL_BOTTOM = 0b00010
WALL_LEFT   = 0b00100
WALL_RIGHT  = 0b01000
WALL        = 0b10000

N = 15
MAZE = ["#"*N for _ in range(N)]

# function mazeStep(r,c){
#     var i,vector=[[0,0],[0,0],[0,0]]; /* 3 possible directions */
#     function R(val){
#         if(typeof val=="undefined")return vector[i][0];
#         vector[i][0]=val;
#     }
#     function C(val){
#         if(typeof val=="undefined")return vector[i][1];
#         vector[i][1]=val;
#     }
#     while(1){
#         i=0; /* create a list of possible options */
#         if(r>1            &&a[r-2][c]!==" "){R(r-2);C(c);i++;}
#         if(r< id.rows*2-1 &&a[r+2][c]!==" "){R(r+2);C(c);i++;}
#         if(c>1            &&a[r][c-2]!==" "){R(r);C(c-2);i++;}
#         if(c< id.cols*2-1 &&a[r][c+2]!==" "){R(r);C(c+2);i++;}
#         /* i is never > 3 because path behind is cleared */
#         if(i==0)break; /* check for dead end */
#         i=Math.floor((Math.random()*i))|0; /* random direction */
#         a[R()][C()]=" "; /* knock out block */
#         a[(R()+r)/2|0][(C()+c)/2|0]=" "; /* clear to it */
#         mazeStep(R(),C());
#     }
# }

def mazeStep(r, c):
    vector = [[0, 0], [0, 0], [0, 0]]  # 3 possible directions

    def R(val=None):
        if val is None:
            return vector[i][0]
        vector[i][0] = val

    def C(val=None):
        if val is None:
            return vector[i][1]
        vector[i][1] = val

    while True:
        i = 0  # create a list of possible options
        if r > 1 and MAZE[r - 2][c] != " ":
            R(r - 2)
            C(c)
            i += 1
        if r < N - 2 and MAZE[r + 2][c] != " ":
            R(r + 2)
            C(c)
            i += 1
        if c > 1 and MAZE[r][c - 2] != " ":
            R(r)
            C(c - 2)
            i += 1
        if c < N - 2 and MAZE[r][c + 2] != " ":
            R(r)
            C(c + 2)
            i += 1

        if i == 0:  # check for dead end
            break

        i = int((i * random.random()))  # random direction
        MAZE[R()][C()] = " "  # knock out block
        MAZE[(R() + r) // 2][(C() + c) // 2] = " "  # clear to it
        mazeStep(R(), C())

# Run
mazeStep(1, 1)

# Print the maze
for row in MAZE:
    print(row)
