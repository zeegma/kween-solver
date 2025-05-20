def generate_board_from_state(state, N):
    # Generate a board from the state representation
    board = [[0 for _ in range(N)] for _ in range(N)]
    for col, row in enumerate(state):
        board[row][col] = 1
    return board