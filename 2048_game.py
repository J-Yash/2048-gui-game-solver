#!/usr/local/bin/python3

"""
Author: Yashvardhan Jain, January 2020
"""

import game_logic
import ai_solver
import copy

def human_next_move():
    print('Please enter move:')
    move = input().strip().upper()
    while(move not in "UDLR"):
        print('Bad move! Please try again.')
        move = input().strip().upper()

    return move

def run_game():
    game = game_logic.initialize_game(4)
    game.print_game()

    while True:
        move = human_next_move()
        game = game.make_move(move)
        game.print_game()
    



if __name__ == "__main__":
    run_game()
    
