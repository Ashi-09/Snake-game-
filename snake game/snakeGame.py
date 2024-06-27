# GAME SCREEN SETUP #
import pygame, sys, random
from pygame.math import Vector2
pygame.init()   # initializing pygame

# FONT #
title_font = pygame.font.Font(None, 40)
title_font_score = pygame.font.Font(None, 40)
title_font_end = pygame.font.Font(None, size= 10)


# COLORS #
blue = (179, 217, 255)
darkblue = (26, 117, 255)
midblue = (126, 161, 255)
red = (204, 0, 0)

# CREATING GRID #
OFFSET = 50
cell_size = 30
number_of_cells = 20
icon = pygame.image.load('icon.png') # game icon
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((2*OFFSET + cell_size*number_of_cells,2*OFFSET + cell_size*number_of_cells)) # length and width of game screen
pygame.display.set_caption('SNAKE GAME') # Title of our game
clock = pygame.time.Clock() # detemine the framerate or the speed of our game

# CREATING BACKGROUND #
class Back:
    def __init__(self):
        self.position = Vector2(4,5)
    
    def draw(self):
        bg_rect = pygame.Rect(self.position.x*cell_size + 100, self.position.y*cell_size, cell_size, cell_size)
        screen.blit(bg_surface,bg_rect)

# bg = Back()
bg_surface = pygame.image.load('rainbow.png')
# bg.draw()
# CREATING FOOD #
class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)
        
    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x*cell_size, OFFSET + self.position.y*cell_size, cell_size, cell_size)
        # pygame.draw.rect(screen,red,food_rect)
        screen.blit(food_surface,food_rect)
    
    def generate_random_cell(self):
        x = random.randint(0,number_of_cells-1)
        y = random.randint(0,number_of_cells-1)
        return Vector2(x,y)
        
    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()

        return position

# food = Food()
food_surface = pygame.image.load('candy.png')

# CREATING SNAKE #
class Snake:
    def __init__(self):
        self.body = [Vector2(6,9),Vector2(5,9)]
        self.direction = Vector2(1,0)
        self.add_segment = False
        self.eat = pygame.mixer.Sound('point.wav')
        self.dead = pygame.mixer.Sound('gameover.mp3')

    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x*cell_size, OFFSET + segment.y*cell_size,cell_size,cell_size)
            pygame.draw.rect(screen, darkblue, segment_rect, 0, 10) # last 0 to fill color and 10 to make rectangle radius

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]
    
    def reset(self):
        self.body = [Vector2(6,9),Vector2(5,9)]
        self.direction = Vector2(1,0)

# snake = Snake()

# CREATIG GAME #
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.bg = Back()
        self.state = 'GAME ON'
        self.score = 0
    
    def draw(self):
        self.snake.draw()
        self.food.draw()
        self.bg.draw()
    
    def update(self):
        if self.state == 'GAME ON':
            self.snake.update()
            self.check_food()
            self.check_walls()
            self.check_snake()

    def check_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            self.snake.eat.play()
    
    def check_walls(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()
    
    def check_snake(self):
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = 'GAME OVER'
        self.score = 0
        self.snake.dead.play()

game = Game()

# DETERMINING SPEED OF THE SNAKE #

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE,200) # event to be triggerded and after how many miliseconds

# GAME LOOP #

while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
        
        if event.type == pygame.KEYDOWN: # means that the player has pressed a key
            if game.state == 'GAME OVER':
                game.state = "GAME ON"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0,1):
                game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0,-1):
                game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1,0):
                game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1,0):
                game.snake.direction = Vector2(-1,0)



    screen.fill(blue)
    # food.draw()
    # snake.draw()
    pygame.draw.rect(screen, midblue, (OFFSET-5, OFFSET-5, cell_size*number_of_cells + 5, cell_size*number_of_cells + 5) ,5)
    game.draw()
    title_surface = title_font.render('SNAKE GAME', True, midblue)
    score_surface = title_font.render(str(game.score), True, midblue)
    title_surface_end = title_font.render('MADE BY - ADITY SHUKLA', True, midblue)
    screen.blit(title_surface, (OFFSET-10,10))
    screen.blit(score_surface, (OFFSET-10 + cell_size*number_of_cells,OFFSET - 30))
    screen.blit(title_surface_end, (number_of_cells*cell_size - 315,number_of_cells*cell_size + 60))
    pygame.display.update()
    clock.tick(60) # this while loop will run 60 times every second
