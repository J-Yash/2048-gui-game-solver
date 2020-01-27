#!/usr/local/bin/python3

"""
Author: Yashvardhan Jain, January 2020
"""
import copy
from queue import PriorityQueue
import random

def successors(game):
    possible_moves = []
    for move in ["'U'", "'L'", "'D'", "'R'"]:
        game_copy = copy.deepcopy(game)
        new_game = game_copy.make_move(move)
        possible_moves.append((new_game, move))
    return possible_moves


def Calculate_heuristic(succ):
    game_cost = cost(succ)
    h = game_cost
    return h


def cost(succ):
    return succ.state_cost()


def is_goal(game):
    return game.is_goal()

def search_move(game):
    original_game = copy.deepcopy(game)

    fringe = []
    
    fringe.append((original_game, ""))
    visited = []
    #all_moves = ""

    count = 0

    while len(fringe) != 0:
        
        (state, moves) = fringe.pop()
        #state.print_game()

        for (succ, move) in successors(state):

            if is_goal(succ) or count == 10:
                return moves[0]

            if succ not in visited:
                # heuristic_value = Calculate_heuristic(succ)
                fringe.append((succ, moves + move))
                visited.append(succ)
                count = count + 1

            #fringe.insert(0, (succ, route_so_far + move ) )
    return False


# Using minimax algorithm with alpha beta pruning

def is_terminal_state(current_game):
    #print("*****************Goal reached")
    return current_game.is_goal()

def is_depth_limit(curr_depth, depth_limit):
    #print("&&&&&&&&&&Depth limit reached")
    return curr_depth == depth_limit

def evaluation_utility_value(curr_game, player_switch):
    #utility = random.randint(0,100)
    board1 = curr_game.get_game()
    #print(board1)
    board = [[None for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            if board1[i][j] == ' ':
                board[i][j] = 0
            else:
                board[i][j] = int(board1[i][j])
    # Calculating utility for neighbor tiles that can be merged.
    util1 = 0
    
    for i in range(len(board[0])):
        for j in range(len(board[0])):
            if (i-1) >= 0:
                util1 += abs(board[i][j] - board[i-1][j])
            if (j-1) >= 0:
                util1 += abs(board[i][j] - board[i][j-1])
            if (i+1) < 4:
                util1 += abs(board[i][j] - board[i+1][j])
            if (j+1) < 4:
                util1 += abs(board[i][j] - board[i][j+1])

    # calculating utility for largest values tiles being on the corners

    util2 = 0
    for i in range(len(board[0])-1):
        #for j in range(len(board[0])-1):
        j = 0
        if board[i][j] <= board[i][j+1]:
            util2 += 10
            if board[i][j+1] <= board[i][j+2]:
                util2 += 15
                if board[i][j+2] <= board[i][j+3]:
                    util2 += 20
                else:
                    util2 -= 20
            else:
                util2 -= 15
                if board[i][j+2] <= board[i][j+3]:
                    util2 += 20
                else:
                    util2 -= 20
        elif board[i][j] >= board[i][j+1]:
            util2 += 10
            if board[i][j+1] >= board[i][j+2]:
                util2 += 15
                if board[i][j+2] >= board[i][j+3]:
                    util2 += 20
                else:
                    util2 -= 20
            else:
                util2 -= 15
                if board[i][j+2] >= board[i][j+3]:
                    util2 += 20
                else:
                    util2 -= 20
        #else: 
        #    j += 1

        for j in range(len(board[0])-1):
        #for j in range(len(board[0])-1):
            i = 0
            if board[i][j] <= board[i+1][j]:
                util2 += 10
                if board[i+1][j] <= board[i+2][j]:
                    util2 += 15
                    if board[i+2][j] <= board[i+3][j]:
                        util2 += 20
                    else:
                        util2 -= 20
                else:
                    util2 -= 15
                    if board[i+2][j] <= board[i+3][j]:
                        util2 += 20
                    else:
                        util2 -= 20
            elif board[i][j] >= board[i+1][j]:
                util2 += 10
                if board[i+1][j] >= board[i+2][j]:
                    util2 += 15
                    if board[i+2][j] >= board[i+3][j]:
                        util2 += 20
                    else:
                        util2 -= 20
                else:
                    util2 -= 15
                    if board[i+2][j] >= board[i+3][j]:
                        util2 += 20
                    else:
                        util2 -= 20

        util3 = 0
        for i in range(len(board[0])):
            for j in range(len(board[0])):
                if board[i][j] == ' ':
                    util3 += 1
        util3 *= 100

            
        utility = util3 + util2 - util1

    return utility

def minimax_with_ab_pruning(current_game, depth, alpha, beta, player_switch, game_move, depth_limit):
    
    if is_terminal_state(current_game) or is_depth_limit(depth, depth_limit):
        return evaluation_utility_value(current_game, player_switch), game_move


    possible_moves = ["'U'", "'L'", "'D'", "'R'"]

    best_move = game_move
    
    if player_switch == 0:
        best_val = -10000
        for move in possible_moves:
            next_game = current_game.make_move(move)
            val, ret_move = minimax_with_ab_pruning(next_game, depth+1, alpha, beta, 1, move, depth_limit)
            
            if val > best_val:
                best_val = val
                best_move = move
                alpha = max(best_val, alpha)
            
            if beta <= alpha:
                break
        

    elif player_switch == 1:
        best_val = 10000
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
    #move = search_move(game)

    # for minimax

    #board = game.get_game()
    #player = game.getCurrentPlayer()
    #deterministic = game.getDeterministic()
    depth = 0
    alpha = -10000
    beta = 10000
    initial_move = None
    depth_limit = 7

    #print(board)
    #print(game.state())
    
    original_game = copy.deepcopy(game)

    val, move = minimax_with_ab_pruning(original_game, depth, alpha, beta, 0, initial_move, depth_limit)
    print(val, move)


    return move
