import numpy as np
from utils.player import MCTSPlayer
import tensorflow as tf

MAX_ITERS = 200
C = 0.5
ENV_PATH = 'models/model.h5'

class Draft:
    """
    class handling state of the draft
    """

    def __init__(self, env_path=ENV_PATH, state=[[],[]], avail_moves=set([]), player=0):
        self.model = tf.keras.models.load_model(env_path)
        self.state = state
        self.avail_moves = avail_moves
        self.move_cnt = [len(state[0]), len(state[1])]
        self.player = player  # current player's turn
        self.next_player = int(not bool(player)) # next player turn

    def get_player(self):
        return MCTSPlayer(draft=self, maxiters=MAX_ITERS, c=C)

    def eval(self):
        assert self.end()
        x = np.zeros((1, 130))
        x[0, self.state[0]] = 1
        x[0, self.state[1]] = -1
        x = np.delete(x,[0, 24, 115, 116, 117, 118, 122, 123, 124, 125, 127],axis=1)
        radiant_win_rate = self.model.predict(x)[0, 0]
        return radiant_win_rate

    def copy(self):
        """
        make copy of the board
        """
        copy = Draft()
        copy.model = self.model
        copy.state = [self.state[0][:], self.state[1][:]]
        copy.avail_moves = set(self.avail_moves)
        copy.move_cnt = self.move_cnt[:]
        copy.player = self.player
        copy.next_player = self.next_player
        return copy

    def move(self, move):
        """
        take move of form [x,y] and play
        the move for the current player
        """
        self.player = self.next_player
        self.next_player = int(not bool(self.player))
        self.state[self.player].append(move)
        self.avail_moves.remove(move)
        self.move_cnt[self.player] += 1

    def get_moves(self):
        """
        return remaining possible draft moves
        (i.e., where there are no 1's or -1's)
        """
        if self.end():
            return set([])
        return set(self.avail_moves)

    def end(self):
        """
        return True if all players finish drafting
        """
        if self.move_cnt[0] == 5 and self.move_cnt[1] == 5:
            return True
        return False
