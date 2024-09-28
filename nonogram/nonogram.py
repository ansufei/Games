import tkinter as tk
from tkinter import font
import matplotlib.pyplot as plt
from nonogram_utils import *
import numpy as np
from PIL import Image

# Ensure matplotlib uses the TkAgg backend
plt.switch_backend('TkAgg')

class Model:
    def __init__(self, img_index):
        #self.image, self.name = save_vector_images(img_index)
        self.image, self.name = use_tmp_img()
        self.new_image = self.generate_new_image()
        self.image_arr = np.array(self.new_image)
        self._grid_instructions = self.create_grid_instructions()
        self.grid_size = self.image_arr.shape[:2]

    def generate_new_image(self):
        self.image.show()
        cropped_img = Image.fromarray(crop_image(self.image), 'RGB')
        new_img = pixelize(30, cropped_img)
        # new_img = increase_contrast(new_img, 1)
        # new_img = increase_sharpness(new_img, 1.5)
        new_img = remove_light_colors(np.array(new_img), 130)
        new_img = Image.fromarray(crop_image(new_img, banner=False)) # crop again after removing some colors
        new_img = simplify_colors(new_img, nb_colors=3)
        plt.imshow(new_img)
        plt.show()
        #save_img('pixel_img/', new_img, self.name)
        return new_img
    
    def create_grid_instructions(self):
        colors = self.new_image.getcolors()
        colors = [list(y) for (x, y) in colors]
        grid = np.zeros(shape = (self.image_arr.shape[0], self.image_arr.shape[1]))
        for index, row in enumerate(self.image_arr):
            grid[index] = [colors.index(list(x)) for x in row]
        grid = count_consecutive_colors(np.array(grid))
        return grid
    
class Board(tk.Tk):
    def __init__(self, model):
        super().__init__()
        self.title("Nonogram")
        self._cells = {} # will contain buttons to be mapped to the coordinates of the cells
        self._model = model._grid_instructions
        self.width, self.height = model.grid_size
        self._create_board_display()
        self._create_board_grid()
        

    def _create_board_display(self): # information about the game's state and result (above the grid)
        display_frame = tk.Frame(master=self) # master = self <=> the game's main window will be the frame's parent
        display_frame.pack(fill=tk.X) # .pack() geometry manager to place the frame object on the main window's top border. tk.X will adjust the content to the size of the window
        self.display = tk.Label( # text displayed on the frame
            master=display_frame, # locate the label inside the frame
            text="Nouveau jeu", # default value
            font=font.Font(size=28, weight="bold"), # font of the label
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self.width):
            self.rowconfigure(row, weight=1)  # minimum width of each cell
            self.columnconfigure(row, weight=1)  # minimum height of each cell
            for col in range(self.height):
                button = tk.Button( # create a button object for each cell
                    master=grid_frame,
                    text="",
                    font=font.Font(size=8),
                    fg="black",
                    width=1,
                    height=1,
                    padx=0,
                    pady=0
                )
                self._cells[button] = (row, col) # adds every button to the cells dictionary
                button.grid( # add every button to the main window using the .grid() geometry manager
                    row=row,
                    column=col,
                    padx=0,
                    pady=0,
                    sticky="nsew"
                )

def main():
    """Create the game's board and run its main loop."""
    #root = tk.Tk()
    img = Model(img_index=1)
    board = Board(img)
    board.mainloop()

if __name__ == "__main__":
    main()