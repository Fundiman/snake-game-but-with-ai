import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
SNAKE_SIZE = 10
FPS = 10
COLOR_CHANGE_INTERVAL = 3000  # 3 seconds in milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Interpolation function for colors
def interpolate_color(color1, color2, factor):
    return tuple(int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3))

# Snake class
class Snake:
    def __init__(self):
        self.body = [(200, 200), (210, 200), (220, 200)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.auto_move = False
        self.color = (0, 255, 0)  # Start with green

    def move(self):
        if self.auto_move:
            self.move_towards_food()
        head = self.body[0]
        x, y = self.direction
        new_head = ((head[0] + (x * GRID_SIZE)) % WIDTH, (head[1] + (y * GRID_SIZE)) % HEIGHT)
        self.body.insert(0, new_head)
        if len(self.body) > self.score + 1:
            self.body.pop()

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def grow(self):
        self.score += 1

    def move_towards_food(self):
        head_x, head_y = self.body[0]
        food_x, food_y = food.position
        if head_x < food_x:
            self.direction = RIGHT
        elif head_x > food_x:
            self.direction = LEFT
        elif head_y < food_y:
            self.direction = DOWN
        elif head_y > food_y:
            self.direction = UP

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))


# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                         random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
        self.color = (255, 0, 0)  # Start with red

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# Load images for the toggle switch and resize them
toggle_on_img = pygame.image.load('toggle_on.png')
toggle_off_img = pygame.image.load('toggle_off.png')
toggle_on_img = pygame.transform.scale(toggle_on_img, (GRID_SIZE * 5, GRID_SIZE * 5))
toggle_off_img = pygame.transform.scale(toggle_off_img, (GRID_SIZE * 5, GRID_SIZE * 5))
toggle_img_rect = toggle_on_img.get_rect(topleft=(10, 130))  # Position under the Cheat-Bot text

def draw_button(screen, image, position):
    screen.blit(image, position)

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

snake = Snake()
food = Food()

# Time tracking for color change
last_color_change_time = pygame.time.get_ticks()
color_change_duration = COLOR_CHANGE_INTERVAL
start_color_snake = (0, 255, 0)
end_color_snake = (255, 0, 0)
start_color_food = (255, 0, 0)
end_color_food = (0, 0, 255)

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    current_time = pygame.time.get_ticks()
    time_since_last_change = current_time - last_color_change_time

    if time_since_last_change > COLOR_CHANGE_INTERVAL:
        last_color_change_time = current_time
        time_since_last_change = 0
        # Swap colors for the next transition
        start_color_snake, end_color_snake = end_color_snake, start_color_snake
        start_color_food, end_color_food = end_color_food, start_color_food

    # Interpolate colors
    factor = time_since_last_change / COLOR_CHANGE_INTERVAL
    snake.color = interpolate_color(start_color_snake, end_color_snake, factor)
    food.color = interpolate_color(start_color_food, end_color_food, factor)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.change_direction(RIGHT)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if toggle_img_rect.collidepoint(mouse_pos):
                snake.auto_move = not snake.auto_move

    # Move snake
    snake.move()

    # Check collision with food
    if snake.body[0] == food.position:
        snake.grow()
        food = Food()

    # Draw snake and food
    snake.draw(screen)
    food.draw(screen)

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {snake.score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw Cheat-Bot text and toggle switch
    cheat_bot_text = font.render("Cheat-Bot", True, WHITE)
    screen.blit(cheat_bot_text, (10, 90))
    if snake.auto_move:
        draw_button(screen, toggle_on_img, toggle_img_rect.topleft)
    else:
        draw_button(screen, toggle_off_img, toggle_img_rect.topleft)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
