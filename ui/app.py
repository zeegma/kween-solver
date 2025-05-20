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
    
    def initialize_board(self):
        try:
            input_config = [int(val.strip()) for val in self.user_input_var.get().split(',')]
            if len(input_config) != self.N or not all(0 <= val < self.N for val in input_config):
                self.error_label.config(text=f"Enter exactly {self.N} values between 0 and {self.N - 1}")
                return

            self.error_label.config(text="")
            self.queens_config = input_config
            self.board = self.generate_board_from_state(input_config)
            self.current_heuristic = self.calculate_heuristic(input_config)

            self.heuristic_label.config(text=f"h = {self.current_heuristic}")
            if self.current_heuristic == 0:
                self.status_label.config(text="Solution Found!", background="#dcfce7", foreground="#166534")
                self.solved = True
            else:
                self.status_label.config(text="", background="white")
                self.solved = False

            self.no_solution = False
            self.possible_moves = self.generate_possible_moves(input_config)
            self.solution_path = [{"config": input_config.copy(), "heuristic": self.current_heuristic}]

            update_board(self.cells, self.queens_config)
            update_possible_moves(
                self.moves_container,
                self.possible_moves,
                self.current_heuristic,
                self.N,
                handle_move_callback=self.handle_move_selection
            )
            update_solution_path(self.path_frame_inner, self.solution_path, self.N)

        except Exception as e:
            self.error_label.config(
                text=f"Invalid input format. Use 4 comma-separated values 0-{self.N - 1}. Error: {str(e)}"
            )