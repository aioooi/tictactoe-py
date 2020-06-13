

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
    self._board[1,1] = 1
    self._board[0,1] = -1
    self._board[1,2] = 1

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

    s = "   \u2554" + "\u2550\u2550\u2550\u2564" * 2 + "\u2550" * 3 + "\u2557\n"
    t = "   \u2551" + " {} \u2502" * 2 + " {} \u2551\n"
    q = "   \u255f" + "\u2500\u2500\u2500\u253c" * 2 + "\u2500" * 3 + "\u2562\n"
    v = "   \u255a" + "\u2550\u2550\u2550\u2567" * 2 + "\u2550" * 3 + "\u255d\n"

    
    ui = numpad
    ui = ["\u262f" if _ == -1 else n for n, _ in zip(ui, self._board.flatten())]
    ui = ["\u0fbe" if _ == 1 else n for n, _ in zip(ui, self._board.flatten())]

    return (s + (t + q) * 2 + t + v).format(*ui)


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
      empty = np.where(self._board == self._EMPTY)
      i = np.random.randint(0, len(empty[0]))
      self._board[empty[0][i], empty[1][i]]
      
      return



    # Human has two in a row?
    rows = np.dot(self._board, np.ones(_SHAPE))
    cols = np.dot(np.ones(_SHAPE), self._board)
    
    
