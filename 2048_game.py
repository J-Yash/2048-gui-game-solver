#!/usr/local/bin/python3

"""
Author: Yashvardhan Jain, January 2020
"""

import game_logic
import ai_solver
import copy
import time
from tkinter import Frame, Label, CENTER
import constants as c

def human_next_move():
    print('Please enter move:')
    move = input().strip().upper()
    while(move not in "UDLRudlr"):
        print('Bad move! Please try again.')
        move = input().strip().upper()
    return move

def run_game():
    new_game = GameGrid()


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title('2048 AI solver : Hit SPACEBAR to start AI. For manual, use WSAD to play.')
        self.master.bind("<Key>", self.game_mode)
        self.commands = ("'W'", "'S'", "'A'", "'D'")
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    
    def init_matrix(self):
        self.matrix = game_logic.initialize_game(4)        

    def update_grid_cells(self):
        board = self.matrix.get_game()
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = board[i][j]
                if new_number == ' ':
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def game_mode(self, event):
        if event.char == ' ':
            self.start_ai_solver(event)
        else:
            self.key_down(event, "human")

    def start_ai_solver(self, event):
        flag = True
        while flag:
            flag = self.key_down(event, "ai")

    def key_down(self, event, token="human"):
        if token == "ai":
            key = ai_solver.ai_next_move(self.matrix)
        elif token == "human":
            key = repr(event.char).upper()
        
        if key in self.commands:
            if self.matrix.is_game_full():
                self.matrix = self.matrix.make_move(key) 
                print("Score: ", self.matrix.get_score())
                self.update_grid_cells()
                if self.matrix.is_goal() is True:
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    return False
                return True
            else:
                self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                self.grid_cells[1][2].configure(
                        text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                return False
        else:
            print('Bad move! Please try again.')
            return True

if __name__ == "__main__":
    game_end = run_game()
