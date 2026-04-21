import numpy as np
import pygame
import sys
import random

# --- الإعدادات والألوان (ثوابت) ---
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2

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

class Connect4Problem:
    """ Problem Formulation Class """
    def __init__(self):
        self.initial_state = np.zeros((ROW_COUNT, COLUMN_COUNT))

    def get_actions(self, board):
        """-- Actions--> العواميد اللي لسه فيها مكان فاضي"""
        return [c for c in range(COLUMN_COUNT) if board[ROW_COUNT-1][c] == 0]

    def get_result(self, board, col, piece):
        """ -- Successor Function (Transition Model)--> شكل اللوحة الجديد بعد الحركة"""
        new_board = board.copy()
        row = self.get_next_open_row(new_board, col)
        new_board[row][col] = piece  # Drop the ball in place
        return new_board

    def goal_test(self, board, piece):
        """-- Goal Test --> هل الحركة دي وصلت حالة الفوز؟"""
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if all(board[r, c+i] == piece for i in range(4)): return True
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if all(board[r+i, c] == piece for i in range(4)): return True
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if all(board[r+i, c+i] == piece for i in range(4)): return True
            for r in range(3, ROW_COUNT):
                if all(board[r-i, c+i] == piece for i in range(4)): return True
        return False

    def get_next_open_row(self, board, col):
        """دالة مساعدة لإيجاد أول صف فاضي في العمود"""
        for r in range(ROW_COUNT):
            if board[r][col] == 0: return r

