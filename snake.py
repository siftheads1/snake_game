import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN

BOARD_LEFT_BOUND = 0
BOARD_RIGHT_BOUND = 720
BOARD_UPPER_BOUND = 0
BOARD_LOWER_BOUND = 720

class Snake:

    direction_dict = {K_RIGHT: 0, K_LEFT: 1, K_DOWN: 3, K_UP: 4}

    def __init__(self, snake_pos, direction=0):
        self.bodies = [snake_pos] #Assumes that pos order is head->tail
        self.len = len(self.bodies)
        self.direction = direction #What is input type?
        self.key_flip = False #whether key input should be flipped (Purple apple)
        self.invisible = False #whether snake is invisible (Gray apple)

    def get_len(self):
        return self.len

    def get_bodies(self):
        return self.bodies

    def get_head_pos(self):
        return self.bodies[0]

    def move(self, key, apples):  #probably need to check if I ate certain apple
        # move snake, game over 여부를 판정한다.
        # return is_game_over

        direction = self.direction

        try:
            direction = Snake.direction_dict[key]
        except:
            pass

        if self.key_flip:
            direction = self.flip_direction(direction)

        self.change_direction(direction)

        is_game_over = False
        #reverse = False

        head_pos = None

        #snake moves right
        if self.direction == 0:
            head_pos = (self.bodies[0][0] + 30, self.bodies[0][1])
        #sneak moves left
        elif self.direction == 1:
            head_pos = (self.bodies[0][0] - 30, self.bodies[0][1])
        #sneak moves down
        elif self.direction == 3:
            head_pos = (self.bodies[0][0], self.bodies[0][1] + 30)
        #sneak moves up
        elif self.direction == 4:
            head_pos = (self.bodies[0][0], self.bodies[0][1] - 30)


        length_change = 0

        for apple in apples.get_apple_list():
            if apple.get_pos() == head_pos:
                self.key_flip = False
                self.invisible = False

                length_change = apple.length

                """
                if apple.direction == True:
                    if apple.color == "Orange":
                        reverse = True
                    else:
                        self.key_flip = True
                """
                if apple.direction == True and apple.get_color() == "Purple":
                    self.key_flip = True

                if apple.color == "Gray":
                    self.invisible = True

        #Game over: snake went off the board
        self.move_aux(head_pos, length_change)

        """
        if reverse:
            self.bodies = self.bodies[::-1]
            if self.bodies[0][0] == self.bodies[1][0]:
                self.direction = 2 if self.bodies[0][1] > self.bodies[1][1] else 3
            else:
                self.direction = 0 if self.bodies[0][0] > self.bodies[1][0] else 1

        """

        is_game_over = self.check_game_over(head_pos)

        return is_game_over

    def draw(self, BOARD):
        # snake을 그린다.
        # rgb code는 head의 경우, (51, 153, 255), 몸통의 경우 (0, 255, 255)을 이용한다.

        pygame.draw.rect(BOARD, (51, 153, 255), (self.bodies[0][0] + 20, self.bodies[0][1] + 50, 30, 30))
        pygame.draw.rect(BOARD, (0, 255, 255), (self.bodies[-1][0] + 20, self.bodies[-1][1] + 50, 30, 30))
        if not self.invisible:
            for (x, y) in self.bodies[1:-1]:
                pygame.draw.rect(BOARD, (0, 255, 255), (x + 20, y + 50, 30, 30))

        pygame.display.update()

    def change_direction(self, direction):
        # change snake's direction
        if abs(self.direction - direction) != 1:  #check if input direction is the direction the head came from
            self.direction = direction

    def check_game_over(self, head_pos):

        if (head_pos[0] < BOARD_LEFT_BOUND or head_pos[0] > BOARD_RIGHT_BOUND) or (head_pos[1] < BOARD_UPPER_BOUND or head_pos[1] > BOARD_LOWER_BOUND):
            return True

        for body_pos in self.bodies[1:]:
            if head_pos == body_pos:
                return True

        return False

    def move_aux(self, head_pos, length_change):
        self.bodies.insert(0, head_pos)
        self.len = self.len + length_change
        self.bodies = self.bodies[: self.len]

    def flip_direction(self, direction):

        #left <-> right
        if direction == 0:
            return 1
        elif direction == 1:
            return 0

        #up <-> down
        elif direction == 3:
            return 4
        elif direction == 4:
            return 3

    def reverse(self):
        self.bodies = self.bodies[::-1]
        if self.bodies[0][0] == self.bodies[1][0]:
            self.direction = 3 if self.bodies[0][1] > self.bodies[1][1] else 4
        else:
            self.direction = 0 if self.bodies[0][0] > self.bodies[1][0] else 1
