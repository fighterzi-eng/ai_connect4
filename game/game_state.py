from search.node import State
from typing import override
import copy



class Game_state(State):

    def __init__(self,turn,board,width,lenght,move):
        self.turn=turn  #0 for player , 1 for computer
        self.board=board # each cell is either filled with "_" for blank or "c" for computer or "p " for the player 
        self.width=width
        self.length =lenght
        #the code for the last move played to reach this state indicated by the number of the choosen column
        self.move =move


    @override
    def get_children(self):
        children=[]
        piece= "p" if self.turn==0 else "c"
        for i in range(self.width):
            child_table=copy.deepcopy(self.board)

            prev_cell=None
            for j in range(self.length):

                current_cell=child_table[i][j]

                if current_cell!="_":
                    break
           
                else :
                    prev_cell=j

            if prev_cell is None:
                continue
            child_table[i][prev_cell]=piece
            child=Game_state(self.turn^1,child_table,self.width,self.length,i)
            children.append(child)
        return children

    @override
    def is_final(self):
        for i in range(self.width):
            if self.board[i][0] == "_":
                return False
        return True

    @override
    def get_move(self):
        return self.move

    def play_move(self,move):
        piece= "p" if self.turn==0 else "c"
        prev_cell=None
        child_table=copy.deepcopy(self.board)
        for j in range(self.length):

            current_cell=child_table[move][j]

            if current_cell!="_":
                break
           
            else :
                prev_cell=j

        if prev_cell is None:
            return None
        child_table[move][prev_cell]=piece
        child=Game_state(self.turn^1,child_table,self.width,self.length,i)
        
        return child

    def __eq__(self,other):

        return self.board==other.board

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    @override
    def eval(self):
        pass

    





    