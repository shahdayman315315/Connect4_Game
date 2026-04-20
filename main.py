import numpy as np
import pygame
import sys
import random

# --- الإعدادات والألوان ---
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2

# ألوان Material Design
COLOR_BG = (23, 32, 42)      
COLOR_BOARD = (44, 62, 80)   
COLOR_SLOT = (28, 40, 51)    
RED_MAIN = (231, 76, 60)     
YELLOW_MAIN = (241, 196, 15) 
WHITE = (236, 240, 241)

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 8)

# --- تهيئة الصوت (الفوز والخسارة فقط) ---
pygame.init()
pygame.mixer.init()

def load_sound(file):
    try:
        return pygame.mixer.Sound(file)
    except:
        return None

win_sfx = load_sound("win.wav")
lose_sfx = load_sound("lose.wav")

# --- دالات المنطق (Logic) ---
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0: return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if all(board[r, c+i] == piece for i in range(4)): return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if all(board[r+i, c] == piece for i in range(4)): return True
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if all(board[r+i, c+i] == piece for i in range(4)): return True
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i, c+i] == piece for i in range(4)): return True
    return False

# --- الـ AI (Minimax + Alpha-Beta) ---
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    if window.count(piece) == 4: score += 100
    elif window.count(piece) == 3 and window.count(0) == 1: score += 5
    elif window.count(piece) == 2 and window.count(0) == 2: score += 2
    if window.count(opp_piece) == 3 and window.count(0) == 1: score -= 40
    return score

def score_position(board, piece):
    score = 0
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    score += center_array.count(piece) * 3
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3): score += evaluate_window(row_array[c:c+4], piece)
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3): score += evaluate_window(col_array[r:r+4], piece)
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            score += evaluate_window([board[r+i][c+i] for i in range(4)], piece)
            score += evaluate_window([board[r+3-i][c+i] for i in range(4)], piece)
    return score

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]
    is_terminal = winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(valid_locations) == 0
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE): return (None, 10000000)
            if winning_move(board, PLAYER_PIECE): return (None, -10000000)
            return (None, 0)
        return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -np.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value: value, column = new_score, col
            alpha = max(alpha, value)
            if alpha >= beta: break
        return column, value
    else:
        value = np.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value: value, column = new_score, col
            beta = min(beta, value)
            if alpha >= beta: break
        return column, value

# --- واجهة المستخدم (UI) ---
def draw_piece(screen, color_main, color_light, center):
    pygame.draw.circle(screen, (10, 10, 10), (center[0] + 2, center[1] + 2), RADIUS) 
    pygame.draw.circle(screen, color_main, center, RADIUS)
    pygame.draw.circle(screen, color_light, (center[0] - RADIUS//3, center[1] - RADIUS//3), RADIUS//3) 

def draw_board(board, screen):
    screen.fill(COLOR_BG)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, COLOR_BOARD, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, COLOR_SLOT, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            px, py = int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)
            if board[r][c] == PLAYER_PIECE: draw_piece(screen, RED_MAIN, (255,150,150), (px, py))
            elif board[r][c] == AI_PIECE: draw_piece(screen, YELLOW_MAIN, (255,255,180), (px, py))
    pygame.display.update()

def game_menu():
    title_font = pygame.font.SysFont("Segoe UI", 70, bold=True)
    btn_font = pygame.font.SysFont("Segoe UI", 35, bold=True)
    
    while True:
        screen.fill(COLOR_BG)
        title = title_font.render("CONNECT 4", 1, WHITE)
        screen.blit(title, (width//2 - 170, 100))
        subtitle = btn_font.render("Select Difficulty", 1, (127, 140, 141))
        screen.blit(subtitle, (width//2 - 110, 180))

        easy_rect = pygame.Rect(width//2-125, 280, 250, 70)
        med_rect = pygame.Rect(width//2-125, 380, 250, 70)
        hard_rect = pygame.Rect(width//2-125, 480, 250, 70)

        mouse_pos = pygame.mouse.get_pos()
        for rect, color, text in [(easy_rect, (46, 204, 113), "EASY"), 
                                  (med_rect, (241, 196, 15), "MEDIUM"), 
                                  (hard_rect, (231, 76, 60), "HARD")]:
            current_color = (min(color[0]+30, 255), min(color[1]+30, 255), min(color[2]+30, 255)) if rect.collidepoint(mouse_pos) else color
            pygame.draw.rect(screen, current_color, rect, border_radius=15)
            txt_surface = btn_font.render(text, 1, COLOR_BG)
            screen.blit(txt_surface, (rect.x + (rect.width//2 - txt_surface.get_width()//2), rect.y + 15))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos): return 1
                if med_rect.collidepoint(event.pos): return 3
                if hard_rect.collidepoint(event.pos): return 5

# --- التشغيل الرئيسي ---
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 - AI Pro")
myfont = pygame.font.SysFont("Segoe UI", 80, bold=True)

DIFFICULTY = game_menu()

board = create_board()
draw_board(board, screen)
game_over = False
turn = PLAYER

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, COLOR_BG, (0, 0, width, SQUARESIZE))
            if turn == PLAYER: draw_piece(screen, RED_MAIN, (255,150,150), (event.pos[0], SQUARESIZE//2))
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER:
            col = event.pos[0] // SQUARESIZE
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                draw_board(board, screen)
                
                if winning_move(board, PLAYER_PIECE):
                    if win_sfx: win_sfx.play()
                    label = myfont.render("YOU WIN!", 1, RED_MAIN)
                    screen.blit(label, (width//2 - 160, 10))
                    game_over = True
                turn = AI

    if turn == AI and not game_over:
        col, _ = minimax(board, DIFFICULTY, -np.inf, np.inf, True)
        if is_valid_location(board, col):
            pygame.time.wait(400)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            draw_board(board, screen)
            if winning_move(board, AI_PIECE):
                if lose_sfx: lose_sfx.play()
                label = myfont.render("AI WINS!", 1, YELLOW_MAIN)
                screen.blit(label, (width//2 - 140, 10))
                game_over = True
            turn = PLAYER

    if game_over:
        pygame.display.update()
        pygame.time.wait(3000)