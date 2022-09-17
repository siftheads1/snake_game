from snakegame import SnakeGame
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

class UI(SnakeGame):
    APPLE_INFO = [] #list of dictionaries

    def __init__(self, stud_id, name, snake_pos):
        self.load_apple_info("apple_info.csv")

        super().__init__(stud_id, name, snake_pos, UI.APPLE_INFO)

    def load_apple_info(self, file_dir):
        # apple.csv 파일에서 apple에 대한 정보를 읽어 class 변수 APPLE_INFO에 저장

        f = open(file_dir, "r")

        #to skip the labels (needs to be modified if csv files are read otherwise)
        f.readline()

        for line in f:
            data = line.split(',')
            apple_property = {}

            apple_property["color"] = data[0]
            apple_property["rgb"] = (int(data[1]), int(data[2]), int(data[3]))
            apple_property["length"] = int(data[4])
            apple_property["direction"] = True if data[5] == "TRUE" else False
            apple_property["speed"] = float(data[6])
            apple_property["point"] = int(data[7])

            UI.APPLE_INFO.append(apple_property)

        f.close()


    def do_game(self):

                """ implement  here """

                self.board.load_highest_score(SnakeGame.HIGHSCORE_SAVE_DIR)
                self.init_apple(self.snake)

                #debug code
                print("init done")

                self.paint()

                #debug code
                print("paint done")

                while True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == KEYDOWN:
                            self.key = event.key

                    is_game_over = self.snake.move(self.key, self.apples)

                    self.update_board()


                    if is_game_over:
                        break
                        #pygame.quit()
                        #sys.exit()

                    is_gold = False
                    for apple in self.apples.get_apple_list():
                        if self.snake.get_head_pos() == apple.get_pos():
                            apple_color = apple.get_color()
                            if apple_color == "Orange":
                                self.snake.reverse()
                            elif apple_color == "Gold":
                                is_gold = True

                            self.update_status(apple)

                    if is_gold:
                        self.start_fever()

                    if self.is_fever:
                        seconds = (pygame.time.get_ticks() - self.fever_start_tick) / 1000
                        if seconds > 10:
                            self.finish_fever()

                    self.paint()

                    clock.tick(self.board.get_speed())

                self.board.game_over(UI.HIGHSCORE_SAVE_DIR, BOARD)

                while True:
                    pass
