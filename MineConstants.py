#constants class for minesweeper game

import Tkinter as Tk
from PIL import Image, ImageTk
import numpy as np

class MineConstants(object):
    def __init__(self):
        #button and tile sizes
        self.tile_size = 20
        self.cell_size = self.tile_size + 2
        self.cell_center = self.cell_size / 2 + 3
        self.border_size = 6
        self.button_size = self.cell_size + self.border_size - 2
        
        #borders
        self.borderwidth = 2
        
        #images
        #for empty tiles
        self.BLANK_IMAGE = Tk.PhotoImage(width=self.tile_size, 
            height=self.tile_size)
        #for flags
        flag_resized = Image.open('flag.gif').resize(
            (self.tile_size, self.tile_size) )
        self.FLAG_IMAGE = ImageTk.PhotoImage(flag_resized)
        #for mines
        mine_resized = Image.open('mine.gif').resize(
            (self.button_size, self.button_size) )
        self.MINE_IMAGE = ImageTk.PhotoImage(mine_resized)
        
        #colours and strings
        #initial [''] handles 0 being a blank space
        self.numbers = [''] + [str(i) for i in range(1,9)]
        #first value is None for easy indexing
        self.colours = [None, 'blue', 'dark green', 'red', 'indigo', 'brown', 
                            'cyan', 'purple', 'orange']