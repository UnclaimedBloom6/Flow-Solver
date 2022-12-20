
from colorshit import *
from Board import Board
import keyboard
import autoit
import pyautogui

def solve(board: Board):
    """Recursively solve the puzzle"""
    if board.board_complete():
        return True

    moves = board.get_all_moves()
    if len(moves) == 0:
        return False
    
    # for cell, pos in moves:
    cell, pos = moves[0]
    for c in pos:
        board.set_cell(c, board.get_cell(cell))
        board.print_board()
        if solve(board):
            return True
        board.set_cell(c, None)
        
    return False


def go_crazy(board: Board):
    """Uses AutoIt to simulate mouse inputs to automatically fill in the solved puzzle."""
    # print(f"End Points: {board.end_points}")
    visited = set()
    cells = []
    for row in board.board:
        cells.extend(row)
    # print(cells)
    for i in range(len(cells)):
        x = i%board.puzzle_size[0]
        y = i//board.puzzle_size[1]
        if (x, y) in visited:
            continue

        if (x, y) not in board.endpoints:
            continue
        # print(f"Starting flow at {(x, y)}")
        connected = board.get_flow((x, y))
        # print(connected)
        for c in connected:
            visited.add(c)

        # print(f"{board.get_cell((x, y))}: {connected}")
        for j in range(len(connected)):
            nx, ny = connected[j]
            click_x = int(board.corner_screen[0] + board.cell_size * nx + board.cell_size/2)
            click_y = int(board.corner_screen[1] + board.cell_size * ny + board.cell_size/2)
            autoit.mouse_move(click_x, click_y, speed=1)

            if j == 0 or j == len(connected)-1:
                autoit.mouse_click("left", click_x, click_y, speed=1)
        
    autoit.mouse_move(362, 663, speed=1)
    autoit.mouse_click("left", 362, 663, speed=1)

def main():

    while True:
        print("Press F4 to start solving!")
        keyboard.wait("f4")

        board = Board()
        if not board.corner:
            continue

        board.print_board()

        solve(board)
        go_crazy(board)

main()

# Using old system

# Moves Must:
# - Not block other color
# - Go to a corner if adjacent
# - Not put itself adjacent to itself
# - Not create a dead-end

# And ideally:
# - Prioritize edges until interrupted