import numpy as np
import pygame
import sys

# --- الإعدادات والألوان (نفس كودك بالظبط) ---
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_1 = 0
PLAYER_2 = 1
P1_PIECE = 1
P2_PIECE = 2

COLOR_BG = (23, 32, 42)      
COLOR_BOARD = (44, 62, 80)   
COLOR_SLOT = (28, 40, 51)    
RED_MAIN = (231, 76, 60)     
YELLOW_MAIN = (241, 196, 15) 
WHITE = (236, 240, 241)

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 8)

class Connect4Logic:
    """ (هذا الكلاس يجمع منطق اللعبة (اللوجيك """
    def __init__(self):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        self.turn = PLAYER_1
        self.game_over = False

    def is_valid_location(self, col):
        return self.board[ROW_COUNT-1][col] == 0

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0: return r

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def winning_move(self, piece):
        # نفس اللوجيك بتاعك للفحص في كل الاتجاهات
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if all(self.board[r, c+i] == piece for i in range(4)): return True
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if all(self.board[r+i, c] == piece for i in range(4)): return True
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if all(self.board[r+i, c+i] == piece for i in range(4)): return True
            for r in range(3, ROW_COUNT):
                if all(self.board[r-i, c+i] == piece for i in range(4)): return True
        return False

class Connect4GUI:
    """ Game Loopهذا الكلاس مسؤول عن الرسم والأصوات والـ """
    def __init__(self, logic):
        pygame.init()
        pygame.mixer.init()
        self.logic = logic
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Connect 4 - Naive Version")
        self.myfont = pygame.font.SysFont("Segoe UI", 80, bold=True)
        self.win_sfx = self.load_sound("win.wav")

    def load_sound(self, file):
        try: return pygame.mixer.Sound(file)
        except: return None

    def draw_piece(self, color_main, color_light, center):
        pygame.draw.circle(self.screen, (10, 10, 10), (center[0] + 2, center[1] + 2), RADIUS) 
        pygame.draw.circle(self.screen, color_main, center, RADIUS)
        pygame.draw.circle(self.screen, color_light, (center[0] - RADIUS//3, center[1] - RADIUS//3), RADIUS//3) 

    def draw_board(self):
        self.screen.fill(COLOR_BG)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.screen, COLOR_BOARD, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, COLOR_SLOT, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                px, py = int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)
                if self.logic.board[r][c] == P1_PIECE: self.draw_piece(RED_MAIN, (255,150,150), (px, py))
                elif self.logic.board[r][c] == P2_PIECE: self.draw_piece(YELLOW_MAIN, (255,255,180), (px, py))
        pygame.display.update()

    def play(self):
        self.draw_board()
        while not self.logic.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, COLOR_BG, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.logic.turn == PLAYER_1:
                        self.draw_piece(RED_MAIN, (255,150,150), (posx, int(SQUARESIZE/2)))
                    else:
                        self.draw_piece(YELLOW_MAIN, (255,255,180), (posx, int(SQUARESIZE/2)))
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // SQUARESIZE
                    
                    if self.logic.is_valid_location(col):
                        row = self.logic.get_next_open_row(col)
                        piece = P1_PIECE if self.logic.turn == PLAYER_1 else P2_PIECE
                        self.logic.drop_piece(row, col, piece)
                        self.draw_board()

                        if self.logic.winning_move(piece):
                            if self.win_sfx: self.win_sfx.play()
                            msg = "PLAYER 1 WINS!" if self.logic.turn == PLAYER_1 else "PLAYER 2 WINS!"
                            color = RED_MAIN if self.logic.turn == PLAYER_1 else YELLOW_MAIN
                            label = self.myfont.render(msg, 1, color)
                            self.screen.blit(label, (width//2 - 280, 10))
                            pygame.display.update()
                            self.logic.game_over = True
                            pygame.time.wait(3000)

                        self.logic.turn = (self.logic.turn + 1) % 2

# --- تشغيل اللعبة ---
if __name__ == "__main__":
    game_logic = Connect4Logic()
    Game = Connect4GUI(game_logic)
    Game.play()