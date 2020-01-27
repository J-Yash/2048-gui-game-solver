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
    #game = game_logic.initialize_game(4)
    #game.print_game()

    #while True:
        #move = human_next_move()

    #    if game.is_game_full():

    #        move = ai_solver.ai_next_move(game)
    #        game = game.make_move(move)
    #        game.print_game()
    #        time.sleep(1)
            
    #    else:
    #        game.print_game()
            #raise Exception("You Lose! The game is full.")
    #        return False
    
    #ai_solver.ai_next_move(game)
    new_game = GameGrid()


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048 AI solver : Hit ENTER to start')
        self.master.bind("<Return>", self.start_ai_solver)

        # self.gamelogic = gamelogic
        self.commands = ("'U'", "'D'", "'L'", "'R'")
        
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

    #def gen(self):
    #    return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = game_logic.initialize_game(4)
        #self.history_matrixs = list()
        #self.matrix = logic.add_two(self.matrix)
        #self.matrix = logic.add_two(self.matrix)
        

    def update_grid_cells(self):
        board = self.matrix.get_game()
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = board[i][j]
                #print("Game board:", board)
                if new_number == ' ':
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def start_ai_solver(self, event):
        flag = True
        while flag:
            flag = self.key_down()

    def key_down(self):
        #key = repr(event.char).upper()

        key = ai_solver.ai_next_move(self.matrix)
        #print(key)
        #if key == c.KEY_BACK and len(self.history_matrixs) > 1:
        #    self.matrix = self.history_matrixs.pop()
        #    self.update_grid_cells()
        #    print('back on step total step:', len(self.history_matrixs))
        if key in self.commands:
            if self.matrix.is_game_full():
                self.matrix = self.matrix.make_move(key) #self.commands[repr(event.char)](self.matrix)
                #if done:
                #self.matrix = logic.add_two(self.matrix)
                # record last move
                #self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                #done = False
                if self.matrix.is_goal() is True:
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                #time.sleep(0.2)
                return True
                #if self.matrix.is_goal() is True:
                #    self.grid_cells[1][1].configure(
                #        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                #    self.grid_cells[1][2].configure(
                #        text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            else:
                self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                self.grid_cells[1][2].configure(
                        text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                return False
        else:
            print('Bad move! Please try again.')
            return True

    #def generate_next(self):
    #    index = (self.gen(), self.gen())
    #    while self.matrix[index[0]][index[1]] != 0:
    #        index = (self.gen(), self.gen())
    #    self.matrix[index[0]][index[1]] = 2    



if __name__ == "__main__":
    game_end = run_game()

    #if game_end is False:
    #    print("You lose! The game is full.")
    
