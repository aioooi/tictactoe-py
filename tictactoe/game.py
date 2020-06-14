

import numpy as np

class Game:
    # board values
    _COMPUTER = -1
    _EMPTY = 0
    _HUMAN = 1
  
    # board shape
    _SHAPE = (3, 3)
  
    def __init__(self):
        self._board = np.zeros(self._SHAPE, dtype=int)
  
    def __str__(self):
        number = [
            "\u2070",
            "\u00b9",
            "\u00b2",
            "\u00b3",
            "\u2074",
            "\u2075",
            "\u2076",
            "\u2077",
            "\u2078",
            "\u2079"
        ]
        numpad = number[7:10] + number[4:7] + number[1:4]
    
        s = "\u2554" + ("\u2550" * 3 + "\u2564") * 2 + "\u2550" * 3 + "\u2557\n"
        t = "\u2551" + " {} \u2502" * 2 + " {} \u2551\n"
        q = "\u255f" + ("\u2500" * 3 + "\u253c") * 2 + "\u2500" * 3 + "\u2562\n"
        v = "\u255a" + ("\u2550" * 3 + "\u2567") * 2 + "\u2550" * 3 + "\u255d\n"
        
        ui = numpad
        # computer plays ☯
        ui = ["\u262f" if _ == self._COMPUTER else n 
                for n, _ in zip(ui, self._board.flatten())]
        # human plays ྾ 
        ui = ["\u0fbe" if _ == self._HUMAN else n 
                for n, _ in zip(ui, self._board.flatten())]
    
        return (s + (t + q) * 2 + t + v).format(*ui)


    def play(self, first_move=1):
        if first_move != 1:
            first = self._COMPUTER
        


    """
    Human makes a move
    """
    def enter_move(self, move=(0,0)):
        assert(len(move) == 2)
    
        if any([_ < 0 or _ > 2 for _ in move]):
            raise Exception("invalid move: position does not exist")
        else:
            if self._board[move] != self._EMPTY:
                raise Exception("invalid move: board position not empty")
            else:
                self._board[move] = self._HUMAN


    """
    Computer makes a move
    """
    def make_move(self):
        # TODO checks etc.

        # random move
        # TODO connect with handicap
        if np.any(self._board == _EMPTY):
            # TODO return value?
            return _random_move()
        
        action = [
            _win
            _avoid_defeat,
            _matchball,
            _center,
            _opposite_corner,
            _empty_corner,
            _random_move,
        ]

        while len(action):
            a = action.pop(0)
            if a():
                break

        # TODO return value?
        return


    def _win():
        rows = np.dot(self._board, np.ones(3))
        cols = np.dot(np.ones(3), self._board)
        diag = self._board.trace()
        sdiag = self._board[::-1].trace()

        check = np.where(
            np.concatenate((rows, cols, [diag], [sdiag])) == 2 * self._COMPUTER)

        if len(check[0]):
            i = np.random.randint(len(check[0]))
            c = check[i]
            
            if c in range(3):
                # row
                x = np.where(self._board[c, :] == self._EMPTY)[0][0]
                self._board[c, x] = self._COMPUTER
            elif c in range(3, 6):
                # column
                x = np.where(self._board[:, c - 3] == self._EMPTY)[0][0]
                self._board[x, c - 3] = self._COMPUTER
            elif c == 6:
                # diagonal
                np.fill_diagonal(self._board, self._COMPUTER)
            else:
                # c == 7, secondary diagonal
                np.fill_diagonal(self._board[::-1], self._COMPUTER)
            
            return True
        
        else:
            return False


    def _avoid_defeat():
        rows = np.dot(self._board, np.ones(3))
        cols = np.dot(np.ones(3), self._board)
        diag = self._board.trace()
        sdiag = self._board[::-1].trace()

        check = np.where(
            np.concatenate((rows, cols, [diag], [sdiag])) == 2 * self._HUMAN)

        if len(check[0]):
            i = np.random.randint(len(check[0]))
            c = check[i]
            
            if c in range(3):
                # row
                x = np.where(self._board[c, :] == self._EMPTY)[0][0]
                self._board[c, x] = self._COMPUTER
            elif c in range(3, 6):
                # column
                x = np.where(self._board[:, c - 3] == self._EMPTY)[0][0]
                self._board[x, c - 3] = self._COMPUTER
            elif c == 6:
                # diagonal
                d = np.array(np.diagonal(self._board))
                x = np.where(d == self._EMPTY))[0][0]
                d[x] = self._COMPUTER
                np.fill_diagonal(self._board, d)
            else:
                # c == 7, secondary diagonal
                d = np.array(np.diagonal(self._board[::-1]))
                x = np.where(d == self._EMPTY))[0][0]
                d[x] = self._COMPUTER
                np.fill_diagonal(self._board[::-1], d)
            
            return True
        
        else:
            return False


    def _matchball():
        pass


    def _center():
        if self._board[1,1] == self._EMPTY:
            self._board[1,1] = self._COMPUTER
            return True
        else:
            return False


    def _opposite_corner():
        corner = [(0,0), (0,2), (2,0), (2,2)]

        if self._board[corner[0]] + self._board[corner[3]] == self._HUMAN:
            if self._board[corner[0]] == self._EMPTY:
                self._board[corner[0]] = self._COMPUTER
            else:
                self._board[corner[3]] = self._COMPUTER
            return True
        elif self._board[corner[1]] + self._board[corner[2]] == self._HUMAN:
            if self._board[corner[1]] == self._EMPTY:
                self._board[corner[1]] = self._COMPUTER
            else:
                self._board[corner[2]] = self._COMPUTER
            return True
        else:
            return False


    def _empty_corner():
        corner = [(0,0), (0,2), (2,0), (2,2)]
        empty = np.where(self._board.flatten()[[0,2,6,8]] == self._EMPTY)
        if len(empty[0]):
            self._board[corner[np.random.randint(len(empty))]] = self._COMPUTER
            return True
        else:
            return False


    def _random_move():
        empty = np.where(self._board == self._EMPTY)
        if len(empty[0]):
            i = np.random.randint(len(empty[0]))
            self._board[empty[0][i], empty[1][i]] = self._COMPUTER
            return True
        else:
            return False