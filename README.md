
# Flow Bot

Solves and completes puzzles on the game "Flow Free" which can be downloaded from the Microsoft store.


## Installation

To use, install the Python libraries:
- PyAutoIt
- PyAutoGui (Although not used directly, autoit will not work properly if it is not at least imported.)
- PIL
- Keyboard

To configure the bot to your system, to into Board.py and change corner1 and corner2 so that they can contain every board.
You don't need to align the corners to the corner of the puzzle, the program will find that automatically.
For example, my corners are set so that the program scans an area like this:
<img src="https://i.imgur.com/CNEJ2gT.png">

Once your corner has been configured and you have Flow Free open, run main.py and press F4 to start the solve.

## How It Works

The solver finds all of the possible moves for each color and sorts them based on how many possibilities there are. The solver will recursively check each of them and backtrack if the puzzle is filled but the board is invalid.

The speed variation is massive depending on the puzzles. For small ones like 5x5 and 7x7 it can solve almost immediately (Mostly), however for puzzles 8x8 and onwards it often struggles and takes significantly longer.

This could be improved by sorting the possible moves by how good they are, eg if a flow is on a wall or against another flow then it will want to keep being on the wall etc.