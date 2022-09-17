import pygame

INFO_START_POS_X = 790
INFO_START_POS_Y = 100

DEFALUT_SPEED = 1 #original value: 0

class Board:
    def __init__(self, stud_id, name):
        self.stud_id = stud_id
        self.name = name
        self._length = 1
        self._speed = DEFALUT_SPEED
        self._score = 0
        self._highscore = 0
        self._time = 0

    #getter(없어서 추가함)
    def get_length(self):
        return self._length

    # setter
    def set_length(self, length):
        self._length = length

    # getter
    def get_speed(self):
        return self._speed

    # setter
    def set_speed(self, speed):
        self._speed = speed

    # getter
    def get_score(self):
        return self._score

    # setter
    def set_score(self, score):
        self._score = score

    # getter
    def get_highest_score(self):
        return self._highscore

    # setter
    def set_highest_score(self, high_score):
        self._highscore = high_score

    # getter
    def get_time(self):
        return self._time

    # setter
    def set_time(self, time):
        self._time = time

    # draw board
    def draw(self, BOARD):  #What is this BOARD for?
        """
        화면 상단에 학번, 이름을 나타내고 화면 우측에 점수, 최고점수, 길이, 속도, 시간을 나타낸다.
        화면 중앙에는 width=30, height=30인 25x25 격자를 그린다.
        """


        """
        #test code
        pygame.init()
        window = pygame.display.set_mode((1000, 850))
        pygame.display.set_caption("Snake Game")

        font = pygame.font.SysFont("malgungothic", 30, True, False)
        stud_id = font.render(f"{self.stud_id}", True, (0, 0, 255))
        window.blit(stud_id, [20, 40])

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            window.fill((0, 0, 0))

            #actual logic(extract this if needed)
            font = pygame.font.SysFont("malgungothic", 30, True, False)

            stud_id = font.render("Student ID: %s" % self.stud_id, True, (0, 0, 255))
            window.blit(stud_id, [40, 0])
            name = font.render("Name: %s" % self.name, True, (0, 0, 255))
            window.blit(name, [550, 0])
            score = font.render("Score:%3d" % self.get_score(), True, (255, 255, 255))
            window.blit(score, [INFO_START_POS_X, INFO_START_POS_Y])
            high_score = font.render("High score:%3d" % self.get_highest_score(), True, (255, 0, 0))
            window.blit(high_score, [INFO_START_POS_X, INFO_START_POS_Y + 100])
            length = font.render("Length:%3d" % self.get_length(), True, (0, 255, 0))
            window.blit(length, [INFO_START_POS_X, INFO_START_POS_Y + 200])
            speed = font.render("Speed:%5.2f" % self.get_speed(), True, (127, 127, 0))
            window.blit(speed, [INFO_START_POS_X, INFO_START_POS_Y + 300])
            time = font.render("Time:%3d s" % self.get_time(), True, (0, 127, 127))
            window.blit(time, [INFO_START_POS_X, INFO_START_POS_Y + 400])
            for x in range(20, 770, 30):
                for y in range(50, 800, 30):
                    pygame.draw.rect(window, (255, 255, 255), (x, y, 30, 30), 1)

            pygame.display.update()

        """

        font = pygame.font.SysFont("malgungothic", 30, True, False)

        stud_id = font.render("Student ID: %s" % self.stud_id, True, (0, 0, 255))
        BOARD.blit(stud_id, [40, 0])
        name = font.render("Name: %s" % self.name, True, (0, 0, 255))
        BOARD.blit(name, [550, 0])
        score = font.render("Score:%3d" % self.get_score(), True, (255, 255, 255))
        BOARD.blit(score, [INFO_START_POS_X, INFO_START_POS_Y])
        high_score = font.render("High score:%3d" % self.get_highest_score(), True, (255, 0, 0))
        BOARD.blit(high_score, [INFO_START_POS_X, INFO_START_POS_Y + 100])
        length = font.render("Length:%3d" % self.get_length(), True, (0, 255, 0))
        BOARD.blit(length, [INFO_START_POS_X, INFO_START_POS_Y + 200])
        speed = font.render("Speed:%5.2f" % self.get_speed(), True, (127, 127, 0))
        BOARD.blit(speed, [INFO_START_POS_X, INFO_START_POS_Y + 300])
        time = font.render("Time:%3d s" % self.get_time(), True, (0, 127, 127))
        BOARD.blit(time, [INFO_START_POS_X, INFO_START_POS_Y + 400])
        for x in range(20, 770, 30):
            for y in range(50, 800, 30):
                pygame.draw.rect(BOARD, (255, 255, 255), (x, y, 30, 30), 1)

        # 작업한 BOARD의 내용을 갱신
        pygame.display.update()

    def game_over(self, file_dir, BOARD):
        """
        화면에 Game Over를 띄우고 highscore를 score.txt 파일에 저장한다.
        """

        """
        DISPLAY GAME OVER
        """

        #should I init or not?
        #pygame.init()
        BOARD.fill((0, 0, 0))
        font = pygame.font.SysFont("malgungothic", 50, True, False)

        gameover_msg = font.render("Game Over", True, (255, 0, 0))
        BOARD.blit(gameover_msg, [400, 400])

        pygame.display.update()

        if self._score > self._highscore:
            f = open(file_dir, "w")
            f.write(str(self._score))
            f.close()


    # load highest score
    def load_highest_score(self, file_dir):
        """
        score.txt 파일로부터 highscore를 불러오며, 파일이 없거나 점수가 없을 경우 highscore는 0이다.
        """

        try:
            f = open(file_dir, "r")
            score = f.readline()

            if not score:
                self.set_highest_score(0)
            else:
                self.set_highest_score(int(score))

            f.close()

        except FileNotFoundError:
            self.set_highest_score(0)
