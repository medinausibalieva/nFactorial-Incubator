import pygame
import itertools
import ctypes
import random
from enum import Enum

class RPSType(Enum):
    Paper = "./img/paper.png"
    Scissors = "./img/scissor.png"
    Rock = "./img/rock.png"

class Window():
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.left = 0
        self.right = width
        self.top = 0
        self.bot = heigth
    
    def getTupel(self):
        return (self.width, self.heigth)
        
class RPSCircle(pygame.sprite.Sprite):
    def __init__(self, type: RPSType, startpos, velocity, startdir, width = 70):
        super().__init__()
        self.type = type
        self.pos = pygame.math.Vector2(startpos)
        self.velocity = velocity
        self.dir = pygame.math.Vector2(startdir).normalize()
        self.image = pygame.transform.scale(
            pygame.image.load(self.type.value).convert_alpha(), (width, width))
        self.rect = self.image.get_rect(
            center = (round(self.pos.x), round(self.pos.y)))
        self.radius = width/2
        self.width = width

    def reflect(self, NV):
        self.dir = self.dir.reflect(pygame.math.Vector2(NV))
    
    def get_name(self):
        return str(self.type.name)

    def load_image(self):
        self.image = pygame.transform.scale(
            pygame.image.load(self.type.value).convert_alpha(), (self.width, self.width))

    def update(self):
        self.pos += self.dir * self.velocity
        self.rect.center = round(self.pos.x), round(self.pos.y)

    def wincheck(self, other):
        if self.type == RPSType.Paper:
            if other.type == RPSType.Scissors:
                self.type = RPSType.Scissors
                self.load_image()
        elif self.type == RPSType.Scissors:
            if other.type == RPSType.Rock:
                self.type = RPSType.Rock
                self.load_image()
        elif self.type == RPSType.Rock:
            if other.type == RPSType.Paper:
                self.type = RPSType.Paper
                self.load_image()

    def reflect_if_collided(self, window_size: Window):
        if self.rect.left <= window_size.left:
            self.reflect((1, 0))
        if self.rect.right >= window_size.right:
            self.reflect((-1, 0))
        if self.rect.top <= window_size.top:
            self.reflect((0, 1))
        if self.rect.bottom >= window_size.bot:
            self.reflect((0, -1))
#     def die_if_killed(self, other_circles: list):
#         for circle in other_circles:
#             if self.pos.distance_to(circle.pos) < self.radius + circle.radius -2:
#                 new_vector = circle.dir - self.dir
#                 self.wincheck(circle)    
                
def find_collisions(sprites: pygame.sprite.Group):
    for a, b in itertools.permutations(sprites, 2):
        if a.pos.distance_to(b.pos) < a.radius + b.radius -2:
                 a.wincheck(b)


def reflectBalls(ball_1, ball_2):
    v1 = pygame.math.Vector2(ball_1.rect.center)
    v2 = pygame.math.Vector2(ball_2.rect.center)
    r1 = ball_1.rect.width // 2
    r2 = ball_2.rect.width // 2
    d = v1.distance_to(v2)
    if d < r1 + r2 - 2:
        ball_1.wincheck(ball_2)
        dnext = (v1 + ball_1.dir).distance_to(v2 + ball_2.dir)
        nv = v2 - v1
        if dnext < d and nv.length() > 0:
            ball_1.dir = ball_1.dir.reflect(nv)
            ball_2.dir = ball_2.dir.reflect(nv)

def window_collisions(group: pygame.sprite.Group, window_size):
    [sprite.reflect_if_collided(window_size) for sprite in group]
    

def go():
    ws = Window(800, 800)  

    pygame.init()
    pygame.display.set_caption("Rock-Paper-Scissors")
    window = pygame.display.set_mode(ws.getTupel())  # Update method name to getTupel()
    clock = pygame.time.Clock()

    all_groups = pygame.sprite.Group()

    rps_types = [RPSType.Paper, RPSType.Scissors, RPSType.Rock]

    # Generate a random number of objects for each type
    for rps_type in rps_types:
        num_objects = random.randint(3, 10)  # Random number between 3 and 10
        for _ in range(num_objects):
            x = random.randint(0, ws.width)
            y = random.randint(0, ws.heigth)  # Fix attribute name to heigth
            velocity = random.uniform(1, 5)
            startdir = (random.random(), random.random())

            rps_object = RPSCircle(rps_type, (x, y), velocity, startdir)
            all_groups.add(rps_object)

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        all_groups.update()

        window.fill((144, 144, 144))
        all_groups.draw(window)

        window_collisions(all_groups, ws)

        for a, b in itertools.permutations(all_groups, 2):
            reflectBalls(a, b)

        if all(sprite.type.name == all_groups.sprites()[0].type.name for sprite in all_groups):
            winner = all_groups.sprites()[0].type.name
            ctypes.windll.user32.MessageBoxW(0, winner + " won!", "Winner: " + winner, 0)
            pygame.display.quit()
            pygame.quit()
            quit()
        pygame.display.flip()

