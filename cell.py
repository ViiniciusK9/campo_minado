from tkinter import Button
import settings
import random



class Cell:
    all = []
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
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

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.sorrounded_cells_mines_length == 0:
                for cell_obj in self.sorround_cells:
                    cell_obj.show_cell()
            self.show_cell()


    def get_cell_by_axis(self, x, y):
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
        self.cell_btn_object.configure(text=f'{self.sorrounded_cells_mines_length}')

    def show_mine(self):
        # A logic to interrupt the game and display a message that player lost!
        self.cell_btn_object.configure(bg='red')

    def right_click_actions(self, event):
        print(event)
        print("I am right cliked!")

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)

        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f'Cell({self.x}, {self.y})'
