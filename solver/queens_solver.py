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
    
    def generate_possible_moves(self, state):
        # Generate all possible next states and evaluate them
        moves = []
        current_h = self.calculate_heuristic(state)
        
        # For each column, try placing the queen in each row
        for col in range(self.N):
            for row in range(self.N):
                # Skip the current position
                if row == state[col]:
                    continue
                
                # Create new state by moving queen in this column
                new_state = state.copy()
                new_state[col] = row
                
                # Calculate heuristic for the new state
                new_h = self.calculate_heuristic(new_state)
                
                moves.append({
                    "config": new_state,
                    "heuristic": new_h,
                    "changedCol": col,
                    "newRow": row
                })
        
        # Sort moves by heuristic (lowest first)
        moves.sort(key=lambda x: x["heuristic"])
        
        return moves
    
    def get_best_neighbor(self, state):
        # Find the best neighboring state according to hill climbing
        current_h = self.calculate_heuristic(state)
        best_state = state.copy()
        best_h = current_h
        
        # Check all possible moves (neighbors)
        for col in range(self.N):
            for row in range(self.N):
                # Skip current position
                if row == state[col]:
                    continue
                
                # Try this neighbor
                new_state = state.copy()
                new_state[col] = row
                new_h = self.calculate_heuristic(new_state)
                
                # If it's better, update best
                if new_h < best_h:
                    best_h = new_h
                    best_state = new_state.copy()
        
        return best_state, best_h