class Connect4AI:
    """كلاس الذكاء الاصطناعي (Agent)"""
    def __init__(self, problem):
        self.problem = problem # AI بالـ Problem Formulation ربط الـ 

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
        if window.count(piece) == 4: score += 100
        elif window.count(piece) == 3 and window.count(0) == 1: score += 5
        elif window.count(piece) == 2 and window.count(0) == 2: score += 2
        if window.count(opp_piece) == 3 and window.count(0) == 1: score -= 40
        return score

    def score_position(self, board, piece):
        score = 0
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
        score += center_array.count(piece) * 3
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(COLUMN_COUNT-3): score += self.evaluate_window(row_array[c:c+4], piece)
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(ROW_COUNT-3): score += self.evaluate_window(col_array[r:r+4], piece)
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                score += self.evaluate_window([board[r+i][c+i] for i in range(4)], piece)
                score += self.evaluate_window([board[r+3-i][c+i] for i in range(4)], piece)
        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.problem.get_actions(board)
        is_terminal = self.problem.goal_test(board, PLAYER_PIECE) or \
                      self.problem.goal_test(board, AI_PIECE) or \
                      len(valid_locations) == 0
        
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.problem.goal_test(board, AI_PIECE): return (None, 10000000)
                if self.problem.goal_test(board, PLAYER_PIECE): return (None, -10000000)
                return (None, 0)
            return (None, self.score_position(board, AI_PIECE))

        if maximizingPlayer:
            value = -np.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = self.problem.get_result(board, col, AI_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value: value, column = new_score, col
                alpha = max(alpha, value)
                if alpha >= beta: break
            return column, value
        else:
            value = np.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = self.problem.get_result(board, col, PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value: value, column = new_score, col
                beta = min(beta, value)
                if alpha >= beta: break
            return column, value

class Connect4GUI:
    """كلاس الواجهة الرسومية والتحكم في اللعبة"""
    def __init__(self, problem, ai):
        pygame.init()
        pygame.mixer.init()
        self.problem = problem
        self.ai = ai
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Connect 4 - Professional AI")
        self.myfont = pygame.font.SysFont("Segoe UI", 80, bold=True)
        self.win_sfx = self.load_sound("win.wav")
        self.lose_sfx = self.load_sound("lose.wav")
        self.difficulty = 1

    def load_sound(self, file):
        try: return pygame.mixer.Sound(file)
        except: return None

    def draw_board(self, board):
        self.screen.fill(COLOR_BG)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.screen, COLOR_BOARD, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, COLOR_SLOT, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                px, py = int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)
                if board[r][c] == PLAYER_PIECE:
                    self._draw_circle(RED_MAIN, (255,150,150), (px, py))
                elif board[r][c] == AI_PIECE:
                    self._draw_circle(YELLOW_MAIN, (255,255,180), (px, py))
        pygame.display.update()

    def _draw_circle(self, main_color, light_color, center):
        pygame.draw.circle(self.screen, (10, 10, 10), (center[0] + 2, center[1] + 2), RADIUS) 
        pygame.draw.circle(self.screen, main_color, center, RADIUS)
        pygame.draw.circle(self.screen, light_color, (center[0] - RADIUS//3, center[1] - RADIUS//3), RADIUS//3)

    def game_menu(self):
        title_font = pygame.font.SysFont("Segoe UI", 70, bold=True)
        btn_font = pygame.font.SysFont("Segoe UI", 35, bold=True)
        while True:
            self.screen.fill(COLOR_BG)
            title = title_font.render("CONNECT 4", 1, WHITE)
            self.screen.blit(title, (width//2 - 170, 100))
            
            easy_rect = pygame.Rect(width//2-125, 280, 250, 70)
            med_rect = pygame.Rect(width//2-125, 380, 250, 70)
            hard_rect = pygame.Rect(width//2-125, 480, 250, 70)

            mouse_pos = pygame.mouse.get_pos()
            for rect, color, text in [(easy_rect, (46, 204, 113), "EASY"), 
                                      (med_rect, (241, 196, 15), "MEDIUM"), 
                                      (hard_rect, (231, 76, 60), "HARD")]:
                curr_c = (min(color[0]+30, 255), min(color[1]+30, 255), min(color[2]+30, 255)) if rect.collidepoint(mouse_pos) else color
                pygame.draw.rect(self.screen, curr_c, rect, border_radius=15)
                txt = btn_font.render(text, 1, COLOR_BG)
                self.screen.blit(txt, (rect.x + (rect.width//2 - txt.get_width()//2), rect.y + 15))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_rect.collidepoint(event.pos): return 1
                    if med_rect.collidepoint(event.pos): return 3
                    if hard_rect.collidepoint(event.pos): return 5

    def play(self):
        self.difficulty = self.game_menu()
        board = self.problem.initial_state
        self.draw_board(board)
        game_over = False
        turn = PLAYER

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, COLOR_BG, (0, 0, width, SQUARESIZE))
                    if turn == PLAYER:
                        self._draw_circle(RED_MAIN, (255,150,150), (event.pos[0], SQUARESIZE//2))
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER:
                    col = event.pos[0] // SQUARESIZE
                    if col in self.problem.get_actions(board):
                        board = self.problem.get_result(board, col, PLAYER_PIECE)
                        self.draw_board(board)
                        if self.problem.goal_test(board, PLAYER_PIECE):
                            if self.win_sfx: self.win_sfx.play()
                            msg = self.myfont.render("YOU WIN!", 1, RED_MAIN)
                            self.screen.blit(msg, (width//2 - 160, 10))
                            game_over = True
                        turn = AI

            if turn == AI and not game_over:
                col, _ = self.ai.minimax(board, self.difficulty, -np.inf, np.inf, True)
                pygame.time.wait(400)
                board = self.problem.get_result(board, col, AI_PIECE)
                self.draw_board(board)
                if self.problem.goal_test(board, AI_PIECE):
                    if self.lose_sfx: self.lose_sfx.play()
                    msg = self.myfont.render("AI WINS!", 1, YELLOW_MAIN)
                    self.screen.blit(msg, (width//2 - 140, 10))
                    game_over = True
                turn = PLAYER

            if game_over:
                pygame.display.update()
                pygame.time.wait(3000)

if __name__ == "__main__":
    problem = Connect4Problem()
    ai_agent = Connect4AI(problem)
    ui = Connect4GUI(problem, ai_agent)
    ui.play()