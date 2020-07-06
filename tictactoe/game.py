#!/usr/bin/python3
# -*- coding: utf-8 -*-

import click
import numpy as np


class Game:
    # board values
    _COMPUTER = -1
    _EMPTY = 0
    _HUMAN = 1

    # board shape
    _SHAPE = (3, 3)

    # handicap
    _MAX_HANDICAP = 100

    def __init__(self, handicap=0):
        self._board = np.zeros(self._SHAPE, dtype=int)

        if 0 <= int(handicap) <= self._MAX_HANDICAP:
            self._handicap = int(handicap)
        else:
            self._handicap = int(0.5 * self._MAX_HANDICAP)

    def __str__(self):
        """Print current board."""
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

        s = "\u2554" + ("\u2550" * 3 + "\u2564") * \
            2 + "\u2550" * 3 + "\u2557\n"
        t = "\u2551" + " {} \u2502" * 2 + " {} \u2551\n"
        q = "\u255f" + ("\u2500" * 3 + "\u253c") * \
            2 + "\u2500" * 3 + "\u2562\n"
        v = "\u255a" + ("\u2550" * 3 + "\u2567") * \
            2 + "\u2550" * 3 + "\u255d\n"

        ui = numpad
        # computer plays ☯
        ui = ["\u262f" if _ == self._COMPUTER else n
              for n, _ in zip(ui, self._board.flatten())]
        # human plays ྾
        ui = ["\u0fbe" if _ == self._HUMAN else n
              for n, _ in zip(ui, self._board.flatten())]

        return (s + (t + q) * 2 + t + v).format(*ui)

    # def input_next_field

    def play(self, computer_moves_first=False):
        """Play the game.

        Returns 
            self._COMPUTER: computer wins
            self._HUMAN: human wins
            0:  draw
        """
        if computer_moves_first:
            turn = self._COMPUTER
        else:
            turn = self._HUMAN

        if not computer_moves_first:
            print(self, '\n')

        while np.any(self._board == self._EMPTY):
            if turn == self._COMPUTER:
                print('My move:')
                self._computer_move()
                turn = self._HUMAN
            else:
                numpad = [7, 8, 9, 4, 5, 6, 1, 2, 3]
                empty_field_labels = [str(numpad.index(e + 1) + 1) 
                    for e in np.where(self._board.flatten() == self._EMPTY)[0]]

                f = numpad.index(
                    int(click.prompt("It's your turn! Choose a field",
                                     type=click.Choice(empty_field_labels))))

                self._human_move((int(f / 3), f % 3))
                turn = self._COMPUTER

            print(self, '\n')

            check = [
                bool(len(self._check_triplet(3 * self._COMPUTER))),
                bool(len(self._check_triplet(3 * self._HUMAN))),
                not np.any(self._board == self._EMPTY)
            ]

            if check[0]:
                return self._COMPUTER
            if check[1]:
                return self._HUMAN
            if check[2] and not (check[0] or check[1]):
                return 0

    def _human_move(self, move=(0, 0)):
        """Human makes a move."""
        assert(len(move) == 2)

        if any([_ < 0 or _ > 2 for _ in move]):
            raise Exception('invalid move: position does not exist')
        else:
            if self._board[move] != self._EMPTY:
                raise Exception('invalid move: board position not empty')
            else:
                self._board[move] = self._HUMAN

    def _computer_move(self):
        """Computer makes a move."""
        h = np.random.randint(self._MAX_HANDICAP)
        if h < self._handicap:
            return self._random_move()

        action = [
            self._win,
            self._avoid_defeat,
            self._matchball,
            self._center,
            self._opposite_corner,
            self._empty_corner,
            self._random_move,
        ]

        while len(action):
            if action.pop(0)():
                break

    def _check_triplet(self, value):
        """Check whether triplet with l1 norm equal to value exists."""
        rows = np.dot(self._board, np.ones(3))
        cols = np.dot(np.ones(3), self._board)
        diag = self._board.trace()
        sdiag = self._board[:: -1].trace()

        return np.where(
            np.concatenate((rows, cols, [diag], [sdiag])) == value)[0]

    def _win(self):
        """Check for row to complete."""
        check = self._check_triplet(2 * self._COMPUTER)

        if len(check):
            i = np.random.randint(len(check))
            c = check[i]

            if 0 <= c < 3:
                # row
                x = np.where(self._board[c, :] == self._EMPTY)[0][0]
                self._board[c, x] = self._COMPUTER
            elif 3 <= c < 6:
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

    def _avoid_defeat(self):
        """Check for (and destroy) opponent's matchballs."""
        check = self._check_triplet(2 * self._HUMAN)

        if len(check):
            i = np.random.randint(len(check))
            c = check[i]

            if 0 <= c < 3:
                # row
                x = np.where(self._board[c, :] == self._EMPTY)[0][0]
                self._board[c, x] = self._COMPUTER
            elif 3 <= c < 6:
                # column
                x = np.where(self._board[:, c - 3] == self._EMPTY)[0][0]
                self._board[x, c - 3] = self._COMPUTER
            elif c == 6:
                # diagonal
                d = np.array(np.diagonal(self._board))
                x = np.where(d == self._EMPTY)[0][0]
                d[x] = self._COMPUTER
                np.fill_diagonal(self._board, d)
            else:
                # c == 7, secondary diagonal
                d = np.array(np.diagonal(self._board[::-1]))
                x = np.where(d == self._EMPTY)[0][0]
                d[x] = self._COMPUTER
                np.fill_diagonal(self._board[::-1], d)

            return True

        else:
            return False

    def _matchball(self):
        """Create two in a row such that remaining square is empty."""
        rows = np.where(np.dot(self._board, np.ones(3)) == self._COMPUTER)[0]
        np.random.shuffle(rows)
        for i in rows:
            empty = np.where(self._board[i, :] == self._EMPTY)[0]
            if len(empty):
                j = empty[np.random.randint(len(empty))]
                self._board[i, j] = self._COMPUTER
                return True

        cols = np.where(np.dot(np.ones(3), self._board) == self._COMPUTER)[0]
        np.random.shuffle(cols)
        for j in cols:
            empty = np.where(self._board[:, j] == self._EMPTY)[0]
            if len(empty):
                i = empty[np.random.randint(len(empty))]
                self._board[i, j] = self._COMPUTER
                return True

        return False

    def _center(self):
        """Play center court."""
        if self._board[1, 1] == self._EMPTY:
            self._board[1, 1] = self._COMPUTER
            return True
        else:
            return False

    def _opposite_corner(self):
        """Occupy (an) opposite corner."""
        corner = [(0, 0), (0, 2), (2, 0), (2, 2)]

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

    def _empty_corner(self):
        """Play an empty corner."""
        corner = [(0, 0), (0, 2), (2, 0), (2, 2)]
        empty = np.where(self._board.flatten()[[0, 2, 6, 8]] == self._EMPTY)[0]
        if len(empty):
            i = np.random.randint(len(empty))
            self._board[corner[empty[i]]] = self._COMPUTER
            return True
        else:
            return False

    def _random_move(self):
        """Play an empty sqaure."""
        empty = np.where(self._board == self._EMPTY)
        if len(empty[0]):
            i = np.random.randint(len(empty[0]))
            self._board[empty[0][i], empty[1][i]] = self._COMPUTER
            return True
        else:
            return False
