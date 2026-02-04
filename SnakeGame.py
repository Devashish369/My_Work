import pygame, random, sys, math

pygame.init()

# ================= CONFIG =================
WIDTH = HEIGHT = 640
CELL = 20
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Deluxe ✨")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 24)
big = pygame.font.SysFont("consolas", 48)

THEMES = [
    {"bg": (10, 15, 35), "snake": (0, 255, 180), "food": (255, 80, 120)},
    {"bg": (0, 0, 0), "snake": (0, 255, 0), "food": (255, 0, 0)}
]
theme = 0

# ================= UTILS =================
def rand_pos():
    return random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL)

# ================= PARTICLES =================
particles = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(80)]

def draw_particles():
    for p in particles:
        pygame.draw.circle(screen, (255, 255, 255), (p[0], p[1]), p[2])
        p[1] += .3
        if p[1] > HEIGHT: p[1] = 0

# ================= GLOW =================
def glow(x, y, w, h, c):
    s = pygame.Surface((w+20, h+20), pygame.SRCALPHA)
    pygame.draw.rect(s, (*c, 60), (0,0,w+20,h+20), border_radius=12)
    screen.blit(s, (x-10,y-10))

# ================= SNAKE =================
class Snake:
    def __init__(self,x,y,col):
        self.body=[(x,y),(x,y+CELL),(x,y+CELL*2)]
        self.dir=(0,-CELL)
        self.col=col

    def move(self,grow=False):
        h=(self.body[0][0]+self.dir[0],self.body[0][1]+self.dir[1])
        self.body.insert(0,h)
        if not grow:self.body.pop()

    def draw(self):
        for i,b in enumerate(self.body):
            fade=max(80,255-i*15)
            r=pygame.Rect(b[0],b[1],CELL,CELL)
            pygame.draw.rect(screen,(*self.col,fade),r,border_radius=8)

    def dead(self):
        h=self.body[0]
        return h[0]<0 or h[0]>=WIDTH or h[1]<0 or h[1]>=HEIGHT or h in self.body[1:]

# ================= AI =================
def ai(snake,food):
    hx,hy=snake.body[0]
    fx,fy=food
    dirs=[(CELL,0),(-CELL,0),(0,CELL),(0,-CELL)]
    best=snake.dir
    dmin=9999
    for d in dirs:
        nx,ny=hx+d[0],hy+d[1]
        if (nx,ny) in snake.body or nx<0 or ny<0 or nx>=WIDTH or ny>=HEIGHT:continue
        dist=abs(fx-nx)+abs(fy-ny)
        if dist<dmin:
            dmin=dist
            best=d
    return best

# ================= FADE =================
def fade(text):
    for a in range(0,255,6):
        t=big.render(text,1,(255,255,255))
        t.set_alpha(a)
        screen.blit(t,t.get_rect(center=(WIDTH//2,HEIGHT//2)))
        pygame.display.flip()
        clock.tick(60)

# ================= MENU =================
def menu():
    global theme
    while True:
        screen.fill((0,0,0))
        draw_particles()

        title=big.render("SNAKE DELUXE",1,(255,255,255))
        screen.blit(title,title.get_rect(center=(WIDTH//2,150)))

        opts=["1 - Single Player","2 - AI Mode","T - Change Theme","ESC - Quit"]
        y=260
        for o in opts:
            txt=font.render(o,1,(200,200,200))
            screen.blit(txt,txt.get_rect(center=(WIDTH//2,y)))
            y+=40

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_1:return"S"
                if e.key==pygame.K_2:return"A"
                if e.key==pygame.K_t:theme=(theme+1)%len(THEMES)
                if e.key==pygame.K_ESCAPE:pygame.quit();sys.exit()

# ================= GAME =================
def game(mode):
    th=THEMES[theme]
    snake=Snake(200,200,th["snake"])
    food=rand_pos()
    score=0
    shake=0

    while True:
        clock.tick(FPS)
        screen.fill(th["bg"])
        draw_particles()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_w:snake.dir=(0,-CELL)
                if e.key==pygame.K_s:snake.dir=(0,CELL)
                if e.key==pygame.K_a:snake.dir=(-CELL,0)
                if e.key==pygame.K_d:snake.dir=(CELL,0)
                if e.key==pygame.K_ESCAPE:return

        if mode=="A":
            snake.dir=ai(snake,food)

        grow=False
        if snake.body[0]==food:
            food=rand_pos()
            grow=True
            score+=10
            shake=5

        snake.move(grow)
        if snake.dead():
            fade("GAME OVER")
            return

        pulse=abs(math.sin(pygame.time.get_ticks()/200))*5
        glow(food[0]-pulse,food[1]-pulse,CELL+pulse*2,CELL+pulse*2,th["food"])
        pygame.draw.circle(screen,th["food"],(food[0]+CELL//2,food[1]+CELL//2),CELL//2+int(pulse))

        snake.draw()

        hud=pygame.Surface((150,40),pygame.SRCALPHA)
        pygame.draw.rect(hud,(0,0,0,160),(0,0,150,40),border_radius=12)
        screen.blit(hud,(10,10))
        screen.blit(font.render(f"Score {score}",1,(255,255,255)),(30,20))

        if shake:
            shake-=1
            screen.scroll(random.randint(-3,3),random.randint(-3,3))

        pygame.display.flip()

# ================= MAIN =================
while True:
    m=menu()
    game(m)
