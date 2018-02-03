from TileBoard import TileBoard

#Get the size of the game from the user, hope they choose 8 because it doesn't work otherwise
n = int(input("What size N-Puzzle? "))

#Shuffle until a solvable puzzle is found
n_puzzle = TileBoard.shuffle(n)
while n_puzzle.solvable() != True:
    n_puzzle = TileBoard.shuffle(n)

#Render the puzzle
print(n_puzzle.__repr__())

#While the puzzle is not solved, prompt for moves
while n_puzzle.solved() != True:

    print(n_puzzle.get_actions())
    print("Input your move as two comma separated numbers.")
    user_move = [int(x) for x in input().split(",")]

    #Draw the new puzzle
    n_puzzle = n_puzzle.move(user_move)
    print(n_puzzle.__repr__())

print("Congratulations, you won!")
