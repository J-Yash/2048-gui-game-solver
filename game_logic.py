#!/usr/local/bin/python3

"""
Author: Yashvardhan Jain, January 2020
"""

import copy
import random

'''
Function to initialize the game.
'''


def initialize_game(size=4):
    game = [[' ' for _ in range(size)] for _ in range(size)]
    game[random.randint(0, size-1)][random.randint(0, size-1)] = 2
    return GameLogic(game)


'''
This class implements the game logic.
'''


class GameLogic:
    def __init__(self, game):
        self.__game = game
        self.__new_piece_loc = (0, 0)
        self.__previous_game = self.__game
        self.__score = 0

    def __cmp__(self, other):
        return cmp(self.state_cost(), other.state_cost())

    def get_score(self):
        return self.__score

    def is_goal(self):
        goal = False
        for i in range(len(self.__game[0])):
            for j in range(len(self.__game[0])):
                if self.__game[i][j] == 2048:
                    goal = True
        if goal is True:
            return True
        else:
            return False

    def is_game_full(self):
        board = self.get_game()
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == ' ':
                    return True

        for i in range(len(board)):
            for j in range(len(board)-1):
                if board[i][j] == board[i][j+1]:
                    return True
        
        for i in range(len(board)):
            for j in range(len(board)-1):
                if board[j][i] == board[j+1][i]:
                    return True

        return False
        

    def state_cost(self):
        sum = 0
        curr_game = self.get_game()
        for i in range(4):
            for j in range(4):
                if curr_game[i][j] != ' ':
                    sum = sum + curr_game[i][j]
        return sum

    def print_game(self):
        str_game = [['______' for _ in range(len(self.__game))] for _ in range(len(self.__game))]

        for i in range(len(self.__game)):
            for j in range(len(self.__game)):
                str_game[i][j] = "_"+str(self.__game[i][j])+"_"

        for i in range(len(self.__game)):
            print("|".join(str_game[i]))
        print("\n")

    def get_game(self):
        return copy.deepcopy(self.__game)

    def __reverse(self, mat):
        new = []
        for i in range(len(mat)):
            new.append([])
            for j in range(len(mat[0])):
                new[i].append(mat[i][len(mat[0])-j-1])
        return new

    def __transpose(self, mat):
        new = []
        for i in range(len(mat[0])):
            new.append([])
            for j in range(len(mat)):
                new[i].append(mat[j][i])
        return new

    def __cover_up(self, mat):
        new = [[' ' for _ in range(len(self.__game))]for _ in range(len(self.__game))]

        done = False
        for i in range(len(self.__game)):
            count = 0
            for j in range(len(self.__game)):
                if mat[i][j] != ' ':
                    new[i][count] = mat[i][j]
                    if j != count:
                        done = True
                    count += 1
        return (new, done)

    def __merge(self, mat):

        done = False
        for i in range(len(self.__game)):
            for j in range(len(self.__game)-1):
                if mat[i][j] == mat[i][j+1] and mat[i][j] != ' ':
                    mat[i][j] = mat[i][j] * 2
                    mat[i][j+1] = ' '
                    done = True
                    self.__score = self.__score + mat[i][j]
        return (mat, done)

    def __up(self, game):
        game = self.__transpose(game)
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        game = self.__transpose(game)
        if done is True:
            self.__game = copy.deepcopy(game)
        return (game, done)

    def __down(self, game):
        game = self.__reverse(self.__transpose(game))
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        game = self.__transpose(self.__reverse(game))
        if done is True:
            self.__game = copy.deepcopy(game)
        return (game, done)

    def __left(self, game):
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        if done is True:
            self.__game = copy.deepcopy(game)
        return (game, done)

    def __right(self, game):
        game = self.__reverse(game)
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        game = self.__reverse(game)
        if done is True:
            self.__game = copy.deepcopy(game)
        return (game, done)

    def __add_piece(self):
        open = []
        for i in range(len(self.__game)):
            for j in range(len(self.__game)):
                if self.__game[i][j] == ' ':
                    open += [(i, j), ]

        if len(open) > 0:
            r = random.choice(open)
            self.__game[r[0]][r[1]] = 2
            self.__new_piece_loc = r

    def get_empty_cells(self):
        open = []
        for i in range(len(self.__game)):
            for j in range(len(self.__game)):
                if self.__game[i][j] == ' ':
                    open += [(i, j), ]
        
        return open
    
    def add_piece_deterministic(self, pos):
        self.__game[pos[0]][pos[1]] = 2
        self.__new_piece_loc = pos


    def make_move(self, move):
        if move not in ["'W'", "'A'", "'S'", "'D'"]:
            print("Error: Invalid Move!")

        self.__previous_game = self.__game
        if move == "'A'":
            self.__left(self.__game)
        if move == "'D'":
            self.__right(self.__game)
        if move == "'S'":
            self.__down(self.__game)
        if move == "'W'":
            self.__up(self.__game)

        self.__add_piece()

        return copy.deepcopy(self)
