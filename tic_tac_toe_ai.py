import math
import random

SIZE = 4
HUMAN = 'X'
AI = 'O'
EMPTY = '.'

# depth per difficulty
LEVELS = {
    "1": 2,   # Easy
    "2": 4,   # Medium
    "3": 6    # Hard
}


def print_board(board):
    for i, row in enumerate(board):
        print(' | '.join(row))
        if i < SIZE - 1:
            print('-' * (SIZE * 4 - 3))


def check_win(board, player):
    for i in range(SIZE):
        if all(board[i][c] == player for c in range(SIZE)):
            return True
        if all(board[r][i] == player for r in range(SIZE)):
            return True

    if all(board[i][i] == player for i in range(SIZE)):
        return True
    if all(board[i][SIZE-1-i] == player for i in range(SIZE)):
        return True

    return False


def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)


# ⭐ Heuristic evaluation for non-terminal boards
def evaluate(board):
    score = 0
    lines = []

    # collect rows, cols, diagonals
    lines.extend(board)
    lines.extend([[board[r][c] for r in range(SIZE)] for c in range(SIZE)])
    lines.append([board[i][i] for i in range(SIZE)])
    lines.append([board[i][SIZE-1-i] for i in range(SIZE)])

    for line in lines:
        if HUMAN not in line:
            score += line.count(AI) ** 2
        elif AI not in line:
            score -= line.count(HUMAN) ** 2

    return score


def minimax(board, depth, alpha, beta, maximizing):
    if check_win(board, AI):
        return 100 - depth
    if check_win(board, HUMAN):
        return depth - 100
    if is_full(board):
        return 0
    if depth == 0:
        return evaluate(board)

    moves = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == EMPTY]
    # center-first ordering speeds pruning
    moves.sort(key=lambda m: abs(m[0]-1.5)+abs(m[1]-1.5))

    if maximizing:
        best = -math.inf
        for r, c in moves:
            board[r][c] = AI
            val = minimax(board, depth-1, alpha, beta, False)
            board[r][c] = EMPTY
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = math.inf
        for r, c in moves:
            board[r][c] = HUMAN
            val = minimax(board, depth-1, alpha, beta, True)
            board[r][c] = EMPTY
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def best_move(board, depth, difficulty):
    moves = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == EMPTY]

    # 🎲 Easy mode sometimes random
    if difficulty == "1" and random.random() < 0.5:
        return random.choice(moves)

    best_val = -math.inf
    best = None

    for r, c in moves:
        board[r][c] = AI
        val = minimax(board, depth, -math.inf, math.inf, False)
        board[r][c] = EMPTY

        if val > best_val:
            best_val = val
            best = (r, c)

    return best


def play():
    board = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

    print("Choose difficulty:")
    print("1 = Easy\n2 = Medium\n3 = Hard")
    difficulty = input("> ").strip()
    depth = LEVELS.get(difficulty, 4)

    print("\n4x4 Tic Tac Toe — You: X, AI: O\n")

    while True:
        print_board(board)

        try:
            r, c = map(int, input("\nYour move: ").split())
        except:
            print("Enter two numbers like: 1 2")
            continue

        if r not in range(SIZE) or c not in range(SIZE) or board[r][c] != EMPTY:
            print("Invalid move.")
            continue

        board[r][c] = HUMAN

        if check_win(board, HUMAN):
            print_board(board)
            print("You win!")
            break
        if is_full(board):
            print_board(board)
            print("Draw!")
            break

        print("\nAI thinking...")
        move = best_move(board, depth, difficulty)
        if move:
            board[move[0]][move[1]] = AI

        if check_win(board, AI):
            print_board(board)
            print("AI wins!")
            break
        if is_full(board):
            print_board(board)
            print("Draw!")
            break


play()
