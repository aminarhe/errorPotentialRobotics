#!/usr/bin/env python3
import sys, pygame, math, random

WIDTH, HEIGHT = 360, 420
GRID_SIZE = 3
CELL = WIDTH // GRID_SIZE
LINE_W = 6
BG = (245, 245, 245)
FG = (30, 30, 30)
ACCENT = (50, 120, 240)
WINLINE = (220, 70, 70)

pygame.init()
pygame.display.set_caption("Tic Tac Toe (Pygame) — Press A to toggle AI")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
bigfont = pygame.font.SysFont(None, 42)

# Board state: 0 empty, 1 X, 2 O
def new_board():
    return [[0]*GRID_SIZE for _ in range(GRID_SIZE)]

def draw_grid():
    screen.fill(BG)
    # grid lines
    for i in range(1, GRID_SIZE):
        # vertical
        pygame.draw.line(screen, FG, (i*CELL, 0), (i*CELL, WIDTH), LINE_W)
        # horizontal
        pygame.draw.line(screen, FG, (0, i*CELL), (WIDTH, i*CELL), LINE_W)

def draw_mark(r, c, player):
    # player 1 => X, player 2 => O
    cx = c*CELL + CELL//2
    cy = r*CELL + CELL//2
    size = CELL//3
    if player == 1:
        pygame.draw.line(screen, ACCENT, (cx-size, cy-size), (cx+size, cy+size), LINE_W)
        pygame.draw.line(screen, ACCENT, (cx+size, cy-size), (cx-size, cy+size), LINE_W)
    elif player == 2:
        pygame.draw.circle(screen, ACCENT, (cx, cy), size, LINE_W)

def check_winner(board):
    # returns (winner, line) where winner in {0,1,2}, line is ((x1,y1),(x2,y2)) for drawing winline
    # rows
    for r in range(GRID_SIZE):
        if board[r][0] != 0 and all(board[r][c] == board[r][0] for c in range(GRID_SIZE)):
            y = r*CELL + CELL//2
            return board[r][0], ((10, y), (WIDTH-10, y))
    # cols
    for c in range(GRID_SIZE):
        if board[0][c] != 0 and all(board[r][c] == board[0][c] for r in range(GRID_SIZE)):
            x = c*CELL + CELL//2
            return board[0][c], ((x, 10), (x, WIDTH-10))
    # diag
    if board[0][0] != 0 and all(board[i][i] == board[0][0] for i in range(GRID_SIZE)):
        return board[0][0], ((10, 10), (WIDTH-10, WIDTH-10))
    # anti-diag
    if board[0][GRID_SIZE-1] != 0 and all(board[i][GRID_SIZE-1-i] == board[0][GRID_SIZE-1] for i in range(GRID_SIZE)):
        return board[0][GRID_SIZE-1], ((10, WIDTH-10), (WIDTH-10, 10))
    # draw?
    if all(board[r][c] != 0 for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
        return 0, None  # 0 but full => draw
    return None, None  # game ongoing

def available_moves(board):
    return [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == 0]

def minimax(board, player, ai_player, human_player):
    # Terminal check
    winner, _ = check_winner(board)
    if winner is not None:
        # winner in {0,1,2}; 0 with full means draw
        if winner == ai_player:
            return 10, None
        elif winner == human_player:
            return -10, None
        else:
            return 0, None

    # Not terminal: maximize for ai_player, minimize for human
    if player == ai_player:
        best_score, best_move = -999, None
        for (r, c) in available_moves(board):
            board[r][c] = ai_player
            score, _ = minimax(board, 3-player, ai_player, human_player)
            board[r][c] = 0
            if score > best_score:
                best_score, best_move = score, (r, c)
        return best_score, best_move
    else:
        best_score, best_move = 999, None
        for (r, c) in available_moves(board):
            board[r][c] = human_player
            score, _ = minimax(board, 3-player, ai_player, human_player)
            board[r][c] = 0
            if score < best_score:
                best_score, best_move = score, (r, c)
        return best_score, best_move

def ai_move(board, ai_player, human_player):
    moves = available_moves(board)
    if not moves:
        return None
    _, move = minimax(board, ai_player, ai_player, human_player)
    if move is None:
        move = random.choice(moves)
    return move

def draw_status_bar(msg, sub=None):
    pygame.draw.rect(screen, (230, 230, 230), (0, WIDTH, WIDTH, HEIGHT-WIDTH))
    text = bigfont.render(msg, True, FG)
    screen.blit(text, (12, WIDTH + 6))
    if sub:
        small = font.render(sub, True, (80, 80, 80))
        screen.blit(small, (12, WIDTH + 44))

def main():
    board = new_board()
    current_player = 1  # X starts
    running = True
    ai_enabled = False
    ai_as = 2  # AI plays 'O' by default (second)
    winner = None
    winline = None

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = new_board()
                    current_player = 1
                    winner, winline = None, None
                elif event.key == pygame.K_a:
                    ai_enabled = not ai_enabled
                    board = new_board()
                    current_player = 1
                    winner, winline = None, None
                elif event.key == pygame.K_TAB:
                    ai_as = 1 if ai_as == 2 else 2
                    board = new_board()
                    current_player = 1
                    winner, winline = None, None

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and winner is None:
                mx, my = event.pos
                if my < WIDTH:
                    c = mx // CELL
                    r = my // CELL
                    if board[r][c] == 0:
                        board[r][c] = current_player
                        winner, winline = check_winner(board)
                        if winner is None:
                            current_player = 3 - current_player

        if ai_enabled and winner is None and current_player == ai_as:
            move = ai_move(board, ai_as, 3 - ai_as)
            if move is not None:
                r, c = move
                board[r][c] = ai_as
                winner, winline = check_winner(board)
                if winner is None:
                    current_player = 3 - current_player

        draw_grid()
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board[r][c] != 0:
                    draw_mark(r, c, board[r][c])

        if winner is not None and winline is not None:
            pygame.draw.line(screen, WINLINE, winline[0], winline[1], LINE_W)

        if winner is None:
            msg = f"Turn: {'X' if current_player==1 else 'O'}"
        else:
            if winner == 0:
                msg = "Draw!"
            else:
                msg = f"'{ 'X' if winner==1 else 'O' }' wins!"
        sub = "LMB to place • R=restart • A=toggle AI • TAB=AI plays X/O"
        if ai_enabled:
            sub += f" • AI: {'X' if ai_as==1 else 'O'}"
        draw_status_bar(msg, sub)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
