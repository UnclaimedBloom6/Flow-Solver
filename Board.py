
from PIL import Image, ImageGrab
from colorshit import *

class Board:

    def __init__(self):
        """Scans the screen and looks for a flow puzzle. If one is found, initializes everything and creates the board."""
        corner1 = (6, 306)
        corner2 = (713, 1084)

        self.colored = ImageGrab.grab(bbox=(*corner1, *corner2))
        self.grayscaled = self.colored.convert('L')

        self.monochrome = mono(self.grayscaled, 60)
        self.monochrome.save("images/monochrome.png")

        self.corner = self.get_corner()
        if self.corner is None:
            print("Board not found!")
            return

        self.corner_screen = (corner1[0] + self.corner[0], corner1[1] + self.corner[1])
        print(f"Corner: {self.corner}")
        print(f"Corner SCREEN: {self.corner_screen}")

        self.crop_shit()
        self.cell_size = self.get_cell_size()
        print(f"Cell Size: {self.cell_size}")

        self.puzzle_size = self.get_puzzle_size()
        print(f"Puzzle Size: {self.puzzle_size}")

        self.colored.save("images/cropped.png")
        self.grayscaled.save("images/grayscaled.png")
        self.monochrome.save("images/monochrome.png")

        self.board = [[None for _ in range(self.puzzle_size[0])] for _ in range(self.puzzle_size[1])]
        self.endpoints = []
        
        self.parse_board()


        print("Bored init finished!")
    
    def get_corner(self):
        """Gets the top left corner of the board"""
        for y in range(int(self.monochrome.height/5)):
            for x in range(int(self.monochrome.width/5)):
                pixel = self.monochrome.getpixel((x, y))
                if pixel == 255:
                    continue
                kapow = False
                for i in range(20):
                    if self.monochrome.getpixel((x+i, y)) == 255:
                        kapow = True
                        break
                if kapow:
                    continue
                for i in range(20):
                    if self.monochrome.getpixel((x, y+i)) == 255:
                        kapow = True
                        break
                if kapow:
                    continue
                return (x, y)

    def crop_shit(self):
        """Crops the Board's colored, grayscale and monochrome images to only show the board."""
        width = 0
        height = 0
        x, y = self.corner
        while x+width < self.monochrome.width and self.monochrome.getpixel((x+width, y)) == 0:
            width += 1
        while y+height < self.monochrome.height and self.monochrome.getpixel((x, y+height)) == 0:
            height += 1
        crop_box = (*self.corner, x+width, y+height)

        self.colored = self.colored.crop(crop_box)
        self.monochrome = self.monochrome.crop(crop_box)
        self.grayscaled = self.grayscaled.crop(crop_box)

    def get_cell_size(self):
        """Gets the cell size in pixels based off the cropped monochrome image."""
        offset = 0
        while self.monochrome.getpixel((offset, offset)) == 0:
            offset += 1

        cell_size = 0
        while self.monochrome.getpixel((offset+cell_size, offset)) == 255:
            cell_size += 1

        return cell_size + offset

    def get_puzzle_size(self):
        """Gets the size of the puzzle. Eg (5, 5) for a 5x5 puzzle."""
        return (round(self.monochrome.width/self.cell_size), round(self.monochrome.height/self.cell_size))

    def set_cell(self, xy, color):
        """Sets the color of the cell on the board."""
        x, y = xy
        self.board[y][x] = color
    
    def get_cell(self, xy):
        """Returns the color of the cell at the x,y position on the board."""
        x, y = xy
        return self.board[y][x]
    
    def is_corner(self, xy):
        return xy[0] % (self.puzzle_size[0]-1) == 0 and xy[1] % (self.puzzle_size[1]-1) == 0
    
    def get_all_cells_of_color(self, color):
        cells = []
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if col != color:
                    continue
                cells.append((x, y))
        return cells
    
    def get_flow(self, xy):
        """Gets the coordinates of every cell connected to the same flow at the given (x, y)"""

        color = self.get_cell(xy)
        if color is None:
            return []

        visited = set()
        cells = []
        queue = [xy]

        while len(queue):
            pos = queue.pop(0)
            if pos in visited:
                continue
            visited.add(pos)

            if self.get_cell(pos) != color:
                continue

            cells.append(pos)

            for cell in self.get_adjacent_cells(pos):
                queue.append(cell)
        return cells
    
    def is_flow_complete(self, xy, flow=None):
        return len(self.get_flow(xy) if flow is None else flow) == len(self.get_all_cells_of_color(self.get_cell(xy)))

    def get_adjacent_cells(self, xy):
        """Gets all of the adjacent cells around the (x, y) position on the board."""
        x, y = xy
        arr = []
        for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if nx < 0 or ny < 0 or nx == self.puzzle_size[0] or ny == self.puzzle_size[1]:
                continue
            arr.append((nx, ny))
        return arr

    def board_complete(self):
        """Checks if all of the cells in the board have been filled and that all flows are valid."""
        if len(self.get_all_cells_of_color(None)) != 0:
            return False
        visited = set()
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if (x, y) in visited:
                    continue
                flow = self.get_flow((x, y))
                if not self.is_flow_complete((x, y), flow):
                    return False
                for i in flow:
                    visited.add(i)
        
        return True
    
    def blocks_another_color(self, xy: tuple[int, int], initial_color):
        """Checks if a move blocks another color from being able to move"""
        # print(f"Checking if {xy} ({initial_color}) is blocking...")
        for child in self.get_adjacent_cells(xy):
            child_color = self.get_cell(child)
            if child_color is None or child_color == initial_color:
                continue
            
            # print(f"\nCurrent Child: {child} ({child_color})")
            secondary = [i for i in self.get_adjacent_cells(child) if i != xy]
            # print(f"BEFORE: {secondary}")
            to_delete = []
            for i in secondary:
                secondary_color = self.get_cell(i)
                # print(f"Checking secondary {i} ({secondary_color})")
                if secondary_color == child_color:
                    continue
                if secondary_color is None:
                    continue
                to_delete.append(i)
            final = [i for i in secondary if i not in to_delete]
            # print(f"FINAL: {final}")
            if len(final) == 0:
                return True

        return False

    def get_possible_moves(self, xy):
        """Gets all of the possible moves the cell at the given (x, y) position on the board can move to."""
        # x, y = xy
        if self.is_flow_complete(xy):
            return []
        current_flow = self.get_flow(xy)
        if xy in self.endpoints and len(current_flow) > 1:
            return []
        color = self.get_cell(xy)
        if color is None:
            return []

        adjacent = self.get_adjacent_cells(xy)
        possible = []
        for cell in adjacent:
            nx, ny = cell
            # Already Occupied
            if self.get_cell(cell) is not None:
                continue

            # Forced corner move
            if self.is_corner(cell):
                return [cell]
            
            # Blocks another color from moving
            if self.blocks_another_color(cell, color):
                continue

            # Adjacent to itself
            adjacent_2 = [i for i in self.get_adjacent_cells(cell) if i != xy and self.get_cell(i) == color]
            if len(adjacent_2) >= 1 and self.get_flow(adjacent_2[0])[0] in current_flow:
                continue

            possible.append(cell)
        
        possible.sort(key=lambda x: len(self.get_adjacent_cells(x)))
        return possible
    
    def is_cell_on_end(self, xy):
        return len([i for i in self.get_adjacent_cells(xy) if self.get_cell(i) == self.get_cell(xy)]) <= 1

    def get_all_moves(self):
        moves = []
        for y, row in enumerate(self.board):
            for x, color in enumerate(row):
                if color is None or not self.is_cell_on_end((x, y)):
                    continue
                possible = self.get_possible_moves((x, y))
                if len(possible) == 0:
                    continue
                moves.append(((x, y), possible))

        return sorted(moves, key=lambda a: len(a[1]))

    def parse_board(self):
        """Reads the pixels from the grayscaled image and fills in the existing colors on the board."""
        for y in range(self.puzzle_size[1]):
            for x in range(self.puzzle_size[0]):
                image_x = self.cell_size * x + self.cell_size/2
                image_y = self.cell_size * y + self.cell_size/2
                gray_color = self.grayscaled.getpixel((image_x, image_y))

                for color, info in colors.items():
                    if info["gray_value"] == gray_color:
                        self.set_cell((x, y), color)
                        self.endpoints.append((x, y))
        
    def print_board(self):
        print_square("White", False, self.puzzle_size[0]+2, True)
        for row in self.board:
            print_square("White", False, 1, False)
            for color in row:
                print_square(color, True, 1, False)
            print_square("White", False, 1, True)
        print_square("White", False, self.puzzle_size[0]+2, True)
