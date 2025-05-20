import tkinter as tk
from tkinter import ttk

def create_ui(app):
    """Create and place all UI components"""
    # Title
    title_label = ttk.Label(app.main_frame, text="4-Queens Local Search Solver", 
                           font=("Arial", 16, "bold"))
    title_label.pack(pady=10)
