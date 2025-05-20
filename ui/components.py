import tkinter as tk
from tkinter import ttk

def create_ui(app):
    # Title
    title_label = ttk.Label(app.main_frame, text="4-Queens Local Search Solver", 
                           font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # User Input Section
    input_frame = ttk.Frame(app.main_frame, style="White.TFrame")
    input_frame.pack(fill=tk.X, pady=10, padx=5)
    
    input_title = ttk.Label(input_frame, text="Initial Configuration", 
                          font=("Arial", 12, "bold"), style="White.TLabel")
    input_title.pack(anchor=tk.CENTER, pady=5)
    
    input_desc = ttk.Label(input_frame, 
                         text="Enter four comma-separated values (0-3) representing the row position of each queen in columns 0-3.",
                         style="White.TLabel")
    input_desc.config(justify="center")
    input_desc.pack(anchor=tk.CENTER, pady=2)
    
    input_container = ttk.Frame(input_frame, style="White.TFrame")
    input_container.pack(pady=5)
    
    app.user_input_var = tk.StringVar(value="0,1,2,3")
    app.user_input = ttk.Entry(input_container, textvariable=app.user_input_var, width=30)
    app.user_input.pack(pady=5)
    
    buttons_frame = ttk.Frame(input_container, style="White.TFrame")
    buttons_frame.pack(pady=5)

    set_btn = ttk.Button(buttons_frame, text="Set Position", command=app.initialize_board)
    set_btn.pack(side=tk.LEFT, padx=5)

    reset_btn = ttk.Button(buttons_frame, text="Reset", command=app.reset_board)
    reset_btn.pack(side=tk.LEFT, padx=5)
    
    app.error_label = ttk.Label(input_frame, text="", foreground="red", style="White.TLabel")
    app.error_label.pack(anchor=tk.W, padx=10, pady=2)

    # Current State Section
    state_frame = ttk.Frame(app.main_frame, style="White.TFrame")
    state_frame.pack(fill=tk.X, pady=10, padx=5)
    
    state_header = ttk.Frame(state_frame, style="White.TFrame")
    state_header.pack(fill=tk.X, padx=10, pady=5)
    
    state_title = ttk.Label(state_header, text="Current State", 
                          font=("Arial", 12, "bold"), style="White.TLabel")
    state_title.pack(side=tk.LEFT)
    
    app.state_info_frame = ttk.Frame(state_header, style="White.TFrame")
    app.state_info_frame.pack(side=tk.RIGHT)
    
    app.heuristic_label = ttk.Label(app.state_info_frame, text="h = 0", 
                                   font=("Arial", 12, "bold"), style="White.TLabel")
    app.heuristic_label.pack(side=tk.LEFT, padx=5)
    
    app.status_label = ttk.Label(app.state_info_frame, text="", style="White.TLabel")
    app.status_label.pack(side=tk.LEFT, padx=5)

    # Chessboard
    app.board_frame = ttk.Frame(state_frame, style="White.TFrame")
    app.board_frame.pack(padx=10, pady=10)
    
    app.cells = []
    for row in range(4):
        row_cells = []
        for col in range(4):
            cell = tk.Frame(app.board_frame, width=50, height=50, 
                          bg="#fcd34d" if (row + col) % 2 == 0 else "#92400e")  # amber-200 or amber-800
            cell.grid(row=row, column=col)
            cell.grid_propagate(False)  # Force the frame to be exactly the size we want
            row_cells.append(cell)
        app.cells.append(row_cells)
    
    # Auto-solve button
    app.auto_solve_btn = ttk.Button(state_frame, text="Auto-Solve", command=app.toggle_auto_solve)
    app.auto_solve_btn.pack(padx=10, pady=5)

    # Possible Moves Section with Scrolling
    moves_frame = ttk.Frame(app.main_frame, style="White.TFrame")
    moves_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=5)
    
    moves_title = ttk.Label(moves_frame, text="Possible Moves", 
                          font=("Arial", 12, "bold"), style="White.TLabel")
    moves_title.pack(anchor=tk.W, padx=10, pady=5)
    
    # Create a canvas with scrollbar for possible moves
    moves_canvas_frame = ttk.Frame(moves_frame, style="White.TFrame")
    moves_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Vertical scrollbar
    moves_vscrollbar = ttk.Scrollbar(moves_canvas_frame, orient=tk.VERTICAL)
    moves_vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Horizontal scrollbar
    moves_hscrollbar = ttk.Scrollbar(moves_canvas_frame, orient=tk.HORIZONTAL)
    moves_hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Canvas for moves
    app.moves_canvas = tk.Canvas(moves_canvas_frame, bg="white", 
                                yscrollcommand=moves_vscrollbar.set,
                                xscrollcommand=moves_hscrollbar.set)
    app.moves_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Configure scrollbars
    moves_vscrollbar.config(command=app.moves_canvas.yview)
    moves_hscrollbar.config(command=app.moves_canvas.xview)
    
    # Create a frame inside the canvas to hold all move frames
    app.moves_container = ttk.Frame(app.moves_canvas, style="White.TFrame")
    app.moves_canvas_window = app.moves_canvas.create_window((0, 0), window=app.moves_container, anchor=tk.NW)
    
    # Configure the moves container to update the scrollregion when its size changes
    app.moves_container.bind("<Configure>", app.on_moves_container_configure)
    app.moves_canvas.bind("<Configure>", app.on_moves_canvas_configure)

    # Solution Path Section
    path_frame = ttk.Frame(app.main_frame, style="White.TFrame")
    path_frame.pack(fill=tk.X, pady=10, padx=5)
    
    path_title = ttk.Label(path_frame, text="Solution Path", 
                         font=("Arial", 12, "bold"), style="White.TLabel")
    path_title.pack(anchor=tk.W, padx=10, pady=5)
    
    # Create a canvas with scrollbar for the solution path
    path_canvas_frame = ttk.Frame(path_frame, style="White.TFrame")
    path_canvas_frame.pack(fill=tk.X, padx=10, pady=5)
    
    app.path_canvas = tk.Canvas(path_canvas_frame, height=150, bg="white")
    app.path_canvas.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    path_scrollbar = ttk.Scrollbar(path_canvas_frame, orient=tk.HORIZONTAL, command=app.path_canvas.xview)
    path_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    app.path_canvas.configure(xscrollcommand=path_scrollbar.set)
    
    app.path_frame_inner = ttk.Frame(app.path_canvas, style="White.TFrame")
    app.path_canvas.create_window((0, 0), window=app.path_frame_inner, anchor=tk.NW)
    app.path_frame_inner.bind("<Configure>", lambda e: app.path_canvas.configure(
        scrollregion=app.path_canvas.bbox("all")))
    
    







