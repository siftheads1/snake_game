import pygame

class Apples:
    def __init__(self):
        self.apple_list = []

    def get_apple_list(self):
        return self.apple_list

    def set_apple(self, Apple):
        self.apple_list.append(Apple)

    def draw(self, BOARD):  #Assumes that the apple.pos contains actual coordinate of center
        # apple을 그린다.
        for apple in self.apple_list:
            pygame.draw.circle(BOARD, apple.color, (apple.pos[0] + 35, apple.pos[1] + 65), 13)

        pygame.display.update()

    def clear_apple_list(self):
        self.apple_list.clear()

    def change_apple_properties(self, apple_property):
        for apple in self.apple_list:
            apple.change_property(apple_property)

    def eat_apple(self, apple_to_eat):
        for i, apple in enumerate(self.apple_list):
            if apple_to_eat.get_pos() == apple.get_pos():
                del self.apple_list[i]


class Apple:
    def __init__(self, color, rgb, pos, length, direction, point, speed):
        self.color = color
        self.rgb = rgb
        self.pos = pos
        self.length = length
        self.direction = direction
        self.point = point
        self.speed = speed

    def get_pos(self):
        return self.pos

    def get_point(self):
        return self.point

    def get_speed(self):
        return self.speed

    def get_color(self):
        return self.color

    def change_property(self, apple_property):
        self.color = apple_property["color"]
        self.rgb = apple_property["rgb"]
        self.length = apple_property["length"]
        self.direction = apple_property["direction"]
        self.point = apple_property["point"]
        self.speed = apple_property["speed"]
