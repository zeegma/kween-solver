import tkinter as tk
from tkinter import ttk

def create_ui(app):
    """Create and place all UI components"""
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

