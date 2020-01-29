#!/usr/local/bin/python3

"""
Author: Yashvardhan Jain, January 2020
"""
import copy
from queue import PriorityQueue
import random
import math

# Using minimax algorithm with alpha beta pruning

def is_terminal_state(current_game):
    return current_game.is_goal()

def is_depth_limit(curr_depth, depth_limit):
    return curr_depth == depth_limit

def evaluation_utility_value(curr_game, player_switch):
    board1 = curr_game.get_game()
    board = [[None for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            if board1[i][j] == ' ':
                board[i][j] = 0
            else:
                board[i][j] = int(board1[i][j])
    
    # Calculating utility for neighbor tiles that can be merged.
    util1 = 0

    for i in range(4):
        for j in range(3):
            if board[i][j] != 0 and board[i][j+1] != 0:
                util1 -= abs(board[i][j] - board[i][j+1])
    
    for j in range(4):
        for i in range(3):
            if board[i][j] != 0 and board[i+1][j] != 0:
                util1 -= abs(board[i][j] - board[i+1][j])


    # calculating utility for largest values tiles being on the corners

    util2 = 10
    for i in range(4):
        if (all(board[i][j] <= board[i][j+1] for j in range(3)) or all(board[i][j] >= board[i][j+1] for j in range(3))):
            util2 *= 3
        else:
            util2 = int(util2/2) + 1
    for j in range(4):
        if (all(board[i][j] <= board[i+1][j] for i in range(3)) or all(board[i][j] >= board[i+1][j] for i in range(3))):
            util2 *= 3
        else:
            util2 = int(util2/2) + 1

    util3 = 0
    for i in range(len(board[0])):
        for j in range(len(board[0])):
            if board[i][j] == ' ':
                util3 += 1
    util3 = util3**3
        
    utility = 3*util3 + 4*util2 + 2*util1 + 5*curr_game.get_score()

    return utility

def minimax_with_ab_pruning(current_game, depth, alpha, beta, player_switch, game_move, depth_limit):
    
    if is_terminal_state(current_game) or is_depth_limit(depth, depth_limit):
        return evaluation_utility_value(current_game, player_switch), game_move

    possible_moves = ["'W'", "'A'", "'S'", "'D'"]

    best_move = game_move
    
    if player_switch == 0:
        best_val = -math.inf
        for move in possible_moves:
            next_game = current_game.make_move(move)
            val, ret_move = minimax_with_ab_pruning(next_game, depth+1, alpha, beta, 1, move, depth_limit)
            
            if val > best_val:
                best_val = val
                best_move = move
                alpha = max(best_val, alpha)
            
            if alpha >= beta:
                break
        

    elif player_switch == 1:
        best_val = math.inf
        for move in possible_moves:
            next_game = current_game.make_move(move)
            val, ret_move = minimax_with_ab_pruning(next_game, depth+1, alpha, beta, 0, move, depth_limit)
            if val < best_val:
                best_val = val
                best_move = move
                beta = min(best_val, beta)
            
            if beta <= alpha:
                break

    return best_val, best_move


def ai_next_move(game):
    depth = 0
    alpha = -math.inf
    beta = math.inf
    initial_move = None
    depth_limit = 8

    original_game = copy.deepcopy(game)

    val, move = minimax_with_ab_pruning(original_game, depth, alpha, beta, 0, initial_move, depth_limit)
    print(val, move)

    return move
