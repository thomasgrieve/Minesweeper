import Tkinter as Tk
from PIL import Image, ImageTk

from MineFramework import MineFramework
from MineConstants import MineConstants

class GridButton(Tk.Button):
    #master is a MineGrid object
    def __init__(self, master, row, col):
        #coordinates
        self.row = row
        self.col = col
        
        #underlying button
        Tk.Button.__init__(self, master, 
            image=master._constants.BLANK_IMAGE, 
            borderwidth=4, command=self.explore)
            
        #flagged status
        self.flagged = False
        
        #right click will flag a square
        self.bind('<Button-3>', self.toggle_flag)   
        
    def explore(self):
        #for ease of reading
        frame = self.master._framework
        buttons = self.master.buttons
        
        #dig up mine
        if frame.mines[self.row][self.col]:
            self.master.game_over('You lost.')
        #0-cell
        elif frame.grid[self.row][self.col] == 0:
            frame.explored_count += frame.BFS(self.row, self.col, 
                buttons=buttons)
        #explore other non-mine cell    
        else: 
            frame.explored[self.row][self.col] = True
            frame.explored_count += 1
            
        if frame.game_won():
            self.master.game_over('You won!')
            
        self.destroy()
        
    def toggle_flag(self, event):
        if self.flagged:
            self['image'] = self.master._constants.BLANK_IMAGE
        else:
            self['image'] = self.master._constants.FLAG_IMAGE
        self.flagged = not self.flagged
            
#end class

class GameOverMessage(Tk.Toplevel):
    def __init__(self, message, master=None):
        self.sizes = [(9,9), (16,16), (16,30)]
        Tk.Toplevel.__init__(self, master)
        self.title(message)
        self.root = master.master
        self.display_options()
        
    def display_options(self):
        msg = Tk.Message(self, text='Play again?')
        msg.pack()
        
        button1 = Tk.Button(self, text='   9x9   ', 
                                  command=lambda: self.restart_game(9,9))
        button1.pack()
        button2 = Tk.Button(self, text='  16x16 ', 
                                  command=lambda: self.restart_game(16,16))
        button2.pack()
        button3 = Tk.Button(self, text='  16x30 ', 
                                  command=lambda: self.restart_game(16,30))
        button3.pack()
        button4 = Tk.Button(self, text='  Quit  ', command=self.root.quit)
        button4.pack()
        
        '''
        self.buttons = [Tk.Button(self, text=str(size), 
                                    command=lambda: self.restart_game(size[0], size[1])) 
                                        for size in self.sizes]
                                        
        self.buttons.append(Tk.Button(self, text='Quit', command=self.root.quit))
                                    
        for button in self.buttons:
            button.pack()
        '''
    
    def restart_game(self, n_rows, n_cols):
        self.master.__init__(framework=MineFramework(n_rows, n_cols), master=self.root)
        self.destroy()
    
    
class MineGrid(Tk.Frame):

    #framework is a MineFramework object
    #_constants is a MineConstants object
    def __init__(self, framework=None, constants=None, master=None):
        Tk.Frame.__init__(self, master)
        
        if framework is None:
            self._framework = MineFramework(16,16)
        else:
            self._framework = framework
        if constants is None:
            self._constants = MineConstants()
        else:
            self._constants = constants
        
        #grid size
        self.n_rows = self._framework.n_rows
        self.n_cols = self._framework.n_cols
        
        #GUI-specific initialization
        self.__create_map(self._framework.grid)
        
        self.pack()
        
    def __create_map(self, grid):
        self.map = [ [self.__create_tile(grid[i][j], i, j) 
                        for j in range(self.n_cols)] 
                            for i in range(self.n_rows)]
        self.buttons = [ [self.__create_button(i, j)
                            for j in range(self.n_cols)] 
                                for i in range(self.n_rows)]
            
    def __create_tile(self, grid_val, row, col):
        #for ease of reading
        size = self._constants.cell_size
        center = self._constants.cell_center
        number = self._constants.numbers[grid_val]
        colour = self._constants.colours[grid_val]
        
        canvas = Tk.Canvas(self, height=size, width=size)
        if not self._framework.mines[row][col]:
            #create text box
            #first two parameters are the position
            canvas_id = canvas.create_text(center, center+1, 
                fill=colour, font=('fixedsys', 18))
            #place text box on canvas
            canvas.itemconfig(canvas_id, text=number)
        else:
            canvas_id = canvas.create_image(center, center+1, 
                image=self._constants.MINE_IMAGE)
            canvas.itemconfig(canvas_id)
        #set borderwidth to 2, background to light grey
        canvas.config(bd=self._constants.borderwidth, bg='light grey')
        #place in grid
        canvas.grid(row=row, column=col)
        
        return canvas
       
    def __create_button(self, row, col):
        button = GridButton(self, row, col)
        button.grid(row=row,column=col)
        return button
        
    def game_over(self, message):
        if not self._framework.game_won():
            self.reveal_mines()
            
        popup = GameOverMessage(message, master=self)
        
    def reveal_mines(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self._framework.mines[i][j]:
                    self.buttons[i][j].destroy()
                #consider disabling buttons at this point
       
def play():
    root = Tk.Tk()
    root.title('MineSweeper')

    game = MineGrid(master=root)

    root.mainloop()