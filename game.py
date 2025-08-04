import pygame
import random
from enum import Enum # for directions
from collections import namedtuple
import numpy as np
pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

'''
AI COMPONENTS TO ADD

Reset 
rewards
change play(action) to return a direction
game iteration
is collision
'''


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3 
    DOWN = 4
    
#Represents a position (x, y) on the screen.
Point = namedtuple('Point', 'x, y')


#These are RGB color codes used for the snake, food, background, etc.
# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 20

class SnakeGameAI:  
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        # reset the game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                        Point(self.head.x-BLOCK_SIZE, self.head.y),
                        Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food() 
        self.frame_iteration = 0
        # self._place_food() MODS a random int val w 20 ensureing the its one of the blocks and not in between blocks. and then multiplies with a block size to make it an actual pixel value
        # on the screen, ensuring that it does not overlap with the snake.    


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y) 
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self,action):

        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head) # add new head to the snake so the current list gets a new item at the front
        
        # 3. check if game over
        reward=0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10  # negative reward for collision
            return reward,game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward= 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        
        # 6. return game over and score
        return reward , game_over, self.score
    
    def is_collision(self,pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        


    #ACTION: This function takes an action as input and updates the snake's position based on the action.
    #[1,0,0] -> Straight (no change in direction)
    #[0,1,0] -> LEFT
    #[0,0,1] -> left

    def _move(self,action):

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)  # get the current direction index
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]   # no change in direction
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4    # turn ri
            new_dir = clock_wise[next_idx]
        elif np.array_equal(action, [0, 0, 1]):     # turn right
            next_idx = (idx - 1) % 4 #to ensure the values are always btw 1 to 4
            new_dir = clock_wise[next_idx]          

        self.direction = new_dir
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            

