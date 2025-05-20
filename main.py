import tkinter as tk
from ui.app import FourQueensSolver

def main():
    root = tk.Tk()
    app = FourQueensSolver(root)
    
    # Debug: Test various configurations to verify heuristic calculation
    test_configs = [
        [0,1,2,3],  # Initial config
        [2,0,3,1],  # Known solution
        [2,1,1,3],  # Configuration from the document
        [1,3,0,2],  # Another solution
    ]
    
    print("=== Heuristic Calculation Debug ===")
    print("Format: [col0_row, col1_row, col2_row, col3_row]")
    for config in test_configs:
        h = app.calculate_heuristic(config)
        print(f"Heuristic for configuration {config} is {h}")
    print("===================================")
    
    root.mainloop()

if __name__ == "__main__":
    main()