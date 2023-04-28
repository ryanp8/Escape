import sys, pygame, math
from player import Player

GRID_SIZE = 64
MAP_WIDTH = 20
MAP_HEIGHT = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 720
MID_SCREEN = SCREEN_HEIGHT / 2

pygame.init()
screen2d = pygame.display.set_mode((GRID_SIZE * MAP_WIDTH, GRID_SIZE * MAP_HEIGHT))
screen3d = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

board = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

print(board[9][6])

p1 = Player(screen2d, board, [GRID_SIZE + 5, GRID_SIZE + 5], 0)
p1.add_rays()
for ray in p1.rays:
    ray.line_check()
# print([ray.length for ray in p1.rays])
print([ray.length for ray in p1.rays[len(p1.rays) // 2 - 10:len(p1.rays) // 2 + 10]])

# print(p1.rays[0].length, p1.rays[-1].length)

def draw_board():

    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col:
                pygame.draw.rect(screen2d, (100, 100, 100), (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    for i in range(0, MAP_WIDTH):
        x = i * GRID_SIZE
        pygame.draw.line(screen2d, (150, 150, 150), (x, 0), (x, MAP_HEIGHT * GRID_SIZE))

    for i in range(0, MAP_HEIGHT):
        y = i * GRID_SIZE
        pygame.draw.line(screen2d, (150, 150, 150), (0, y), (MAP_WIDTH * GRID_SIZE, y))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_w:
                p1.forward(True)
            if event.key== pygame.K_s:
                p1.backward(True)
            if event.key== pygame.K_a:
                p1.turn_left(True)
            if event.key== pygame.K_d:
                p1.turn_right(True)

        if event.type == pygame.KEYUP:
            if event.key== pygame.K_w:
                p1.forward(False)
            if event.key== pygame.K_s:
                p1.backward(False)
            if event.key== pygame.K_a:
                p1.turn_left(False)
            if event.key== pygame.K_d:
                p1.turn_right(False)
                
    p1.move()
    
    # screen2d.fill(0)
    # draw_board()
    # p1.draw()
    # screen3d.fill(0)
    pygame.draw.rect(screen3d, (101, 159, 252), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    # pygame.draw.rect(screen3d, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2))

    pygame.draw.rect(screen3d, (153, 119, 84), (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    rays = p1.rays
    for x, ray in enumerate(rays):
        line_len = 60 * SCREEN_HEIGHT / ray.length
        pygame.draw.line(screen3d, ray.color, (x, MID_SCREEN - line_len / 2), (x, MID_SCREEN + line_len / 2))

    pygame.display.update();