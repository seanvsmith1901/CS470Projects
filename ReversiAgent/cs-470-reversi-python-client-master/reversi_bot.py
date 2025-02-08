import math

import numpy as np
import random as rand
import reversi

class ReversiBot:
    def __init__(self, move_num):
        self.move_num = move_num

    def make_move(self, state):
        '''
        This is the only function that needs to be implemented for the lab!
        The bot should take a game state and return a move.

        The parameter "state" is of type ReversiGameState and has two useful
        member variables. The first is "board", which is an 8x8 numpy array
        of 0s, 1s, and 2s. If a spot has a 0 that means it is unoccupied. If
        there is a 1 that means the spot has one of player 1's stones. If
        there is a 2 on the spot that means that spot has one of player 2's
        stones. The other useful member variable is "turn", which is 1 if it's
        player 1's turn and 2 if it's player 2's turn.

        ReversiGameState objects have a nice method called get_valid_moves.
        When you invoke it on a ReversiGameState object a list of valid
        moves for that state is returned in the form of a list of tuples.

        Move should be a tuple (row, col) of the move you want the bot to make.
        '''

        if self.move_num == 1:
            maximizing_player = True
        else:
            maximizing_player = False
        current_depth = 7

        current_best_move = None
        best_value, best_move = self.minmax(state, state.board, current_depth, maximizing_player, current_best_move, -math.inf, math.inf)
        return best_move


    def minmax(self, state, board, depth, maximizingPlayer, current_best_move, alpha, beta):
        valid_moves = state.get_valid_moves()
        if depth == 0 or len(valid_moves) == 0:
            return self.heuristic_eval(board, maximizingPlayer, current_best_move)

        if maximizingPlayer:

            best_val = -math.inf
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                new_board[move[0]][move[1]] = 1
                state.board = new_board # that could do it.
                new_value, best_move = self.minmax(state, new_board, depth - 1, False, best_move, alpha, beta)
                if new_value > best_val:
                    best_move = move
                    best_val = new_value
                alpha = max(alpha, best_val)
                if alpha >= best_val:
                    break
            return best_val, best_move

        else:
            best_val = math.inf
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                new_board[move[0]][move[1]] = 1
                state.board = new_board  # that could do it.
                new_value, best_move = self.minmax(state, new_board, depth - 1, True, best_move, alpha, beta)
                if new_value < best_val:
                    best_val = new_value
                    best_move = move
                beta = min(beta, best_val)
                if beta <= alpha:
                    break
            return best_val, best_move




    def heuristic_eval(self, board, maximizingPlayer, current_best_move):
        SQUARE_VALUES = [
            [120, -20, 20, 5, 5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20, 5, 5, 20, -20, 120],
        ]
        player_1_score = 0
        player_2_score = 0

        for i in range(8):
            for j in range(8):
                if board[i][j] == 1:
                    player_1_score += SQUARE_VALUES[i][j]
                if board[i][j] == 2:
                    player_2_score += SQUARE_VALUES[i][j]

        if maximizingPlayer:
            return player_1_score, current_best_move
        else:
            return player_2_score, current_best_move
