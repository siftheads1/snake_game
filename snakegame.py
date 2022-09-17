from board import Board
from apple import *
from snake import Snake
import sys
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, Rect

WIDTH = 1000
HEIGHT = 850
# pygame 초기화
pygame.init()
# BOARD 객체 저장
BOARD = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
# FPS를 위한 Clock 생성
clock = pygame.time.Clock()

pygame.key.set_repeat(5, 5)

class SnakeGame:

    HIGHSCORE_SAVE_DIR = "score.txt"

    def __init__(self, stud_id, name, snake_pos, apple_info):
        self.key = K_DOWN
        self.game_over = False

        self.apples = Apples()          #apples initialize
        self.snake = Snake(snake_pos)   #snake initialize
        self.board = Board(stud_id, name)    #board initialize

        self.apple_info = apple_info
        self.is_fever = False
        self.fever_start_tick = 0
        self.game_start_tick = pygame.time.get_ticks()


    def add_apple(self, snake, is_gold):
        # 각 색깔에 해당하는 확률에 맞게 Apple instance를 만들어서 Apples class에 넣기
        # add apple 하나씩

        """
        colors = (("Green", (51, 204, 51)),
                  ("Blue", (0, 102, 255)),
                  ("Orange", (255, 153, 51)),
                  ("Gray", (128, 128, 128)),
                  ("Purple", (153, 102, 255)),
                  ("Pink", (255, 51, 204))
                  ("Red", (255, 0, 0))
                  ("Gold", (255, 215, 0)))
        """

        apple_index_list = [0, 0, 0, 1, 2, 3, 4, 5, 6, 7]  #(num - 1)s corresponding to the index on specification

        if self.snake.get_len() <= 4:
            apple_index_list[3] = 0

        apple_property_index = apple_index_list[random.randint(0, 9)]

        if is_gold:
            apple_property_index = 0

        apple_property = self.apple_info[apple_property_index]

        new_apple_pos = None
        while True:
            is_valid_pos = True
            new_apple_pos = (random.randint(0, 24) * 30, random.randint(0, 24) * 30)

            for apple in self.apples.get_apple_list():
                if new_apple_pos == apple.get_pos():
                    is_valid_pos = False

            for snake_pos in self.snake.get_bodies():
                if new_apple_pos == snake_pos:
                    is_valid_pos = False

            if is_valid_pos:
                break

        new_apple = Apple(apple_property["color"],
                          apple_property["rgb"],
                          new_apple_pos,
                          apple_property["length"],
                          apple_property["direction"],
                          apple_property["point"],
                          apple_property["speed"])

        self.apples.set_apple(new_apple)

        return -1

    def init_apple(self, snake):
        # snake를 피해서 random 하게 apple initialize

        for _ in range(10):
            self.add_apple(snake, False) #, apple_info)
        return -1

    def update_board(self):
        cur_time = (pygame.time.get_ticks() - self.game_start_tick) / 1000
        self.board.set_time(cur_time)

    def update_status(self, apple):
        # 먹은 사과의 역할에 맞게 status update

        cur_score = self.board.get_score()
        cur_score += apple.get_point()
        self.board.set_score(cur_score)

        cur_speed = self.board.get_speed()
        cur_speed += apple.get_speed()
        self.board.set_speed(cur_speed)

        self.board.set_length(self.snake.get_len())

        self.apples.eat_apple(apple)
        self.add_apple(self.snake, self.is_fever)

        return -1

    def paint(self):
        # 게임 화면 그리기

        BOARD.fill((0, 0, 0))
        self.board.draw(BOARD)
        self.snake.draw(BOARD)
        self.apples.draw(BOARD)

        return -1

    def start_fever(self):
        self.is_fever = True
        self.fever_start_tick = pygame.time.get_ticks()
        self.apples.change_apple_properties(self.apple_info[0])

    def finish_fever(self):
        self.apples.clear_apple_list()
        self.init_apple(self.snake)
        self.is_fever = False

    def do_game(self):

        """ implement  here """

        self.board.load_highest_score(HIGHSCORE_SAVE_DIR)
        self.init_apple(self.snake)

        self.paint()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.key = event.key

            is_game_over = self.snake.move(self.key, self.apples)

            self.update_board()

            """
            if is_game_over:
                self.board.game_over(BOARD, SnakeGame.HIGHSCORE_SAVE_DIR)
                #pygame.quit()
                #sys.exit()
            """

            is_gold = False
            for apple in self.apples.get_apple_list():
                if self.snake.get_head_pos() == apple.get_pos():
                    apple_color = apple.get_color()
                    if apple_color == "Orange":
                        self.snake.reverse()
                    elif apple_color == "Gold":
                        is_gold = True

                    update_status(apple)

            if is_gold:
                self.start_fever()

            if self.is_fever:
                seconds = (pygame.time.get_ticks() - self.fever_start_tick) / 1000
                if seconds > 10:
                    self.finish_fever()

            self.paint()

            clock.tick(self.board.get_speed())
