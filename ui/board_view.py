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

def update_possible_moves(container, possible_moves, current_heuristic, N=4, handle_move_callback=None):
    
    # Clear existing moves
    for widget in container.winfo_children():
        widget.destroy()
    
    if not possible_moves:
        no_moves_label = ttk.Label(container, text="No more moves available.", style="White.TLabel")
        no_moves_label.pack(pady=10)
        return
    
    # Dynamically determine the number of columns based on moves
    num_columns = min(3, len(possible_moves))
    if num_columns == 0:
        num_columns = 1
    
    # Create a grid of frames for moves
    for i, move in enumerate(possible_moves):
        # Determine background color based on heuristic comparison
        if move["heuristic"] < current_heuristic:
            bg_color = "#dcfce7"  
            hover_color = "#bbf7d0"  
        elif move["heuristic"] == current_heuristic:
            bg_color = "#fef9c3"  
            hover_color = "#fef08a" 
        else:
            bg_color = "#fee2e2"  
            hover_color = "#fecaca"  
        
        row, col = divmod(i, num_columns)
        
        move_frame = tk.Frame(container, bd=1, relief=tk.SOLID, bg=bg_color, 
                            width=150, height=120)
        move_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        move_frame.grid_propagate(False)  # Keep the frame at a fixed size
        
        # Add move information
        header_frame = tk.Frame(move_frame, bg=bg_color)
        header_frame.pack(fill=tk.X, padx=5, pady=2)
        
        move_label = tk.Label(header_frame, text=f"Move Queen in Col {move['changedCol']} to Row {move['newRow']}", 
                           bg=bg_color, font=("Arial", 9))
        move_label.pack(side=tk.LEFT)
        
        heuristic_label = tk.Label(header_frame, text=f"h = {move['heuristic']}", 
                                bg=bg_color, font=("Arial", 9, "bold"))
        heuristic_label.pack(side=tk.RIGHT)
        
        # Add mini chessboard
        mini_board = tk.Frame(move_frame, bg=bg_color)
        mini_board.pack(padx=5, pady=2)
        
        for mini_row in range(N):
            for mini_col in range(N):
                cell_color = "#fcd34d" if (mini_row + mini_col) % 2 == 0 else "#92400e" 
                cell = tk.Frame(mini_board, width=15, height=15, bg=cell_color)
                cell.grid(row=mini_row, column=mini_col, padx=0, pady=0)
                cell.grid_propagate(False)
                
                # Highlight the changed position
                if mini_col == move["changedCol"] and mini_row == move["newRow"]:
                    cell.config(highlightbackground="blue", highlightthickness=2)
                
                # Add queen symbol - ensure it's always created
                if move["config"][mini_col] == mini_row:
                    # Always use black queen on light cells and white queen on dark cells for contrast
                    queen_label = tk.Label(cell, text="♛", font=("Arial", 8),
                                        fg="black" if (mini_row + mini_col) % 2 == 0 else "black",
                                        bg=cell_color)  
                    queen_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Bind click event if callback provided
        if handle_move_callback:
            move_frame.bind("<Button-1>", lambda e, m=move: handle_move_callback(m))
            move_frame.bind("<Enter>", lambda e, frame=move_frame, color=hover_color: frame.config(bg=color))
            move_frame.bind("<Leave>", lambda e, frame=move_frame, color=bg_color: frame.config(bg=color))
            
            # Make all children also react to hover
            for child in move_frame.winfo_children():
                child.bind("<Enter>", lambda e, frame=move_frame, color=hover_color: frame.config(bg=color))
                child.bind("<Leave>", lambda e, frame=move_frame, color=bg_color: frame.config(bg=color))
                child.bind("<Button-1>", lambda e, m=move: handle_move_callback(m))
                # Handle grandchildren (like in mini boards)
                for grandchild in child.winfo_children():
                    grandchild.bind("<Button-1>", lambda e, m=move: handle_move_callback(m))
                
def update_solution_path(container, solution_path, N=4):
    
    # Clear existing path visualizations
    for widget in container.winfo_children():
        widget.destroy()
    
    # Add steps in solution path
    for step_index, step in enumerate(solution_path):
        # Create step frame
        if step["heuristic"] == 0:
            step_frame = tk.Frame(container, bd=1, relief=tk.SOLID, bg="#dcfce7")
        else:
            step_frame = tk.Frame(container, bd=1, relief=tk.SOLID, bg="#f3f4f6")
        
        step_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add step header
        header_frame = tk.Frame(step_frame, bg=step_frame["bg"])
        header_frame.pack(padx=5, pady=2)
        
        step_label = tk.Label(header_frame, text=f"Step {step_index}", 
                           bg=header_frame["bg"], font=("Arial", 9))
        step_label.pack()
        
        heuristic_label = tk.Label(header_frame, text=f"h = {step['heuristic']}", 
                                bg=header_frame["bg"], font=("Arial", 9, "bold"))
        heuristic_label.pack()
        
        # Add mini chessboard
        mini_board = tk.Frame(step_frame, bg=step_frame["bg"])
        mini_board.pack(padx=5, pady=2)
        
        for mini_row in range(N):
            for mini_col in range(N):
                cell_color = "#fcd34d" if (mini_row + mini_col) % 2 == 0 else "#92400e"  # amber-200 or amber-800
                cell = tk.Frame(mini_board, width=12, height=12, bg=cell_color)
                cell.grid(row=mini_row, column=mini_col, padx=0, pady=0)
                cell.grid_propagate(False)
                
                # Add queen symbol - ensure it's visible
                if step["config"][mini_col] == mini_row:
                    queen_label = tk.Label(cell, text="♛", font=("Arial", 6),
                                        fg="black" if (mini_row + mini_col) % 2 == 0 else "white")
                    queen_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def create_mini_board(parent, config, background_color, N=4, cell_size=15, highlight_col=None, highlight_row=None):
    
    mini_board = tk.Frame(parent, bg=background_color)
    mini_board.pack(padx=5, pady=2)
    
    for row in range(N):
        for col in range(N):
            cell_color = "#fcd34d" if (row + col) % 2 == 0 else "#92400e"  
            cell = tk.Frame(mini_board, width=cell_size, height=cell_size, bg=cell_color)
            cell.grid(row=row, column=col, padx=0, pady=0)
            cell.grid_propagate(False)
            
            # Highlight the cell if specified
            if col == highlight_col and row == highlight_row:
                cell.config(highlightbackground="blue", highlightthickness=2)
            
            # Add queen symbol if present at this position
            if config[col] == row:
                # Choose queen color for contrast
                queen_color = "black" if (row + col) % 2 == 0 else "white"
                queen_label = tk.Label(cell, text="♛", font=("Arial", int(cell_size/2)),
                                    fg=queen_color, bg=cell_color)
                queen_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    return mini_board