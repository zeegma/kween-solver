from solver.utils import generate_board_from_state

class QueensSolver:
    
    def __init__(self, N=4):
        self.N = N  # Board size

    def calculate_heuristic(self, state):
        # Calculate the heuristic for the given state
        board = generate_board_from_state(state, self.N)
        attacking = 0
        
        for i in range(self.N):
            row = state[i]
            
            # Left
            col = i - 1
            while col >= 0 and board[row][col] != 1:
                col -= 1
            if col >= 0 and board[row][col] == 1:
                attacking += 1
            
            # Right
            col = i + 1
            while col < self.N and board[row][col] != 1:
                col += 1
            if col < self.N and board[row][col] == 1:
                attacking += 1
            
            # Diagonal Left Up
            row = state[i] - 1
            col = i - 1
            while row >= 0 and col >= 0 and board[row][col] != 1:
                row -= 1
                col -= 1
            if row >= 0 and col >= 0 and board[row][col] == 1:
                attacking += 1
            
            # Diagonal Right Down
            row = state[i] + 1
            col = i + 1
            while row < self.N and col < self.N and board[row][col] != 1:
                row += 1
                col += 1
            if row < self.N and col < self.N and board[row][col] == 1:
                attacking += 1
            
            # Diagonal Left Down
            row = state[i] + 1
            col = i - 1
            while row < self.N and col >= 0 and board[row][col] != 1:
                row += 1
                col -= 1
            if row < self.N and col >= 0 and board[row][col] == 1:
                attacking += 1
            
            # Diagonal Right Up
            row = state[i] - 1
            col = i + 1
            while row >= 0 and col < self.N and board[row][col] != 1:
                row -= 1
                col += 1
            if row >= 0 and col < self.N and board[row][col] == 1:
                attacking += 1
        
        # Divide by 2 because each attack is counted twice (once from each queen)
        return int(attacking / 2)