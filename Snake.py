import pygame
import time
import random
from pygame.locals import *


SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,19)*SIZE

class Snake:
    def __init__(self, surface, length):
        self.parent_screen = surface
        self.block_origin = pygame.image.load("square.png").convert_alpha()
        self.block = pygame.transform.scale(self.block_origin, (40, 40))
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'
        self.length = length

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill((110, 110, 5))
        for i in range(len(self.x)):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move(self):
        for i in range(len(self.x)-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("蛇ゲーム")
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def play(self):
        self.snake.move()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        for i in range(len(self.snake.x)):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.snake.increase_length()
                self.apple.move()

        # snake colliding with itself
        for i in range(3, len(self.snake.x)):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game over"

        # snake hitting the boundaries
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            raise "Hit the boundary, game over"
        

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()

                    if event.key == pygame.K_RETURN:
                        pause = False


                    if not pause:
                        if event.key == pygame.K_UP:
                            self.snake.move_up()

                        if event.key == pygame.K_DOWN:
                            self.snake.move_down()

                        if event.key == pygame.K_LEFT:
                            self.snake.move_left()

                        if event.key == pygame.K_RIGHT:
                            self.snake.move_right()

                elif event.type == pygame.QUIT:
                    running = False
            try:
                if not pause:
                    self.play()

            except Exception as e:
                # this is for game over condition
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.2)

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('meiryo', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (180, 320))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (180, 370))
        pygame.display.flip()
        
    def display_score(self):
        font = pygame.font.SysFont('meiryo', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))
        
if __name__ == '__main__':
    game = Game()
    game.run()
