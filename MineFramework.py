import random
import collections

class MineFramework(object):

    def __init__(self, n_rows, n_cols, prob_mine=0.2):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self._n_tiles = self.n_rows * self.n_cols
        self._prob_mine = prob_mine
        self.MINE = -1
        self.FLAG = -2
        self.mines = [[self.__is_mine() for j in range(self.n_cols)] 
                                    for i in range(self.n_rows)]
        self._n_mines = sum([row.count(True) for row in self.mines])
        self.grid = [[0 for j in range(self.n_cols)] 
                            for i in range(self.n_rows)]
        self.__init_grid()
        
        self.flagged = [[False for j in range(self.n_cols)] 
                                for i in range(self.n_rows)]
        self.explored = [[False for j in range(self.n_cols)] 
                                for i in range(self.n_rows)]
        self.explored_count = 0

        
    #generates a random number from 0 to 1 and compares to probability if there
    #being a mine in an arbitrary cell. If the randomly generated number is 
    #lower than the probability, we say there is a mine, otherwise not
    def __is_mine(self):
        #gives a random real number in range [0,1)
        #2^16 chosen arbitrarily as upper bound for random number
        rand_value = random.randint(0,65535) / float(65536)
        if rand_value < self._prob_mine:
            return True
        else: 
            return False
            

    #finds all available neighbours along a given axis        
    def __find_neighbour_axis(self, index, max_index):
        if index == 0:
            return [index, index+1]
        elif index == max_index-1:
            return [index-1, index]
        else:
            return [index-1,index,index+1]
            

    #increment count of all neighbours of given vertex        
    def __update_neighbours(self, row, col):
        row_choices = self.__find_neighbour_axis(row, self.n_rows)
        col_choices = self.__find_neighbour_axis(col, self.n_cols)
        for r in row_choices:
            for c in col_choices:
                if self.grid[r][c] != self.MINE:
                    self.grid[r][c] += 1
                
                
    #initialize grid values given a mines 2D array
    def __init_grid(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                #update surrounding cells of a mine
                if self.mines[i][j]:
                    self.grid[i][j] = self.MINE
                    self.__update_neighbours(i, j)
                    
    
    #for command line version of game
    def count_non_mines(self):
        return self._n_tiles - self._n_mines
        
    def game_won(self):
        return self.explored_count == self.count_non_mines()

    #for command line version of game                
    def print_grid(self):
        #print separator before column numbers
        print '   |',
        #print column numbers
        for i in range(self.n_cols):
            print ('{0:2d}').format(i+1),
        print ''
        #print separating line
        separator = '-' * (self.n_cols * 3 + 4)
        print separator
        
        #print grid values
        for i in range(self.n_rows):
            print ('{0:2d} |').format(i+1),
            for j in range(self.n_cols):
                #doesn't allow user to flag explored cells
                if self.flagged[i][j] and not self.explored[i][j]:
                    print ('{0:2s}').format(' F'),
                #print empty box for unexplored cell
                elif not self.explored[i][j]:
                    print ('{0:2s}').format('[]'),
                #print cell number
                else:
                    print ('{0:2d}').format(self.grid[i][j]),
            #end line
            print ''
    
    #debugging tool                
    def print_final_grid(self):
        #print separator before column numbers
        print '   |',
        #print column numbers
        for i in range(self.n_cols):
            print ('{0:2d}').format(i+1),
        print ''
        #print separating line
        separator = '-' * (self.n_cols * 3 + 4)
        print separator
        
        #print grid values
        for i in range(self.n_rows):
            print ('{0:2d} |').format(i+1),
            for j in range(self.n_cols):
                #print wrongly flagged cells
                if self.grid[i][j] != self.MINE and self.flagged[i][j]:
                    print ('{0:2s}').format(' X'),
                #print mines
                elif self.grid[i][j] == self.MINE:
                    print ('{0:2s}').format(' *'),
                #print non-mine cells
                else:
                    print ('{0:2d}').format(self.grid[i][j]),
            #end line
            print ''
            
            
    #generate all neighbours of a given cell as tuples
    def __find_neighbours(self, cell):
        row = cell[0]
        col = cell[1]
        row_choices = self.__find_neighbour_axis(row, self.n_rows)
        col_choices = self.__find_neighbour_axis(col, self.n_cols)
        for r in row_choices:
            for c in col_choices:
                #don't want repeat entries
                if r != row or c != col:
                    yield (r, c)
            
    #breadth-first search for exploring 0 values        
    def BFS(self, start_row, start_col, buttons=None):
        #initial cell must be counted
        count = 1
        queue = collections.deque()
        queue.appendleft((start_row, start_col))
        #explore initial cell
        self.explored[start_row][start_col] = True
        while len(queue) > 0:
            cell = queue.pop()
            row = cell[0]
            col = cell[1]
            #repeat with all unexplored neighbours of cell
            for neighbour in self.__find_neighbours(cell):
                nbr_row = neighbour[0]
                nbr_col = neighbour[1]
                #increase count if not explored
                if not self.explored[nbr_row][nbr_col]:
                    count += 1
                    #mark as explored
                    self.explored[nbr_row][nbr_col] = True
                    
                    #destroy buttons if using GUI game
                    if buttons is not None:
                        buttons[nbr_row][nbr_col].destroy()
                        
                    #enqueue all neighbours with value 0
                    if self.grid[nbr_row][nbr_col] == 0:
                        queue.appendleft(neighbour)
                    
        return count
                    
    
    #update explored and flagged arrays
    #returns update to explored square count, -1 on failure
    def update_grid(self, command, row, col):
        #explore a square
        if command[0].upper() == 'E':
            #dig up a mine
            if self.mines[row][col]:
                return -1
            elif self.grid[row][col] == 0:
                return self.BFS(row, col)
            else: 
                self.explored[row][col] = True
                return 1
        #flag a square        
        elif command[0].upper() == 'F':
            self.flagged[row][col] = True
            return 0
        #unflag a square
        elif command[0].upper() == 'U':
            self.flagged[row][col] = False
            return 0
        else:
            return 0

#end class