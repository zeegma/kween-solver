import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

from solver.queens_solver import QueensSolver
from solver.utils import generate_board_from_state
from ui.components import create_ui
from ui.board_view import update_board, update_possible_moves, update_solution_path

class FourQueensSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("4-Queens Local Search")
        self.root.geometry("750x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#F5ECEC") 
        
        # State variables
        self.N = 4
        self.queens_config = [0, 1, 2, 3]
        self.current_heuristic = 0
        self.possible_moves = []
        self.solution_path = []
        self.solved = False
        self.no_solution = False
        self.auto_solve_mode = False
        self.input_error = ""
        self.board = [[0 for _ in range(self.N)] for _ in range(self.N)]

        # Solver logic
        self.solver = QueensSolver(self.N)

        # UI setup
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        create_ui(self)
        self.initialize_board()

        # Style setup
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f9fafb")
        self.style.configure("White.TFrame", background="white")
        self.style.configure("TLabel", background="#f9fafb")
        self.style.configure("White.TLabel", background="white")
        self.style.configure("TButton", padding=6)

    def calculate_heuristic(self, state):
        return self.solver.calculate_heuristic(state)

    def generate_board_from_state(self, state):
        return generate_board_from_state(state, self.N)

    def generate_possible_moves(self, state):
        return self.solver.generate_possible_moves(state)

    def get_best_neighbor(self, state):
        return self.solver.get_best_neighbor(state)