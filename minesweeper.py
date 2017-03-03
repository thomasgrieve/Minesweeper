import sys

from MineFramework import MineFramework
from MineGrid import play

def get_grid_size():
    #handle command line arguments
    if len(sys.argv) < 3:
        print 'Usage: ' + sys.argv[0] + ' <number of rows> <number of columns>'
        sys.exit(-1)
	
    try:
        n_rows = int(sys.argv[1])
        n_cols = int(sys.argv[2])
    except (ValueError):
        print 'Usage: ' + sys.argv[0] + ' <number of rows> <number of columns>'
        sys.exit(-1)
    return (n_rows, n_cols)

def play_cmd_line(size_tuple):
    continue_playing = True
    grid = MineFramework(size_tuple[0], size_tuple[1], prob_mine=0.2)
    
    while(continue_playing):
        game_winnable = True
        explored_count = 0

        grid.print_grid()

        while game_winnable and explored_count < grid.count_non_mines():
            move = raw_input('What\'s your next move?\n')
            try:
                move = move.rsplit()
                command = move[0]
                #account for 0-indexing
                row = int(move[1]) - 1
                col = int(move[2]) - 1
            except(ValueError, IndexError):
                print type(move)
                print 'Usage: <explore / flag> <row> <col>'
                continue
		
            explored_update = grid.update_grid(command, row, col)
            #dug up a mine, game lost
            if explored_update == -1:
                game_winnable = False
            #game continues
            else:
                explored_count += explored_update
                grid.print_grid()

        grid.print_final_grid()
        if game_winnable:
            print 'You win!'
        else:
            print 'You lost.'
		
        continue_playing = raw_input('Play again?')[0].upper() == 'Y'
        #separate games
        if continue_playing:
            print '\n'
#end command line version

#to play command line version
#play_cmd_line(get_grid_size())

play()
	
	
	
			
