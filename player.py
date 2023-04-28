import math, pygame
from ray import Ray

GRID_SIZE = 64

class Player:

    def __init__(self, screen, board, start_pos, start_dir):
        self.pos = start_pos
        self.board = board
        self.dir = start_dir
        self.velocity = 2.2
        self.rotation_velocity = math.pi / 120
        self.screen = screen
        self.control = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False
        }
        self.rays = []

    def draw(self):
        # print(self.dir)
        pygame.draw.circle(self.screen, (255, 255, 255), self.pos, 10)
        # pygame.draw.line(self.screen, (255, 255,255), self.pos, (self.pos[0] + 30 * math.cos(self.dir), self.pos[1] + 30 * math.sin(self.dir)))
        for ray in self.rays:
            ray.draw()

    def add_rays(self):
        tmp = []
        FOV = math.pi / 3
        SCREEN_WIDTH = 800

        # for i in range(SCREEN_WIDTH // 2, 1, -0.2):
        i = SCREEN_WIDTH // 2
        while i > 1:
            offset = -i / (SCREEN_WIDTH // 2) * (FOV / 2)

            tmp.append(Ray(self.screen, self.board, self.pos, self.dir + offset, offset))
            i -= 1

        tmp.append(Ray(self.screen, self.board, self.pos, self.dir, 0))

        i = 1
        while i < SCREEN_WIDTH // 2:
            offset = i / (SCREEN_WIDTH // 2) * (FOV / 2)
            print(offset)
            tmp.append(Ray(self.screen, self.board, self.pos, self.dir + offset, offset))
            i += 1

        self.rays = tmp
        # self.rays = [Ray(self.screen, self.board, self.pos, self.dir - FOV / 2, FOV / 2), Ray(self.screen, self.board, self.pos, self.dir, 0), Ray(self.screen, self.board, self.pos, self.dir + FOV / 2, FOV / 2)]

    def forward(self, state):
        self.control['forward'] = state

    def backward(self, state):
        self.control['backward'] = state
    
    def turn_left(self, state):
        self.control['left'] = state
    
    def turn_right(self, state):
        self.control['right'] = state
        

    def move(self):
        if self.control['forward']:
            next_x = self.pos[0] + math.cos(self.dir) * self.velocity
            next_y = self.pos[1] + math.sin(self.dir) * self.velocity
            if self.board[int(self.pos[1] / GRID_SIZE)][int(next_x / GRID_SIZE)] == 0:
                self.pos[0] = next_x
            if self.board[int(next_y / GRID_SIZE)][int(self.pos[0] / GRID_SIZE)] == 0:
                self.pos[1] = next_y

        if self.control['backward']:
            # self.pos[0] -= math.cos(self.dir) * self.velocity
            # self.pos[1] -= math.sin(self.dir) * self.velocity
            next_x = self.pos[0] - math.cos(self.dir) * self.velocity
            next_y = self.pos[1] - math.sin(self.dir) * self.velocity
            if self.board[int(self.pos[1] / GRID_SIZE)][int(next_x / GRID_SIZE)] == 0:
                self.pos[0] = next_x
            if self.board[int(next_y / GRID_SIZE)][int(self.pos[0] / GRID_SIZE)] == 0:
                self.pos[1] = next_y
        
        if self.control['left']:
            self.dir -= self.rotation_velocity

        if self.control['right']:
            self.dir += self.rotation_velocity

        if abs(self.dir) > 2 * math.pi:
            self.dir = 0

        self.add_rays()
        for ray in self.rays:
            ray.line_check()

        # print(self.dir * 180 / math.pi)
        # print(f'({self.pos[0] // 64},{self.pos[1] // 64})')