import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox

pygame.init()


class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.space_pressed = False

    def draw(self, win):
        win.fill((0, 0, 0))
        title_text = self.font.render("Snake Game", True, (255, 255, 255))
        title_text_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        win.blit(title_text, title_text_rect)

        controls_text = self.font.render("Controls by Arrows", True, (255, 255, 255))
        controls_text_rect = controls_text.get_rect(center=(self.screen_width // 2, 200))
        win.blit(controls_text, controls_text_rect)

        start_text = self.font.render("Press Space to Start", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        win.blit(start_text, start_text_rect)

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.space_pressed = True


class Game:
    def __init__(self, screen_width, screen_height, cell_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.win = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.snake_speed = 1
        self.game_over = False
        self.game_running = False

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
        collision_sound = pygame.mixer.Sound("./assets/eat_sound.wav")
        collision_sound.play()

    def show_game_over_message(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Game Over", f"Your score: {self.score}")

    def generate_food(self, snake):
        while True:
            food_position = (
                random.randint(0, self.screen_width // self.cell_size - 1) * self.cell_size,
                random.randint(0, self.screen_height // self.cell_size - 1) * self.cell_size,
            )

            if food_position not in snake.body:
                return food_position

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_running = False
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    self.snake.handle_input(event.key)

    def update_snake(self):
        new_head = self.snake.head_position

        if self.snake.next_direction:
            self.snake.direction = self.snake.next_direction
            self.snake.next_direction = None

        if self.snake.direction == pygame.K_UP:
            new_head = (self.snake.head_position[0], self.snake.head_position[1] - self.cell_size)
        elif self.snake.direction == pygame.K_DOWN:
            new_head = (self.snake.head_position[0], self.snake.head_position[1] + self.cell_size)
        elif self.snake.direction == pygame.K_LEFT:
            new_head = (self.snake.head_position[0] - self.cell_size, self.snake.head_position[1])
        elif self.snake.direction == pygame.K_RIGHT:
            new_head = (self.snake.head_position[0] + self.cell_size, self.snake.head_position[1])

        self.snake.body.insert(0, new_head)
        self.snake.head_position = new_head
        self.snake.body.pop()

    def check_snake_collision(self):
        if (
            self.snake.head_position[0] < 0
            or self.snake.head_position[0] >= self.screen_width
            or self.snake.head_position[1] < 0
            or self.snake.head_position[1] >= self.screen_height
        ):
            return True

        for cell in self.snake.body[1:]:
            if self.snake.head_position == cell:
                return True

        return False

    def loop(self):
        self.snake = Snake(self.screen_width, self.screen_height, self.cell_size)
        food = Food(*self.generate_food(self.snake), self.cell_size)

        while self.game_running:
            self.clock.tick(10)

            self.handle_events()

            if not self.game_over:
                self.update_snake()

                if self.check_snake_collision():
                    self.play_collision_sound()
                    self.show_game_over_message()
                    self.game_over = True
                    break

                if self.snake.eat(food):
                    self.play_eat_sound()
                    self.score += 1
                    food.position = self.generate_food(self.snake)

            self.win.fill((0, 0, 0))
            self.snake.draw(self.win)
            food.draw(self.win)
            pygame.display.update()

            if self.game_over:
                self.game_over = False
                self.score = 0

        self.stop_background_music()

    def start(self):
        self.play_background_music()
        self.game_running = True
        menu = Menu(self.screen_width, self.screen_height)

        while True:
            menu.draw(self.win)
            menu.handle_events()

            if menu.space_pressed:
                self.loop()


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

    def update(self):
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
        self.body.pop()

    def check_collision(self):
        if (
            self.head_position[0] < 0
            or self.head_position[0] >= self.screen_width
            or self.head_position[1] < 0
            or self.head_position[1] >= self.screen_height
        ):
            return True

        for cell in self.body[1:]:
            if self.head_position == cell:
                return True

        return False

    def eat(self, food):
        return self.head_position == food.position

    def draw(self, win):
        pygame.draw.rect(win, self.head_color, (self.head_position[0], self.head_position[1], self.cell_size, self.cell_size))
        for segment in self.body[1:]:
            pygame.draw.rect(win, self.body_color, (segment[0], segment[1], self.cell_size, self.cell_size))


class Food:
    def __init__(self, x, y, size):
        self.position = (x, y)
        self.size = size
        self.color = (255, 0, 0)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.position[0], self.position[1], self.size, self.size))


if __name__ == "__main__":
    screen_width = 800
    screen_height = 800
    cell_size = 8

    game = Game(screen_width, screen_height, cell_size)
    game.start()
