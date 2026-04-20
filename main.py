import numpy as np
import pygame
import sys
import random


ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2

# تعريف الألوان
BLUE = (0, 0, 255)    # لون اللوحة البلاستيك 🔵
BLACK = (0, 0, 0)     # لون الفراغات (الخلفية) ⚫
RED = (255, 0, 0)     # لون قرص اللاعب الأول 🔴
YELLOW = (255, 255, 0) # لون قرص اللاعب الثاني (الكمبيوتر) 🟡
# ألوان بروفيشنال (Material UI Palette)
WHITE = (236, 240, 241)      # أبيض كريمي للنصوص
BG_COLOR = (34, 47, 62)      # كحلي غامق جداً للخلفية
BOARD_COLOR = (52, 73, 94)   # رمادي مزرق للوحة
RED_PIECE = (238, 82, 83)    # أحمر "برياني" هادي
YELLOW_PIECE = (255, 159, 67) # برتقالي ذهبي
SHADOW = (29, 209, 161, 100) # لون للظلال (اختياري)


# مقاسات الرسم
SQUARESIZE = 100 # كل خانة عبارة عن مربع 100x100 بكسل
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE # زودنا صف فوق عشان حركة الماوس
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5) # نصف قطر الدائرة عشان تسيب مسافة بسيطة بين الدوائر

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# 1. دالة التأكد من صحة العمود: بتشوف هل العمود لسه فيه مكان ولا مليان؟
def is_valid_location(board, col):
    # لو الصف اللي فوق خالص (رقم 5 في المصفوفة المقلوبة) لسه 0، يبقى فيه مكان
    return board[ROW_COUNT-1][col] == 0

# 2. دالة البحث عن أول صف فاضي: بتمشي من تحت لفوق
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# 3. دالة وضع القطعة: بتغير الـ 0 لرقم اللاعب (1 أو 2)
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# 4. دالة عكس اللوحة: عشان لما نطبعها تظهر الصفوف اللي تحت هي اللي تحت فعلاً
def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # 1. التحقق من الفوز الأفقي
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # 2. التحقق من الفوز الرأسي
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # 3. التحقق من الفوز القطري (المائل لليمين)
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # 4. التحقق من الفوز القطري (المائل لليسار)
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
            

# ألوان مودرن
BG_COLOR = (44, 62, 80)      # رمادي مزرق غامق
BOARD_COLOR = (52, 152, 219) # أزرق فاتح "Clean"
RED_PIECE = (231, 76, 60)    # أحمر هادي
YELLOW_PIECE = (241, 196, 15) # أصفر ذهبي

def draw_board(board, screen):
    screen.fill(BG_COLOR) # تلوين الخلفية
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # رسم مستطيلات اللوحة (الجسم الأساسي)
            pygame.draw.rect(screen, BOARD_COLOR, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            
            # رسم "الفتحات" بشكل يخليها تبان غويطة (Inner Shadow)
            pygame.draw.circle(screen, (44, 62, 80), (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pos_x = int(c * SQUARESIZE + SQUARESIZE / 2)
            pos_y = height - int(r * SQUARESIZE + SQUARESIZE / 2)
            
            if board[r][c] == 1: # قطعة اللاعب 1
                # الدائرة الأساسية
                pygame.draw.circle(screen, RED_PIECE, (pos_x, pos_y), RADIUS)
                # لمعة الإضاءة (Reflection) عشان تبان 3D
                pygame.draw.circle(screen, (255, 120, 120), (pos_x - 12, pos_y - 12), RADIUS // 3)
                
            elif board[r][c] == 2: # قطعة اللاعب 2
                pygame.draw.circle(screen, YELLOW_PIECE, (pos_x, pos_y), RADIUS)
                # لمعة الإضاءة
                pygame.draw.circle(screen, (255, 200, 100), (pos_x - 12, pos_y - 12), RADIUS // 3)
    
    pygame.display.update()



def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4
    return score

def score_position(board, piece):
    score = 0
    # تمييز العمود الأوسط لأنه يفتح احتمالات أكثر
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # تقييم الصفوف والأعمدة والأقطار
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    return score

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE): return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE): return (None, -10000000)
            else: return (None, 0)
        else: return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -np.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta: break
        return column, value
    else:
        value = np.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta: break
        return column, value
    # --- تشغيل اللعبة ---

# 1. تهيئة مكتبة Pygame
pygame.init()

# 2. إنشاء الشاشة
screen = pygame.display.set_mode(size)
board = create_board()
print_board(board)
game_over = False
turn = 0 # اللاعب 1 يبدأ الأول

# 3. رسم اللوحة لأول مرة
draw_board(board, screen)

# 4. حلقة اللعبة الأساسية (بتفضل شغالة لحد ما حد يخسر أو نقفل البرنامج)
# --- قبل الـ Loop نجهز الخط ---
pygame.font.init()
myfont = pygame.font.SysFont("monospace", 75, bold=True)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BG_COLOR, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED_PIECE, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BG_COLOR, (0, 0, width, SQUARESIZE))
            
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        # رسم النص وتحديث الشاشة فوراً
                        label = myfont.render("YOU WIN!! 🏆", 1, RED_PIECE)
                        screen.blit(label, (40, 10))
                        game_over = True

                    draw_board(board, screen) # تحديث اللوحة
                    turn = (turn + 1) % 2

    # دور الـ AI
    if turn == AI and not game_over:
        col, minimax_score = minimax(board, 4, -np.inf, np.inf, True)

        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                # رسم النص وتحديث الشاشة فوراً
                label = myfont.render("AI WINS! 🤖", 1, YELLOW_PIECE)
                screen.blit(label, (40, 10))
                game_over = True

            draw_board(board, screen) # تحديث اللوحة
            turn = (turn + 1) % 2

    # --- الجزء اللي كان فيه المشكلة ---
    if game_over:
        # أهم سطر: بنعيد رسم النص فوق اللوحة النهائية ونحدث الشاشة
        if winning_move(board, PLAYER_PIECE):
            label = myfont.render("YOU WIN!! 🏆", 1, RED_PIECE)
        else:
            label = myfont.render("AI WINS! 🤖", 1, YELLOW_PIECE)
        
        screen.blit(label, (40, 10))
        pygame.display.update() # إظهار النص فوراً
        
        pygame.time.wait(2000) # استراحة قصيرة
        
        # حلقة الانتظار عشان البرنامج ميهنجش ويفضل عارض النتيجة
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()