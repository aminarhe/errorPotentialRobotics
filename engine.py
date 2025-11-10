# Board: 3x3 with 0 = empty, 1 = X, 2 = O

def winner_simple(board):
    # rows, cols, diags
    for r in range(3):
        if board[r][0] != 0 and board[r][0] == board[r][1] == board[r][2]:
            return board[r][0]
    for c in range(3):
        if board[0][c] != 0 and board[0][c] == board[1][c] == board[2][c]:
            return board[0][c]
    if board[0][0] != 0 and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] != 0 and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    # draw or ongoing
    if all(board[r][c] != 0 for r in range(3) for c in range(3)):
        return 0  # draw
    return None  # ongoing

def best_move(board, player):
    """
    Returns (r, c) for the optimal move for `player` (1 or 2).
    Uses full minimax => perfect play.
    """
    opponent = 3 - player

    def minimax(b, turn):
        w = winner_simple(b)
        if w is not None:
            if w == player:
                return 1
            elif w == opponent:
                return -1
            else:
                return 0

        if turn == player:
            best = -2
            for r in range(3):
                for c in range(3):
                    if b[r][c] == 0:
                        b[r][c] = player
                        score = minimax(b, opponent)
                        b[r][c] = 0
                        if score > best:
                            best = score
            return best
        else:
            best = 2
            for r in range(3):
                for c in range(3):
                    if b[r][c] == 0:
                        b[r][c] = opponent
                        score = minimax(b, player)
                        b[r][c] = 0
                        if score < best:
                            best = score
            return best

    best_score = -2
    best_move_rc = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                board[r][c] = player
                score = minimax(board, opponent)
                board[r][c] = 0
                if score > best_score:
                    best_score = score
                    best_move_rc = (r, c)

    return best_move_rc
