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

        controls_text = self.font.render("Controls:", True, (255, 255, 255))
        controls_text_rect = controls_text.get_rect(center=(self.screen_width // 2, 200))
        win.blit(controls_text, controls_text_rect)

        up_text = self.font.render("Move Up: Arrow Up", True, (255, 255, 255))
        up_text_rect = up_text.get_rect(center=(self.screen_width // 2, 250))
        win.blit(up_text, up_text_rect)

        down_text = self.font.render("Move Down: Arrow Down", True, (255, 255, 255))
        down_text_rect = down_text.get_rect(center=(self.screen_width // 2, 300))
        win.blit(down_text, down_text_rect)

        left_text = self.font.render("Move Left: Arrow Left", True, (255, 255, 255))
        left_text_rect = left_text.get_rect(center=(self.screen_width // 2, 350))
        win.blit(left_text, left_text_rect)

        right_text = self.font.render("Move Right: Arrow Right", True, (255, 255, 255))
        right_text_rect = right_text.get_rect(center=(self.screen_width // 2, 400))
        win.blit(right_text, right_text_rect)

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
        self.snake_speed = 10

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
        messagebox.showinfo("Game Over", "Game Over!")

    def loop(self, snake, food):
        run = True
        while run:
            pygame.time.delay(self.snake_speed)
            self.clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and snake.direction != "down":
                snake.move("up")
            elif keys[pygame.K_DOWN] and snake.direction != "up":
                snake.move("down")
            elif keys[pygame.K_LEFT] and snake.direction != "right":
                snake.move("left")
            elif keys[pygame.K_RIGHT] and snake.direction != "left":
                snake.move("right")

            snake.update()

            if snake.collide(self.screen_width, self.screen_height):
                self.play_collision_sound()
                self.show_game_over_message()
                break

            if snake.eat(food):
                self.play_eat_sound()
                self.score += 1
                food.randomize_position(snake.body)

            self.win.fill((0, 0, 0))
            snake.draw(self.win)
            food.draw(self.win)
            pygame.display.update()

        self.stop_background_music()
        pygame.quit()
        return self.score


class Cell:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, 20, 20))


class Snake:
    def __init__(self, x, y):
        self.color = (0, 255, 0)
        self.body = []
        self.head = Cell(x, y, (0, 100, 0))
        self.body.append(self.head)
        self.direction = "right"

    def move(self, direction):
        self.direction = direction

    def update(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        if self.direction == "right":
            self.head.x += 20
        if self.direction == "left":
            self.head.x -= 20
        if self.direction == "up":
            self.head.y -= 20
        if self.direction == "down":
            self.head.y += 20

    def draw(self, win):
        for cell in self.body:
            cell.draw(win)

    def collide(self, screen_width, screen_height):
        if self.head.x < 0 or self.head.x >= screen_width or self.head.y < 0 or self.head.y >= screen_height:
            return True

        for i in range(1, len(self.body)):
            if self.head.x == self.body[i].x and self.head.y == self.body[i].y:
                return True

        return False

    def eat(self, food):
        if self.head.x == food.x and self.head.y == food.y:
            self.body.append(Cell(food.x, food.y, self.color))
            return True
        else:
            return False


class Food:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.game = game

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, 20, 20))

    def randomize_position(self, snake_body):
        while True:
            self.x = random.randrange(0, self.game.screen_width - 20, 20)
            self.y = random.randrange(0, self.game.screen_height - 20, 20)

            for cell in snake_body:
                if cell.x == self.x and cell.y == self.y:
                    break
            else:
                break


def main():
    screen_width = 800
    screen_height = 800

    pygame.init()
    game = Game(screen_width, screen_height, 8)
    menu = Menu(screen_width, screen_height)

    while True:
        menu.draw(game.win)
        menu.handle_events()

        if menu.space_pressed:
            menu.space_pressed = False
            game.play_background_music()
            snake = Snake(screen_width // 2, screen_height // 2)
            food = Food(400, 300, game)
            score = game.loop(snake, food)
            print(f"Your score: {score}")

if __name__ == "__main__":
    main()
