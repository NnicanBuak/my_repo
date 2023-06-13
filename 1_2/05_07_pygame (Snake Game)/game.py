import pygame
import pyautogui
import random
import sys
import tkinter as tk
from tkinter import messagebox

pygame.init()

root = tk.Tk()
root.withdraw()

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.space_pressed = False

    def draw(self, screen):
        screen.fill((0, 0, 0))

        self.font = pygame.font.Font(None, 64)

        title_text = self.font.render("Ultimate Snake", True, (255, 255, 255))
        title_text_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title_text, title_text_rect)

        self.font = pygame.font.Font(None, 36)

        controls_text = self.font.render("*Controls by Arrows", True, (255, 150, 150))
        controls_text_rect = controls_text.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(controls_text, controls_text_rect)

        start_text = self.font.render("Press Space to Start", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        screen.blit(start_text, start_text_rect)

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.space_pressed = True
            elif event.type == pygame.MOUSEBUTTONDOWN and self.space_pressed:
                self.space_pressed = False


class Game:
    def __init__(self, screen_width, screen_height, cell_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Ultimate Snake")
        self.clock = pygame.time.Clock()
        self.is_game_over = False
        self.is_game_running = False
        self.food = None
        self.gold_food = None
        self.score = 0

    def play_background_music(self):
        pygame.mixer.music.load("./assets/background_music.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def play_collision_sound(self):
        collision_sound = pygame.mixer.Sound("./assets/collision_sound.wav")
        collision_sound.play()

    def play_eat_sound(self):
        eat_sound = pygame.mixer.Sound("./assets/eat_sound.wav")
        eat_sound.play()

    def game_win(self):
        pygame.mixer.music.stop()
        messagebox.showinfo("Victory!", f"You won! Your score: {self.score}")

        pygame.display.quit()

    def game_over(self):
        pygame.mixer.music.stop()
        messagebox.showinfo("Game Over", f"Your score: {self.score}")

        pyautogui.getWindowsWithTitle("Ultimate Snake")[0].activate()

        self.stop()
        self.start()

    def generate_food(self, snake):
        while True:
            food_position = (
                random.randint(0, self.screen_width // self.cell_size - 1) * self.cell_size,
                random.randint(0, self.screen_height // self.cell_size - 1) * self.cell_size,
            )

            if food_position not in snake.body:
                return food_position

    def loop(self):
        snake = Snake(self.screen_width, self.screen_height, self.cell_size)
        self.food = Food(*self.generate_food(snake), self.cell_size)
        self.gold_food = None
        self.gold_food_timer = 0

        while self.is_game_running:
            self.clock.tick(snake.speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        snake.handle_input(event.key)

            if not self.is_game_over:
                snake.update(self.screen_width, self.screen_height)

                if snake.check_collision(self.screen_width, self.screen_height):
                    self.play_collision_sound()
                    self.is_game_over = True

                if snake.eat(self.food):
                    if snake.speed < snake.max_speed:
                        snake.speed += 0.05
                    self.play_eat_sound()
                    self.score += 1
                    snake.grow()
                    self.food = Food(*self.generate_food(snake), self.cell_size)

                if self.gold_food is None and random.random() < 0.001:
                    self.gold_food = GoldFood(*self.generate_food(snake), self.cell_size)

                if self.gold_food is not None:
                    self.gold_food_timer += 1

                    if self.gold_food_timer >= 180:
                        self.gold_food = None
                        self.gold_food_timer = 0

                    if snake.eat(self.gold_food):
                        self.play_eat_sound()
                        self.score = 9999
                        self.gold_food = None
                        self.gold_food_timer = 0
                        self.game_win()

            self.screen.fill((0, 0, 0))

            snake.draw(self.screen)
            self.food.draw(self.screen)

            if self.gold_food is not None:
                self.gold_food.draw(self.screen)

            pygame.display.update()

            if self.is_game_over:
                self.game_over()
                self.is_game_over = False
                self.score = 0

    def start(self):
        self.play_background_music()
        self.is_game_running = True
        menu = Menu(self.screen_width, self.screen_height)

        # Draw the labels once before the game loop starts
        draw_label(self.screen, "Snake", (self.screen_width // 2, self.screen_height // 2), self.screen_width,
                self.screen_height)

        # Create an instance of the Snake class
        snake = Snake(self.screen_width, self.screen_height, self.cell_size)

        # Generate the initial food using the snake instance
        self.food = Food(*self.generate_food(snake), self.cell_size)

        # Draw the food label
        draw_label(self.screen, "Food", self.food.position, self.screen_width, self.screen_height)

        while True:
            menu.draw(self.screen)
            menu.handle_events()

            if menu.space_pressed:
                self.loop()



    def stop(self):
        self.is_game_over = False
        self.score = 0
        self.food = None
        self.gold_food = None


class Snake:
    def __init__(self, screen_width, screen_height, cell_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.head_color = (0, 255, 0)
        self.body_color = (0, 200, 0)
        self.head_position = (screen_width // 2, screen_height // 2)
        self.body = [self.head_position]
        self.direction = None
        self.next_direction = None
        self.speed = 2
        self.max_speed = 5

    def handle_input(self, key):
        if self.direction is None:
            self.direction = key
        elif key == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.next_direction = key
        elif key == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.next_direction = key
        elif key == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.next_direction = key
        elif key == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.next_direction = key

    def update(self, screen_width, screen_height):
        new_head = self.head_position

        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        if self.direction == pygame.K_UP:
            new_head = (self.head_position[0], self.head_position[1] - self.cell_size)
        elif self.direction == pygame.K_DOWN:
            new_head = (self.head_position[0], self.head_position[1] + self.cell_size)
        elif self.direction == pygame.K_LEFT:
            new_head = (self.head_position[0] - self.cell_size, self.head_position[1])
        elif self.direction == pygame.K_RIGHT:
            new_head = (self.head_position[0] + self.cell_size, self.head_position[1])

        self.body.insert(0, new_head)
        self.head_position = new_head

        if self.next_direction is None:
            self.body.pop()

    def eat(self, food):
        if self.head_position == food.position:
            return True
        return False

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self, screen_width, screen_height):
        if (
            self.head_position[0] < 0
            or self.head_position[0] >= screen_width
            or self.head_position[1] < 0
            or self.head_position[1] >= screen_height
        ):
            return True

        for cell in self.body[1:]:
            if self.head_position == cell:
                return True

        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.head_color,
                         (self.head_position[0], self.head_position[1], self.cell_size, self.cell_size))
        for body_part in self.body[1:]:
            pygame.draw.rect(screen, self.body_color, (body_part[0], body_part[1], self.cell_size, self.cell_size))


def draw_label(screen, text, position, screen_width, screen_height):
    # Check if position is near the screen borders
    near_left = position[0] < 100
    near_right = position[0] > screen_width - 100
    near_top = position[1] < 100
    near_bottom = position[1] > screen_height - 100

    # Set the text color
    text_color = (255, 255, 255)

    if near_left:
        text_position = (position[0] + 20, position[1])
        arrow_symbol = "<"
    elif near_right:
        text_position = (position[0] - 120, position[1])
        arrow_symbol = ">"
    elif near_top:
        text_position = (position[0], position[1] + 20)
        arrow_symbol = "^"
    elif near_bottom:
        text_position = (position[0], position[1] - 20)
        arrow_symbol = "v"
    else:
        text_color = (0, 0, 0)
        text_position = position
        arrow_symbol = ""

    # Draw text
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=text_position)

    screen.blit(text_surface, text_rect)

    # Draw arrow symbol
    if arrow_symbol:
        arrow_font = pygame.font.Font(None, 36)
        arrow_surface = arrow_font.render(arrow_symbol, True, text_color)
        arrow_rect = arrow_surface.get_rect(center=position)
        screen.blit(arrow_surface, arrow_rect)


class Food:
    def __init__(self, x, y, size):
        self.position = (x, y)
        self.size = size
        self.color = (255, 0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.size, self.size))


class GoldFood:
    def __init__(self, x, y, size):
        self.position = (x, y)
        self.size = size
        self.color = (255, 215, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.size, self.size))


if __name__ == "__main__":
    screen_width = 800
    screen_height = 600
    cell_size = 20

    game = Game(screen_width, screen_height, cell_size)
    game.start()
