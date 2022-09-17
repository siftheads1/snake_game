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

class AI(SnakeGame):
    APPLE_INFO = []

    def __init__(self, stud_id, name, snake_pos, time_limit, n_apple):

        self.load_apple_info("apple_info.csv")

        super().__init__(stud_id, name, snake_pos, AI.APPLE_INFO) #TODO: need apple_info argument

        self.time_limit = time_limit
        self.n_apple = n_apple
        self.movement = []

    def load_apple_info(self, file_dir):
        # apple.csv 파일에서 apple에 대한 정보를 읽어 class 변수 APPLE_INFO에 저장

        f = open("apple_info.csv", "r")

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

            AI.APPLE_INFO.append(apple_property)

        f.close()

    def init_apple(self, snake):
        # snake를 피해서 random 하게 apple initialize

        for _ in range(self.n_apple):
            self.add_apple(snake, True) #, apple_info)
        return -1

    def update_status(self, apple):
        # 먹은 사과의 역할에 맞게 status update

        #is_gold = True if apple.get_color() == "Gold" else False

        cur_score = self.board.get_score()
        cur_score += apple.get_point()
        self.board.set_score(cur_score)

        cur_speed = self.board.get_speed()
        cur_speed += apple.get_speed()
        self.board.set_speed(cur_speed)

        self.board.set_length(self.snake.get_len())

        self.apples.eat_apple(apple)

        return -1

    def find_path(self):
        #cur_distance = 1
        head_pos = self.snake.get_head_pos()
        apple_list = self.apples.get_apple_list()
        cur_len = self.snake.get_len()
        path_list_tmp = [[(head_pos[0] - 30, head_pos[1])], [(head_pos[0] + 30, head_pos[1])], [(head_pos[0], head_pos[1] - 30)], [(head_pos[0], head_pos[1] + 30)]]

        path_list = []
        path_to_apple = None

        for path in path_list_tmp:
            is_valid_path = True

            if (path[-1][0] < 0 or path[-1][0] > 720) or (path[-1][1] < 0 or path[-1][1] > 720):
                is_valid_path = False

            for body_pos in self.snake.get_bodies():
                if path[-1] == body_pos:
                    is_valid_path = False

            if is_valid_path:

                for apple in apple_list:
                    if apple.get_pos() == path[-1]:
                        return path

                path_list.append(path)

        while True:

            #cur_distance += 1

            #debugging code
            #print(path_list)

            new_path_list = []

            for path in path_list:

                #debugging code
                #print(path)
                #print(path.append((path[-1][0] - 30, path[-1][1])))

                """
                path_list_temp = [path.append((path[-1][0] - 30, path[-1][1])),
                path.append((path[-1][0] + 30, path[-1][1])),
                path.append((path[-1][0], path[-1][1] - 30)),
                path.append((path[-1][0], path[-1][1] + 30))]
                """
                path_list_temp = [(path + [(path[-1][0] - 30, path[-1][1])]),
                                  (path + [(path[-1][0] + 30, path[-1][1])]),
                                  (path + [(path[-1][0], path[-1][1] - 30)]),
                                  (path + [(path[-1][0], path[-1][1] + 30)])]

                #debugging code
                #print(path_list_temp)

                paths_to_append = []

                for temp_path in path_list_temp:

                    #check if the path leads to the game over
                    is_valid_path = True

                    #gets out of map
                    if (temp_path[-1][0] < 0 or temp_path[-1][0] > 720) or (temp_path[-1][1] < 0 or temp_path[-1][1] > 720):
                        is_valid_path = False

                    #overlaps with body
                    body_pos_list = (self.snake.get_bodies() + path)[-(cur_len):]
                    for body_pos in body_pos_list:
                        if body_pos == temp_path[-1]:
                            is_valid_path = False

                    if is_valid_path:

                        #check if snake has reached to the apple
                        for apple in apple_list:
                            if apple.get_pos() == temp_path[-1]:
                                return temp_path

                        #check if the path is redundant(destination is already searched)
                        is_redundant_path = False

                        for prev_path in (path_list + new_path_list):
                            if prev_path[-1] == temp_path[-1]:
                                is_redundant_path = True
                                break

                        if not is_redundant_path:
                            paths_to_append.append(temp_path)

                new_path_list = new_path_list + paths_to_append

            path_list = new_path_list

            #debugging code
            print(f"num_of_paths: {len(path_list)}")

    def find_next_direction(self, path):

        #debugging code
        print(f"len_of_path: {len(path)}")

        head_pos = self.snake.get_head_pos()
        if path[0][0] == head_pos[0]:
            if path[0][1] < head_pos[1]:
                return K_UP
            else:
                return K_DOWN
        else:
            if path[0][0] < head_pos[0]:
                return K_LEFT
            else:
                return K_RIGHT

    def get_movement(self):
        # self.movement에 움직일 방향을 저장

        # Q: Do we really need to do this every time? Looks super inefficient...
        path = self.find_path()
        key = self.find_next_direction(path)
        self.movement = [key] #or append, idk

    def do_game(self):
        self.init_apple(self.snake)

        start_ticks = pygame.time.get_ticks()
        self.get_movement()
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000


        self.board.load_highest_score(SnakeGame.HIGHSCORE_SAVE_DIR)

        self.paint()

        if seconds <= 60:
            """ implement  here """

            while True:

                print(self.snake.get_head_pos())

                #응급처치 코드(L228-L231)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                for event in self.movement:
                    self.key = event

                is_game_over = self.snake.move(self.key, self.apples)

                for apple in self.apples.get_apple_list():
                    if self.snake.get_head_pos() == apple.get_pos():
                        self.update_status(apple)

                self.update_board()

                self.paint()

                if is_game_over:
                    #TODO: delete this print statement
                    print(f"score: {self.board._score}")
                    print("game over")
                    pygame.quit()
                    sys.exit()

                self.get_movement()

                seconds = (pygame.time.get_ticks() - start_ticks) / 1000

                print(seconds)

                if seconds > 60:
                    print(f"score: {self.board._score}")
                    print("game over")
                    pygame.quit()
                    sys.exit()


                clock.tick(self.board.get_speed())
        else:
            print(f"score: {self.board._score}")
            pygame.quit()
            sys.exit()
