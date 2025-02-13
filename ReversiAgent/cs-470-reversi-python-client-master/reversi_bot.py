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
        current_depth = 6

        current_best_move = None
        best_value, best_move = self.minmax(state, state.board, current_depth, maximizing_player, current_best_move, -math.inf, math.inf)
        return best_move


    def minmax(self, state, board, depth, maximizingPlayer, current_best_move, alpha, beta):
        valid_moves = state.get_valid_moves()
        if depth == 0 or len(valid_moves) == 0:
            return self.heuristic_eval(board, current_best_move, state)


        if maximizingPlayer:

            best_val = -math.inf
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                new_board = self.play_move(new_board, move, player=1)
                state.board = new_board # that could do it.
                new_value, _ = self.minmax(state, new_board, depth - 1, False, best_move, alpha, beta)
                if new_value > best_val:
                    best_move = move
                    best_val = new_value

                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break

            return best_val, best_move

        else:
            best_val = math.inf
            best_move = None
            for move in valid_moves:
                new_board = board.copy()
                new_board = self.play_move(new_board, move, player=2)
                state.board = new_board  # that could do it.
                new_value, _ = self.minmax(state, new_board, depth - 1, True, best_move, alpha, beta)

                if new_value < best_val:
                    best_val = new_value
                    best_move = move

                beta = min(beta, best_val)

                if beta <= alpha:
                    break

            return best_val, best_move


    def play_move(self, board, move, player):
        row, col = move
        opponent = 2 if player == 1 else 1
        # we should check to see if its a valid move, but I am going to assume that only valid moves get passed in.
        board[row][col] = player

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            self.flip_peices(board, row, col, dr, dc, player, opponent)
        return board

    def flip_peices(self, board, row, col, dr, dc, player, opponent):
        r,c = row + dr, col + dc
        pieces_to_clip = []

        while 0 <= r < 8 and  0 <= c < 8 and board[r][c] == opponent:
            pieces_to_clip.append((r, c))
            r,c = r + dr, c + dc

        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for r_flip, c_flip in pieces_to_clip:
                board[r_flip][c_flip] = player


    def heuristic_eval(self, board, current_best_move, state):
        SQUARE_VALUES = [
            [100, -10, 11, 6, 6, 11, -10, 100],
            [-10, -20, 1, 2, 2, 1, -20, -10],
            [10, 1, 5, 4, 4, 5, 1, 10],
            [6, 2, 4, 2, 2, 4, 2, 6],
            [6, 2, 4, 2, 2, 4, 2, 6],
            [10, 1, 5, 4, 4, 5, 1, 10],
            [-10, -20, 1, 2, 2, 1, -20, -10],
            [100, -10, 11, 6, 6, 11, -10, 100],
        ]
        player_1_score = 0
        player_2_score = 0




        for i in range(8):
            for j in range(8):
                if board[i][j] == 1:
                    player_1_score += SQUARE_VALUES[i][j]
                if board[i][j] == 2:
                    player_2_score += SQUARE_VALUES[i][j]

        new_score = player_1_score - player_2_score

        if len(state.get_valid_moves()) > 0: # this makes us think faster if nothing else
            new_score = new_score / len(state.get_valid_moves())


        return new_score, current_best_move # keeps me focusd on gamestate, not individual move
