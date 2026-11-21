
from search.node import Node
from search.minmax import Minimax
from game.game_state import Game_state


class Game:

    def __init__(self,width,lenght,cutoff):
        



        board = [["_" for _ in range(lenght)] for _ in range(width)]
        self.state=Game_state(0,board,width,lenght,None)
        self.node=Node(self.state)
        self.computer=Minimax(cutoff,self.node)
        self.width=width
        self.lenght=lenght



    def playerturn(self,move):
        if not 0 <= move < self.width:
            return False
        newstate=self.state.play_move(move)

        if newstate is None:
            print("thats not a vaalid move")
            return False
        else:
            self.state=newstate
            self.computer.update_node(Node(self.state))
            return True

    def is_end(self):
        return self.state.is_final()


    def computerturn(self):
        move=self.computer.search()
        newstate=self.state.play_move(move)
        
        if newstate is None:
            raise TypeError
        self.state=newstate
        return self.computer.tree
        

    def get_scores(self):
        """returns player score and computer scores respectively"""
        return self.state.final_score()
    def get_turn(self):
        return "p" if self.state.turn==0 else "c"

    def get_board(self):
        return self.state.board

    