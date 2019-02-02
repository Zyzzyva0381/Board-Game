import pygame
import sys
from pygame.locals import *


class Turn(object):
    def __init__(self, team_names, first, sign_color, sign_poses, sign_radius):
        self.turn_dict = {
            True: team_names[0],
            False: team_names[1]
        }
        self.move = -1  # each turn has 2 moves, 0 and 1 for each move
        self.turn = first  # True for left, False for right

        self.sign_color = sign_color
        self.sign_pos = {
            True: sign_poses[0],
            False: sign_poses[1]
        }
        self.sign_radius = sign_radius
        self.next_turn = first

    def make_move(self):
        self.move += 1
        if self.move > 1:
            self.turn = not self.turn
            self.move = 0
            print("Now Player %s is in turn. " % self.turn_dict[self.turn])
        print("Now is Move %d of 1. " % self.move)

    def draw_sign(self, screen):
        # self.next_turn = self.turn if self.move < 1 else not self.turn
        pygame.draw.circle(screen, self.sign_color, self.sign_pos[self.turn], self.sign_radius)


class Tile(object):
    def __init__(self, tile_width, tile_height, tile_origin, tile_x, tile_y, tile_line_width=2):  # TODO make them keyword
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.width = tile_width
        self.height = tile_height
        self.pos = tile_origin
        self.rect = pygame.Rect(tile_origin, (tile_width, tile_height))
        self.own = "neutral"
        self.state = "blank"
        self.line_width = tile_line_width

    def draw(self, surf, colour, color1, color2):
        if self.own == True:
            pygame.draw.rect(surf, color1, self.rect)
        elif self.own == False:
            pygame.draw.rect(surf, color2, self.rect)
        pygame.draw.rect(surf, colour, self.rect, self.line_width)


class Board(object):  # TODO on board obj
    def __init__(self, board_width, board_height, board_origin, num_board_width, num_board_height):  # TODO make them keyword
        tiles = [[[] for _ in range(num_board_height)] for __ in range(num_board_width)]
        for x in range(num_board_width):
            for y in range(num_board_height):
                tile_origin_x = board_origin[0] + x * board_width
                tile_origin_y = board_origin[1] + y * board_height
                tiles[x][y] = Tile(board_width, board_height, (tile_origin_x, tile_origin_y), x, y)
        self.tiles = tiles

    def draw(self, surf, colour):
        for line in self.tiles:  # draw board
            for tile in line:
                tile.draw(surf, colour)

    def get_pressed(self, event):
        if event.type == MOUSEBUTTONUP:
            for line in self.tiles:
                for tile in line:
                    if tile.rect.collidepoint(event.pos):
                        print("Clicked tile at x=%d, y=%d. " % (tile.tile_x, tile.tile_y))


def terminate():
    pygame.quit()
    sys.exit()


def check_quit():
    for event in pygame.event.get(QUIT):
        terminate()


def main():
    pygame.init()

    winwidth = 800
    winheight = 600
    screen = pygame.display.set_mode((winwidth, winheight))
    pygame.display.set_caption("Board Game 0.0.1 Alpha - By Zyzzyva038")

    fpsclock = pygame.time.Clock()
    fps = 40

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (50, 225, 50)

    board_width = 40  # TODO make the whole board an object
    board_height = 40
    board_origin = (175, 50)
    num_board_width = 10
    num_board_height = 11

    tiles = [[[] for _ in range(num_board_height)] for __ in range(num_board_width)]
    for x in range(num_board_width):
        for y in range(num_board_height):
            tile_origin_x = board_origin[0] + x * board_width
            tile_origin_y = board_origin[1] + y * board_height
            tiles[x][y] = Tile(board_width, board_height, (tile_origin_x, tile_origin_y), x, y)

    turn = Turn(("Left", "Right"), True, (225, 0, 0), ((100, 300), (700, 300)), 5)

    old_tile_clicked = None

    start_mode = True

    while True:  # MAIN LOOP

        tile_clicked = None

        # HANDLE EVENTS

        check_quit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                for line in tiles:
                    for tile in line:
                        if tile.rect.collidepoint(event.pos):
                            print("Clicked tile at x=%d, y=%d. " % (tile.tile_x, tile.tile_y))
                            last_clicked = old_tile_clicked
                            tile_clicked = (tile.tile_x, tile.tile_y)
                            old_tile_clicked = tile_clicked

        # UPDATE GAME STATE
        if tile_clicked:
            if turn.move == -1:
                turn.make_move()
            elif turn.move == 0 and tiles[tile_clicked[0]][tile_clicked[1]].own == "neutral":
                if start_mode and tile_clicked == last_clicked:
                    turn.make_move()
                    turn.make_move()
                    tiles[tile_clicked[0]][tile_clicked[1]].own = turn.turn
                    start_mode = False
                else:
                    turn.make_move()
            elif turn.move == 1 and tile_clicked == last_clicked:
                if tiles[tile_clicked[0]][tile_clicked[1]].own == "neutral":
                    turn.make_move()
                    tiles[tile_clicked[0]][tile_clicked[1]].own = turn.turn

        #  DRAW SCREEN
        screen.fill(white)  # fill screen

        for line in tiles:  # draw board
            for tile in line:
                tile.draw(screen, black, red, blue)

        turn.draw_sign(screen)

        pygame.display.update()

        # TICK FPS
        fpsclock.tick(fps)


if __name__ == "__main__":
    main()
