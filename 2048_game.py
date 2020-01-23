#!/usr/local/bin/python3

"""
Author: Yashvardhan Jain, January 2020
"""

import game_logic
import ai_solver

if __name__ == "__main__":
    game1 = game_logic.initialize_game()

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
