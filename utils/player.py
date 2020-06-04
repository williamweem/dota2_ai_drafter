import random
from utils.node import Node
import logging
import numpy
import pickle

logging.basicConfig(filename='State.log', level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

class MCTSPlayer:

    def __init__(self, draft, maxiters, c):
        self.draft = draft
        self.maxiters = maxiters
        self.c = c

    def get_move(self):
        """
        decide the next move
        """
        root = Node(player=self.draft.player, untried_actions=self.draft.get_moves(), c=self.c)

        for i in range(self.maxiters):
            node = root
            tmp_draft = self.draft.copy()
            logging.info('State setelah copy: {}'.format(tmp_draft.move_cnt))
            logging.info('State setelah copy: {}'.format(tmp_draft.state))

            # selection - select best child if parent fully expanded and not terminal
            while len(node.untried_actions) == 0 and node.children != []:
                node = node.select()
                tmp_draft.move(node.action)
                logging.info('State selection: {}'.format(tmp_draft.state))
                logging.info('State selection: {}'.format(tmp_draft.move_cnt))

            # expansion - expand parent to a random untried action
            if len(node.untried_actions) != 0:
                a = random.sample(node.untried_actions, 1)[0]
                tmp_draft.move(a)
                logging.info('State expansion: {}'.format(tmp_draft.state))
                logging.info('State expansion: {}'.format(tmp_draft.move_cnt))
                p = tmp_draft.player
                node = node.expand(a, p, tmp_draft.get_moves())

            # simulation - rollout to terminal state from current
            while not tmp_draft.end():
                moves = tmp_draft.get_moves()
                a = random.sample(moves, 1)[0]
                tmp_draft.move(a)
                logging.info('State: {}'.format(tmp_draft.state))
                logging.info('State: {}'.format(tmp_draft.move_cnt))

            # backpropagation - propagate result of rollout game up the tree
            while node != None:
                if node.player == 0:
                    result = tmp_draft.eval()
                else:
                    result = 1 - tmp_draft.eval()
                node.update(result)
                node = node.parent

        return root.select_final()
