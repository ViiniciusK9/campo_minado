from tkinter import Button, Label
import settings
import random
import ctypes
import sys


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append the objeto to the Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4
        )
        btn.bind('<Button-1>', self.left_click_actions) # Left Click
        btn.bind('<Button-3>', self.right_click_actions) # Right Click
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg='white',
            fg='black',
            text=f'Cells Left: {Cell.cell_count}',
            width=12,
            height=4,
            font=("", 30)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.sorrounded_cells_mines_length == 0:
                for cell_obj in self.sorround_cells:
                    cell_obj.show_cell()
            self.show_cell()
            # If Mines count is equal to the cells left count, player won
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game!', 'Game Win', 0)
                sys.exit()


        # Cancel Left and Right click events if cell is already opened:
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    @staticmethod
    def get_cell_by_axis(x, y):
        # Return a cell object based on the value of x and y.
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def sorround_cells(self):
        cells = []
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if i != self.x or j != self.y:
                    result = self.get_cell_by_axis(i, j)

                    if result is not None:
                        cells.append(result)

        return cells

    @property
    def sorrounded_cells_mines_length(self):
        counter = 0
        for cell in self.sorround_cells:
            if cell.is_mine:
                counter += 1

        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=f'{self.sorrounded_cells_mines_length}')
            # Replace the text of cell label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f'Cells Left: {Cell.cell_count}'
                )

            # If this was a mine candidate, then for safety, we should
            # configure the background color to SystemButtonFace
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )

            # Mark the call as opened (Use is as the last line of this method)
            self.is_opened = True


    def show_mine(self):
        # A logic to interrupt the game and display a message that player lost!
        self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        sys.exit()



    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                bg='orange'
            )
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)

        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f'Cell({self.x}, {self.y})'
