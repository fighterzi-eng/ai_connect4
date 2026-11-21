from search.node import Node


class  Minimax():


    def __init__(self,cutoff:int,initial_node:Node):
        self.cutoff=cutoff
        self.node=initial_node
        self.tree={}
        self.tree[self.node]=[]



    def min(self,node:Node,current_depth,alpha,beta)->Node:
        if node.is_final():
            node.value=node.eval()
            node.type="final"
            return node
        elif current_depth>=self.cutoff:
            node.value=node.eval()
            return node
        v=float('inf')
        node.type="min"

        self.tree[node]=[]
        for child in node.get_children():
            self.tree[node].append(child)
            currentv=self.max(child,current_depth+1,alpha,beta).value
            if v> currentv:
                v=currentv
                returned_node=child
                beta=min(beta,v)
            if beta<=alpha:
                node.alpha=alpha
                node.beta=beta
                node.value=v
                return returned_node
        node.alpha=alpha
        node.beta=beta
        node.value=v
        return returned_node



    def max(self,node:Node,current_depth,alpha,beta) -> Node:
        if node.is_final():
            node.value=node.eval()
            node.type="final"
            return node
        elif current_depth>=self.cutoff:
            node.value=node.eval()
            return node
        v=float('-inf')
        node.type="max"

        self.tree[node]=[]
        for child in node.get_children():
            self.tree[node].append(child)
            currentv=self.min(child,current_depth+1,alpha,beta).value
            if v< currentv:
                v=currentv
                returned_node=child
                alpha=max(alpha,v)
            if alpha>=beta:
                node.alpha=alpha
                node.beta=beta
                node.value=v
                return returned_node
        node.alpha=alpha
        node.beta=beta
        node.value=v
        return returned_node


    def search(self):
        choosen_node =self.max(self.node,0,float('-inf'),float('inf'))
        return choosen_node.state.get_move()

    def update_node(self,node):
        self.node=node
        self.tree = {node: []}






