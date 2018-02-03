from basicsearch_lib.board import Board
import math
import copy
import random

solve_state = (1,2,3,4,5,6,7,8,None)

class TileBoard(Board):

    def __init__(self, n, force_state=None):
        #Since were calling a 3x3 grid and 8-puzzle
        #In order to get rows and columns, we need to take the sqrt of n+1
        self.side_length = int(math.sqrt(n+1))
        #Our grid is a square so we can just use one var - side_length - for most functions
        Board.__init__(self, self.side_length, self.side_length, self.side_length)

        self.force_state = force_state
        #If there is a force_state, set the grid to it
        if (force_state != None):
            self.set_state(force_state)

    #Iterates through the force_state tuple, assigning those values to the board
    def set_state(self, state):
        for row in range(0, self.side_length):
            for col in range(0, self.side_length):
                self.place(row, col, self.force_state[row*self.side_length+col])

    #Creates a tuple of the current board state by iterating through the board
    #and adding elements to a list then converting to a tuple
    def state_tuple(self):
        board_state=[]
        for row in range(0, self.side_length):
            for col in range(0, self.side_length):
                board_state.append(self.get(row, col))
        return tuple(board_state)

    #Compares the self state_tuple to the other boards state_tuple
    def __eq__(self,other_board):
        if self.state_tuple() == other_board.state_tuple():
            return True
        return False

    #Compares the self state_tuple to the solved_state tuple
    def solved(self):
        if self.state_tuple() == solve_state:
            return True
        return False

    #Check to see if the given tile is empty - == None -
    def is_empty(self, row, col):
        if self.get(row,col)==None:
            return True
        return False

    #Iterate through the board checking is_empty to find and return the empty_tile
    def get_empty(self):
        for row in range(0, self.side_length):
            for col in range(0, self.side_length):
                if self.is_empty(row,col):
                    return (row, col)

    #Find the empty_tile, then check to see that the 8 adjacent tiles are valid
    #Return the offsets that result in a valid tile minus [0,0] AKA no move
    def get_actions(self):
        actions = []
        empty_tile = self.get_empty()
        for row_delta in (-1,0,1):
            if empty_tile[0]+row_delta > -1 and empty_tile[0]+row_delta < self.side_length:
                if row_delta != 0:
                    actions.append([row_delta,0])
        for col_delta in (-1,0,1):
            if empty_tile[1]+col_delta > -1 and empty_tile[1]+col_delta < self.side_length:
                if col_delta !=0:
                    actions.append([0,col_delta])
        return actions

    #Create a copy of the board
    #Get the empty_tile coordinates
    #Get the tile to be moved
    #Swap the tiles according to the offset and return the newboard
    def move(self,offset):
        newboard = copy.deepcopy(self)
        empty_tile = self.get_empty()
        temp_tile = self.get(empty_tile[0]+offset[0],empty_tile[1]+offset[1])
        newboard.place(empty_tile[0], empty_tile[1], temp_tile)
        newboard.place(empty_tile[0]+offset[0], empty_tile[1]+offset[1], None)
        return newboard

    #Count InversionNumber, if InversionNumber is even, the puzzle is solvable
    def solvable(self):
        InversionNumber = 0
        board_state = self.state_tuple()
        length = len(board_state)
        for i in range(0,length):
            for j in range(i+1,length):
                if board_state[i] == None or board_state[j] == None:
                    pass
                elif board_state[j] < board_state[i]:
                    InversionNumber += 1
        if InversionNumber%2 == 0:
            return True
        return False

    #Shuffle and return a new board_state
    def shuffle(n):
        temp_state = list(solve_state)
        random.shuffle(temp_state)
        return TileBoard(n, tuple(temp_state))
