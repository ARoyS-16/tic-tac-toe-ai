import math

# Print the board nicely
def print_board(b):
    for i, r in enumerate(b):
        print(' | '.join(r))
        if i < 3:
            print('-' * 13)

# Check if a player has won
def check_win(b, p):
    for r in b:
        if all(c == p for c in r):
            return True

    for c in range(4):
        if all(b[r][c] == p for r in range(4)):
            return True

    if all(b[i][i] == p for i in range(4)):
        return True

    if all(b[i][3-i] == p for i in range(4)):
        return True

    return False

# Check if board is full
def is_full(b):
    return all(b[r][c] != '.' for r in range(4) for c in range(4))

# Minimax with Alpha-Beta pruning
def minimax(b, depth, alpha, beta, is_max):
    if check_win(b, 'O'):
        return 10 - depth
    if check_win(b, 'X'):
        return depth - 10
    if is_full(b) or depth == 0:
        return 0

    if is_max:
        best = -math.inf
        for r in range(4):
            for c in range(4):
                if b[r][c] == '.':
                    b[r][c] = 'O'
                    val = minimax(b, depth-1, alpha, beta, False)
                    b[r][c] = '.'
                    best = max(best, val)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        return best
        return best
    else:
        best = math.inf
        for r in range(4):
            for c in range(4):
                if b[r][c] == '.':
                    b[r][c] = 'X'
                    val = minimax(b, depth-1, alpha, beta, True)
                    b[r][c] = '.'
                    best = min(best, val)
                    beta = min(beta, best)
                    if beta <= alpha:
                        return best
        return best

# Choose best move for AI
def best_move(b):
    best_val = -math.inf
    move = None

    for r in range(4):
        for c in range(4):
            if b[r][c] == '.':
                b[r][c] = 'O'
                val = minimax(b, 6, -math.inf, math.inf, False)
                b[r][c] = '.'

                if val > best_val:
                    best_val = val
                    move = (r, c)

    return move

# Game loop
def play():
    board = [['.' for _ in range(4)] for _ in range(4)]

    print("4x4 Tic Tac Toe — You: X, AI: O")
    print("Enter row and column (0–3)\n")

    while True:
        print_board(board)

        try:
            r, c = map(int, input("\nYour move: ").split())
        except:
            print("Enter two numbers like: 1 2")
            continue

        if r not in range(4) or c not in range(4) or board[r][c] != '.':
            print("Invalid move.")
            continue

        board[r][c] = 'X'

        if check_win(board, 'X'):
            print_board(board)
            print("You win!")
            break

        if is_full(board):
            print_board(board)
            print("Draw!")
            break

        print("\nAI thinking...")
        mr, mc = best_move(board)
        board[mr][mc] = 'O'

        if check_win(board, 'O'):
            print_board(board)
            print("AI wins!")
            break

        if is_full(board):
            print_board(board)
            print("Draw!")
            break

play()
