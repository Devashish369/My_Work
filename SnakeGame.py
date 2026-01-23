import pygame
import random
import os
import sys

pygame.init()
pygame.mixer.init()

# ================= CONFIG =================
WIDTH, HEIGHT = 640, 640
CELL = 20
FPS = 60

# ================= COLORS / THEMES =================
THEMES = [
    {"bg": (15, 20, 40), "snake": (0, 220, 140), "food": (255, 80, 120)},
    {"bg": (0, 0, 0), "snake": (0, 255, 0), "food": (255, 0, 0)},
    {"bg": (10, 30, 50), "snake": (0, 200, 255), "food": (255, 200, 0)},
]

theme_id = 0

# ================= SCREEN =================
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game (Pygame Edition)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 28)
big_font = pygame.font.SysFont("consolas", 48)

# ================= SOUND =================
def load_sound(name):
    return pygame.mixer.Sound(name) if os.path.exists(name) else None

eat_sound = load_sound("eat.wav")
gameover_sound = load_sound("gameover.wav")

# ================= UTIL =================
def draw_text(text, font, color, x, y, center=True):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
    screen.blit(surf, rect)

def random_pos():
    return (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)
    )

# ================= SNAKE =================
class Snake:
    def __init__(self, x, y, color):
        self.body = [(x, y), (x, y + CELL), (x, y + CELL * 2)]
        self.dir = (0, -CELL)
        self.color = color

    def move(self, grow=False):
        head = (self.body[0][0] + self.dir[0], self.body[0][1] + self.dir[1])
        self.body.insert(0, head)
        if not grow:
            self.body.pop()

    def draw(self):
        for i, seg in enumerate(self.body):
            r = pygame.Rect(seg[0], seg[1], CELL, CELL)
            pygame.draw.rect(screen, self.color, r, border_radius=6)

    def collision(self):
        head = self.body[0]
        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in self.body[1:]
        ):
            return True
        return False

# ================= AI =================
def ai_direction(snake, food):
    hx, hy = snake.body[0]
    fx, fy = food

    options = [
        ((CELL, 0), abs(fx - (hx + CELL)) + abs(fy - hy)),
        ((-CELL, 0), abs(fx - (hx - CELL)) + abs(fy - hy)),
        ((0, CELL), abs(fy - (hy + CELL)) + abs(fx - hx)),
        ((0, -CELL), abs(fy - (hy - CELL)) + abs(fx - hx)),
    ]

    safe = []
    for d, dist in options:
        nx, ny = hx + d[0], hy + d[1]
        if (nx, ny) not in snake.body and 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
            safe.append((d, dist))

    if safe:
        return min(safe, key=lambda x: x[1])[0]
    return snake.dir

# ================= MENU =================
def menu():
    global theme_id
    while True:
        screen.fill((0, 0, 0))
        draw_text("SNAKE GAME", big_font, (255, 255, 255), WIDTH//2, 120)
        draw_text("1 - Single Player", font, (200, 200, 200), WIDTH//2, 240)
        draw_text("2 - AI Snake", font, (200, 200, 200), WIDTH//2, 280)
        draw_text("3 - Multiplayer", font, (200, 200, 200), WIDTH//2, 320)
        draw_text("T - Change Theme", font, (200, 200, 200), WIDTH//2, 360)
        draw_text("ESC - Quit", font, (200, 200, 200), WIDTH//2, 400)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1: return "SINGLE"
                if e.key == pygame.K_2: return "AI"
                if e.key == pygame.K_3: return "MULTI"
                if e.key == pygame.K_t:
                    theme_id = (theme_id + 1) % len(THEMES)
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

# ================= GAME =================
def game(mode):
    theme = THEMES[theme_id]
    snake1 = Snake(100, 100, theme["snake"])
    snake2 = Snake(400, 400, (0, 200, 255)) if mode == "MULTI" else None
    food = random_pos()
    score = 0
    speed_timer = 0

    while True:
        clock.tick(FPS)
        screen.fill(theme["bg"])

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_w: snake1.dir = (0, -CELL)
                if e.key == pygame.K_s: snake1.dir = (0, CELL)
                if e.key == pygame.K_a: snake1.dir = (-CELL, 0)
                if e.key == pygame.K_d: snake1.dir = (CELL, 0)

                if snake2:
                    if e.key == pygame.K_UP: snake2.dir = (0, -CELL)
                    if e.key == pygame.K_DOWN: snake2.dir = (0, CELL)
                    if e.key == pygame.K_LEFT: snake2.dir = (-CELL, 0)
                    if e.key == pygame.K_RIGHT: snake2.dir = (CELL, 0)

        # AI
        if mode == "AI":
            snake1.dir = ai_direction(snake1, food)

        speed_timer += 1
        if speed_timer % 8 == 0:
            grow = False
            if snake1.body[0] == food:
                food = random_pos()
                grow = True
                score += 10
                if eat_sound: eat_sound.play()

            snake1.move(grow)
            if snake1.collision():
                if gameover_sound: gameover_sound.play()
                return

            if snake2:
                snake2.move()
                if snake2.collision() or snake2.body[0] in snake1.body:
                    return

        # Draw
        pygame.draw.rect(screen, theme["food"], (*food, CELL, CELL), border_radius=6)
        snake1.draw()
        if snake2: snake2.draw()
        draw_text(f"Score: {score}", font, (255, 255, 255), 10, 10, center=False)
        pygame.display.flip()

# ================= MAIN =================
while True:
    mode = menu()
    game(mode)