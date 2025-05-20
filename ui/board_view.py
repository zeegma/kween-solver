import tkinter as tk
from tkinter import ttk


def create_board(parent, N=4, cell_size=50):

    # Create the board frame
    board_frame = ttk.Frame(parent, style="White.TFrame")
    board_frame.pack(padx=10, pady=10)
    
    # Create cells for the board
    cells = []
    for row in range(N):
        row_cells = []
        for col in range(N):
            # Alternate colors for chess pattern - amber colors
            cell = tk.Frame(board_frame, width=cell_size, height=cell_size, 
                          bg="#fcd34d" if (row + col) % 2 == 0 else "#92400e")
            cell.grid(row=row, column=col)
            cell.grid_propagate(False)  
            row_cells.append(cell)
        cells.append(row_cells)
    
    return board_frame, cells

def update_board(cells, queens_config):
    
    N = len(queens_config)
    
    # Clear all queen symbols
    for row in range(N):
        for col in range(N):
            for widget in cells[row][col].winfo_children():
                widget.destroy()
    
    # Place queens according to current configuration
    for col, row in enumerate(queens_config):
        queen_label = tk.Label(cells[row][col], text="♛", font=("Arial", 20),
                            fg="black")  
        queen_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
