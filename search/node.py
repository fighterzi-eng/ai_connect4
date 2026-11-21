from abc import ABC, abstractmethod





class State(ABC):

    @abstractmethod
    def get_children(self):
        pass
    @abstractmethod
    def is_final(self):
        pass

    @abstractmethod
    def eval(self):
        pass

    @abstractmethod
    def get_move(self):
        pass








class Node:

    def __init__(self,state:State):
        self.state=state
        self.type=None
        self.value=None
        self.alpha=None
        self.beta=None
        

    def get_children(self):
        children=[]
        for i in self.state.get_children():
            children.append(Node(i))
        return children

    def is_final(self):
        return self.state.is_final()
    def eval(self):
        return self.state.eval()

    def __hash__(self):
        return hash(self.state)

    def __eq__(self,other):
        return (self.state==other.state)