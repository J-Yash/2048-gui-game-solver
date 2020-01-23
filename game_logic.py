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
        #global current_player

        done = False
        for i in range(len(self.__game)):
            for j in range(len(self.__game)-1):
                if mat[i][j] == mat[i][j+1] and mat[i][j] != ' ':
                    mat[i][j] = mat[i][j] * 2
                    mat[i][j+1] = ' '
                    done = True
                #elif mat[i][j].upper() == mat[i][j+1].upper() and mat[i][j] != ' ':
                #    mat[i][j] = chr(ord(mat[i][j]) + 1)
                #    mat[i][j] = mat[i][j].upper() if self.__current_player > 0 else mat[i][j].lower()
                #    mat[i][j+1] = ' '
                #    done = True
        return (mat, done)

    def __up(self, game):
        # print("up")
        # return matrix after shifting up
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
        # print("down")
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
        # print("left")
        # return matrix after shifting left
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        if done is True:
            self.__game = copy.deepcopy(game)
        return (game, done)

    def __right(self, game):
        # print("right")
        # return matrix after shifting right
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

    def make_move(self, move):
        if move not in ['U', 'L', 'D', 'R']:
            print("Error: Invalid Move!")

        self.__previous_game = self.__game
        if move == 'L':
            self.__left(self.__game)
        if move == 'R':
            self.__right(self.__game)
        if move == 'D':
            self.__down(self.__game)
        if move == 'U':
            self.__up(self.__game)

        self.__add_piece()

        return copy.deepcopy(self)


game1 = initialize_game()

game1.print_game()
game1.make_move("D")
game1.print_game()
game1.make_move("D")
game1.print_game()
game1.make_move("D")
game1.print_game()
game1.make_move("L")
game1.print_game()
game1.make_move("D")
game1.print_game()
game1.make_move("L")
game1.print_game()
game1.make_move("D")
game1.print_game()
