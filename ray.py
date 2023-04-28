import math, pygame, sys

GRID_SIZE = 64
MAP_WIDTH = 20
MAP_HEIGHT = 20

COLORS = [(200, 200, 200), (100, 100, 100), (100, 200, 100), (100, 100, 200)]

class Ray:

    def __init__(self, screen, board, start, theta, angle_offset, color=(200,200,200)):
        self.screen = screen
        self.board = board
        self.p1 = start
        self.p2 = [-1, -1]
        self.angle_offset = angle_offset
        self.theta = -theta
        self.length = 0
        self.color = color

    def distance(self, x0, y0, x1, y1):
        return math.sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0))

    def line_check(self):
        d0 = sys.maxsize
        d1 = sys.maxsize
        alpha = math.tan(self.theta)
        potential_intersect = []
        color_scale = 1
        # Vertical grid check
        # Quadrants I and IV
        if abs(self.theta) < math.pi / 2 or abs(self.theta) > 3 * math.pi / 2:
            # print('theta:', self.theta, 'tan(theta)', math.tan(self.theta))
            x1 = (self.p1[0] // GRID_SIZE + 1) * GRID_SIZE
            # dy = (self.p1[0] - x1) * alpha
            y1 = self.p1[1] + (self.p1[0] - x1) * alpha
            dy = GRID_SIZE * alpha
            while y1 >= 0 and x1 >= 0 and int(y1 / GRID_SIZE) < MAP_HEIGHT and int(x1 / GRID_SIZE) < MAP_WIDTH and self.board[int(y1 / GRID_SIZE)][int(x1 / GRID_SIZE)] == 0:
                x1 += GRID_SIZE
                y1 -= dy
                # print('theta:', self.theta, 'tan(theta)', alpha, '(',x1 // GRID_SIZE,',',y1 // GRID_SIZE,')')

                # print(int(x1/GRID_SIZE), int(y1/GRID_SIZE))
                # print(self.board[int(y1 / GRID_SIZE)][int(x1 / GRID_SIZE)])
            # print(x1, y1)
            potential_intersect.append([x1, y1])
            d0 = self.distance(self.p1[0], self.p1[1], x1, y1)
            self.p2 = [x1, y1]

        # Quadrants II and III
        elif abs(self.theta) <= math.pi or abs(self.theta) < 3 * math.pi / 2:
            x1 = (self.p1[0] // GRID_SIZE) * GRID_SIZE
            dy = (self.p1[0] - x1) * alpha
            y1 = self.p1[1] + (self.p1[0] - x1) * alpha
            dy = GRID_SIZE * alpha

            while y1 >= 0 and x1 >= 0 and int(y1 / GRID_SIZE) < MAP_HEIGHT and int(x1 / GRID_SIZE) < MAP_WIDTH and self.board[int(y1 / GRID_SIZE)][int(x1 / GRID_SIZE) - 1] == 0:
                x1 -= GRID_SIZE
                y1 += dy
                # print('theta:', self.theta, 'tan(theta)', alpha, '(',x1 // GRID_SIZE,',',y1 // GRID_SIZE,')')

            potential_intersect.append([x1, y1])
            d0 = self.distance(self.p1[0], self.p1[1], x1, y1)
            self.p2 = [x1 - GRID_SIZE, y1]
        


        # Horizontal grid check
        # Quadrants I and II
        if (self.theta < math.pi and self.theta > 0) or (self.theta < -math.pi and self.theta > -2 * math.pi):
            y1 = (self.p1[1] // GRID_SIZE) * GRID_SIZE
            x1 = self.p1[0] + (self.p1[1] - y1) / alpha
            dx = GRID_SIZE / alpha
            while y1 >= 0 and x1 >= 0 and int(y1 / GRID_SIZE) < MAP_HEIGHT and int(x1 / GRID_SIZE) < MAP_WIDTH and self.board[int(y1 / GRID_SIZE) - 1][int(x1 / GRID_SIZE)] == 0:
                x1 += dx
                y1 -= GRID_SIZE


            d1 = self.distance(self.p1[0], self.p1[1], x1, y1)
            potential_intersect.append([x1, y1])
            if d1 < d0:
                self.p2 = [x1, y1 - GRID_SIZE]
                

        # Quadrants III and IV
        elif (self.theta > math.pi and self.theta < 2 * math.pi) or (self.theta < 0 and self.theta > -math.pi):
            y1 = (self.p1[1] // GRID_SIZE + 1) * GRID_SIZE
            x1 = self.p1[0] + (self.p1[1] - y1) / alpha
            dx = GRID_SIZE / alpha
            while y1 >= 0 and x1 >= 0 and int(y1 / GRID_SIZE) < MAP_HEIGHT and int(x1 / GRID_SIZE) < MAP_WIDTH and self.board[int(y1 / GRID_SIZE)][int(x1 / GRID_SIZE)] == 0:
                x1 -= dx
                y1 += GRID_SIZE

            d1 = self.distance(self.p1[0], self.p1[1], x1, y1)
            potential_intersect.append([x1, y1])
            if d1 < d0:
                self.p2 = [x1, y1]


        self.color = COLORS[self.board[int(self.p2[1] / GRID_SIZE)][int(self.p2[0] / GRID_SIZE)]]
        self.length = min(d0, d1) * math.cos(self.angle_offset)
        # self.length = min(d0, d1)
        # print(self.length)
        # self.length = min(d0, d1)

        # Fog and basic shading
        if d1 < d0:
            color_scale = 0.8
        # color_scale *= 0 / self.length
        self.color = tuple(min(max(i * color_scale, 0), 255) for i in self.color);
        # self.color = tuple((max(i - int(i * color_scale * self.length / 1600), 100) for i in self.color))


    def draw(self):
        pygame.draw.line(self.screen, self.color, self.p1, self.p2)