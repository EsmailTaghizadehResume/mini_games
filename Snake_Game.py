import pygame
import random
import tkinter as tk

# Set up the game window
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the font for the score display
SCORE_FONT = ('times', 24)

# Set up the Snake class
class Snake:
    def __init__(self, x=250, y=250):
        self.body = [(x, y)]
        self.direction = 'right'
        self.score = 0

    def move(self):
        x, y = self.body[0]
        if self.direction == 'right':
            x += 10
        elif self.direction == 'left':
            x -= 10
        elif self.direction == 'up':
            y -= 10
        elif self.direction == 'down':
            y += 10
        self.body.insert(0, (x, y))
        self.body.pop()

    def change_direction(self, direction):
        if direction == 'right':
            if self.direction != 'left':
                self.direction = 'right'
        elif direction == 'left':
            if self.direction != 'right':
                self.direction = 'left'
        elif direction == 'up':
            if self.direction != 'down':
                self.direction = 'up'
        elif direction == 'down':
            if self.direction != 'up':
                self.direction = 'down'

    def grow(self):
        x, y = self.body[0]
        if self.direction == 'right':
            x += 10
        elif self.direction == 'left':
            x -= 10
        elif self.direction == 'up':
            y -= 10
        elif self.direction == 'down':
            y += 10
        self.body.insert(0, (x, y))
        self.score += 10

    def draw(self):
        for x, y in self.body:
            pygame.draw.rect(WINDOW, GREEN, (x, y, 10, 10))

    def check_collision(self):
        x, y = self.body[0]
        if x < 0 or x > WINDOW_WIDTH - 10 or y < 0 or y > WINDOW_HEIGHT - 10:
            return True
        for i in range(1, len(self.body)):
            if x == self.body[i][0] and y == self.body[i][1]:
                return True
        return False

# Set up the Food class
class Food:
    def __init__(self):
        self.x, self.y = self.generate_position()

    def generate_position(self):
        x = random.randint(0, WINDOW_WIDTH - 10)
        y = random.randint(0, WINDOW_HEIGHT - 10)
        return x - x % 10, y - y % 10

    def draw(self):
        pygame.draw.rect(WINDOW, RED, (self.x, self.y, 10, 10))

    def check_collision(self, snake):
        x, y = snake.body[0]
        if self.x <= x <= self.x + 10 and self.y <= y <= self.y + 10:
            self.x, self.y = self.generate_position()
            return True
        return False

# Set up the Tkinter window for the score and high score display
class ScoreBoard:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.create_scoreboard()

    def create_scoreboard(self):
        self.root = tk.Tk()
        self.root.title('Score')
        self.score_var = tk.StringVar()
        self.score_var.set('Score: 0')
        self.score_label = tk.Label(self.root, textvariable=self.score_var, font=SCORE_FONT)
        self.score_label.pack()
        self.high_score_var = tk.StringVar()
        self.high_score_var.set('High Score: 0')
        self.high_score_label = tk.Label(self.root, textvariable=self.high_score_var, font=SCORE_FONT)
        self.high_score_label.pack()

    def update_score(self, score):
        self.score = score
        self.score_var.set('Score: {}'.format(score))
        if score > self.high_score:
            self.update_high_score(score)

    def update_high_score(self, high_score):
        self.high_score = high_score
        self.high_score_var.set('High Score: {}'.format(high_score))

    def show_scoreboard(self):
        self.root.mainloop()

# Set up the game loop
def game_loop():
    snake = Snake()
    food = Food()
    scoreboard = ScoreBoard()
    clock = pygame.time.Clock()

    game_over = False
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.change_direction('right')
                elif event.key == pygame.K_LEFT:
                    snake.change_direction('left')
                elif event.key == pygame.K_UP:
                    snake.change_direction('up')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('down')

        # Move the snake
        snake.move()

        # Check for collision with the food
        if food.check_collision(snake):
            snake.grow()
            scoreboard.update_score(snake.score)

        # Check for collision with the walls or itself
        if snake.check_collision():
            game_over = True

        # Draw the objects
        WINDOW.fill(BLACK)
        snake.draw()
        food.draw()
        pygame.display.update()

        # Set the frame rate
        clock.tick(10)

    # Clean up the game and show the final score
    pygame.quit()
    scoreboard.show_scoreboard()
    print('Final Score:', snake.score)

if __name__ == '__main__':
    game_loop()