from search.node import State
from typing import override


class Game_state(State):

    # kernels in board order: X = the side's piece, _ = empty cell
    FOURS = ("XXXX",)
    THREES = ("_XXX", "X_XX", "XX_X", "XXX_")
    TWOS = ("XX__", "X_X_", "X__X", "_XX_", "_X_X", "__XX")

    def __init__(self, turn, board, width, lenght, move=None):
        self.turn = turn    # 0 for player, 1 for computer
        self.board = board  # board[col][row]: "_" blank, "c" computer, "p" player (row 0 = top)
        self.width = width
        self.length = lenght
        self.move = move    # column of the last move played to reach this state
        self.stride = lenght + 1           # one extra sentinel bit per column
        self.nbits = width * self.stride   # length of the 1D signal

        # sampling step for each direction: vertical, horizontal, diagonal /, diagonal \
        self.steps = (1, self.stride, self.stride + 1, self.stride - 1)

        # bitboards built from the list board
        p = c = full = 0
        for col in range(width):
            for row in range(lenght):
                bit = 1 << (col * self.stride + (lenght - 1 - row))
                full |= bit
                cell = board[col][row]
                if cell == "p":
                    p |= bit
                elif cell == "c":
                    c |= bit
        self.player_bits = p
        self.computer_bits = c
        self.empty_bits = full & ~(p | c)   # sentinel bits stay 0

    def _convolve(self, kernel, a, s):
       
        #  zero padded so every window has 4 samples
        pad = [0] * (3 * s)
        sig_a = [(a >> j) & 1 for j in range(self.nbits)] + pad
        sig_e = [(self.empty_bits >> j) & 1 for j in range(self.nbits)] + pad

        count = 0
        for i in range(self.nbits):                 # slide the kernel
            win_a = sig_a[i : i + 4 * s : s]        # sample every s
            win_e = sig_e[i : i + 4 * s : s]
            if all(win_a[k] if ch == "X" else win_e[k]
                   for k, ch in enumerate(kernel)):
                count += 1
        return count

    def _count(self, kernels, a):
        sum=0
        for k in kernels:
            for step in self.steps:
                sum+=self._convolve(k, a, step)
       
        return sum

   
    @override
    def get_children(self):
        children = []
        # centre columns first  better alpha-beta pruning bec center moves have more possiblities therefor higher chance of winning
        order = sorted(range(self.width), key=lambda c: abs(c - (self.width - 1) / 2))
        for col in order:
            child = self.play_move(col)
            if child is not None:
                children.append(child)
        return children

    @override
    def is_final(self):
        # the game ends only when the board is full
        return self.empty_bits == 0

    @override
    def get_move(self):
        return self.move

    def play_move(self, col):
        """Child state after the side to move plays col, or None if the column is full."""
        row = None
        for j in range(self.length):
            if self.board[col][j] != "_":
                break
            row = j
        if row is None:
            return None
        piece = "p" if self.turn == 0 else "c"
        child_table = [column[:] for column in self.board]   
        child_table[col][row] = piece
        return Game_state(self.turn ^ 1, child_table, self.width, self.length, col)

    @override
    def eval(self):
        c, p = self.computer_bits, self.player_bits

        # completed fours dominate; the final score is just the difference
        score = 100 * (self._count(self.FOURS, c) - self._count(self.FOURS, p))
        if self.is_final():
            return score

        score += 5 * (self._count(self.THREES, c) - self._count(self.THREES, p))
        score += 2 * (self._count(self.TWOS, c) - self._count(self.TWOS, p))
        return score

    def __eq__(self, other):
        return self.board == other.board and self.turn == other.turn

    def __hash__(self):
        return hash((self.player_bits, self.computer_bits, self.turn))
    def final_score(self):
        c, p = self.computer_bits, self.player_bits

        # completed fours dominate; the final score is just the difference
        pscore = 100 * ( self._count(self.FOURS, p))
        cscore=100*(self._count(self.FOURS, c) )
        return pscore,cscore
