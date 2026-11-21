# usr/bin/python3
from time import perf_counter
from game.game import Game
from gui.gui import GUI

gui = GUI()
WIDTH, LENGHT, CUTOFF = gui.get_parameters()

system = Game(WIDTH, LENGHT, CUTOFF)
gui.display_board(system.get_board())

while not system.is_end():
    if system.get_turn() == "p":
        move = gui.get_move()
        while not system.playerturn(move):          
            move = gui.get_move()
        gui.update_display(system.get_board())
    else:
        start = perf_counter()
        tree = system.computerturn()
        time=perf_counter() - start
        gui.update_display(system.get_board())
        gui.display_stats(time, tree)
        gui.display_tree(tree,CUTOFF)

playerscore, computerscore = system.get_scores()
gui.display_result(playerscore, computerscore)