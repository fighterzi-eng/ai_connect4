from game.game import Game
from time import perf_counter

#place holders until gui input for start
LENGHT=6
WIDTH=7
CUTOFF=5


def printboard(board):
    for i in range(LENGHT):
        for j in range(WIDTH):
            print(board[j][i]+"  ",end="")
        print("\n")



system=Game(WIDTH,LENGHT,CUTOFF)

while not system.is_end():
    printboard(system.get_board())
    if system.get_turn() =="p":
        #place holder for gui input
        move=int(input("enter your move from 0 to width -1"))
        while system.playerturn(move) is None:
            move=int(input("invalid move try again enter your move from 0 to width -1"))
        #function to update the gui
    else:
        start=perf_counter()
        tree= system.computerturn()
        end=perf_counter()
        time=end-start
        print(f"time taken: {time} ")
        # update the gui with move
        #functions to display the tree and time and nodes expanded listing node type in its shape upuerr triangle or lower triangle  its v ,alpa,beta
playerscore,computerscore=system.get_scores()

print(f"player score: {playerscore}   computerscore: {computerscore}")


      
