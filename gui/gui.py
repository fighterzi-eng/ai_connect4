import os
import tkinter as tk
from tkinter import ttk

COLORS = {"_": "white", "p": "red", "c": "gold"}
SHAPE = {"max": "▲", "min": "▼", "final": "■", None: "●"}   

class GUI:

    def __init__(self, cell=70):
        self.cell = cell
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
        self.var = tk.IntVar()      
        self.canvas = None
        self.treeview = None
        self.stats = None


    def get_parameters(self):
        """Show a form, block until Start is pressed, return [width, length, cutoff]."""
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)
        entries = {}
        for i, (name, default) in enumerate([("width", 7), ("length", 6), ("cutoff", 5)]):
            tk.Label(frame, text=name).grid(row=i, column=0)
            e = tk.Entry(frame, width=5)
            e.insert(0, default)
            e.grid(row=i, column=1)
            entries[name] = e
        tk.Button(frame, text="Start", command=lambda: self.var.set(1)).grid(row=3, columnspan=2)

        self.root.wait_variable(self.var)
        params = [int(entries[n].get()) for n in ("width", "length", "cutoff")]
        frame.destroy()
        return params

   
    def display_board(self, board):
        width, length = len(board), len(board[0])
        buttons = tk.Frame(self.root)
        buttons.pack()
        for col in range(width):
            tk.Button(buttons, text=str(col), width=self.cell // 10,
                      command=lambda c=col: self.var.set(c)).grid(row=0, column=col)

        self.canvas = tk.Canvas(self.root, width=width * self.cell,
                                height=length * self.cell, bg="blue")
        self.canvas.pack()

        self.stats = tk.Label(self.root, text="", font=("Arial", 11))
        self.stats.pack(pady=4)

        self.treeview = ttk.Treeview(self.root, show="tree", height=15)
        self.treeview.column("#0", width=width * self.cell)
        self.treeview.pack(fill="both", expand=True)

        self.update_display(board)


    def update_display(self, board):
        self.canvas.delete("all")
        pad = 5
        for col in range(len(board)):
            for row in range(len(board[0])):
                x, y = col * self.cell, row * self.cell
                self.canvas.create_oval(x + pad, y + pad, x + self.cell - pad,
                                        y + self.cell - pad,
                                        fill=COLORS[board[col][row]])
        self.root.update()


    def get_move(self):
        """Block until one of the column buttons is pressed, return its column."""
        self.var.set(-1)
        self.root.wait_variable(self.var)
        return self.var.get()

 
    def display_stats(self, seconds, tree):
        expanded = len(tree)                                  
        generated = sum(len(c) for c in tree.values()) + 1    
        self.stats.config(text=f"Time: {seconds:.3f}s    "
                               f"Expanded nodes: {expanded}    "
                               f"Generated nodes: {generated}")
        self.root.update()

    def display_tree(self, tree, max_depth=3):
        self.treeview.delete(*self.treeview.get_children())
        root_node = next(iter(tree))      
        self._add(tree, root_node, "", 0, max_depth)
        self.root.update()

    def _add(self, tree, node, parent, depth, max_depth):
        text = (f"{SHAPE[node.type]} depth={depth} move={node.state.get_move()}  "
                f"v={node.value}")
        if node.alpha is not None:
            text += f"  α={node.alpha}  β={node.beta}"
        item = self.treeview.insert(parent, "end", text=text, open=(depth == 0))
        if depth < max_depth:
            for child in tree.get(node, []):
                self._add(tree, child, item, depth + 1, max_depth)


    def display_result(self, player_score, computer_score):
        if player_score > computer_score:
            winner = "Player wins!"
        elif computer_score > player_score:
            winner = "Computer wins!"
        else:
            winner = "It's a draw!"
        text = f"{winner}\nPlayer: {player_score}   Computer: {computer_score}"
        tk.Label(self.root, text=text, font=("Arial", 16, "bold")).pack(pady=10)
        self.root.mainloop()   