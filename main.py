from ui import UI
from ai import AI

TIME_LIMIT = 60
N_APPLE = 25


def main():
    stud_id = "2021-12345"
    name = "안재훈"
    snake_pos = (0, 0)

    print("***** Snake Game *****")
    print(" 1: User mode \t 2: AI mode")
    mode = int(input("Select mode: "))

    if mode == 1:
        ui_game = UI(stud_id, name, snake_pos)
        ui_game.do_game()
    elif mode == 2:
        ai_game = AI(stud_id, name, snake_pos, TIME_LIMIT, N_APPLE)
        ai_game.do_game()


if __name__=="__main__":
    main()
