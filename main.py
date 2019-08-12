import pygame
import sys
import connection
import random
from pygame.locals import *


class Turn(object):
    def __init__(self, team_names, first, sign_color, sign_poses, sign_radius):
        self.turn_dict = {
            True: team_names[0],
            False: team_names[1]
        }
        self.move = 1  # each turn has 2 moves, 0 and 1 for each move, 0 after 1st, 1 after 2nd
        self.turn = not first  # True for left, False for right

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

    def revert_move(self):
        self.move -= 1
        if self.move < 0:
            self.turn = not self.turn
            self.move = 1
        print("Move invalid. ")

    def draw_sign(self, screen):
        self.next_turn = self.turn if self.move == 0 else not self.turn
        pygame.draw.circle(screen, self.sign_color, self.sign_pos[self.next_turn], self.sign_radius)

    def __repr__(self):
        return "Turn owned by %s at move %d" % (self.turn, self.move)

    __str__ = __repr__


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

    def draw(self, surf, colour, resources, num_width, num_height):  # TODO
        if (self.tile_x % 2 == 0 and self.tile_y % 2 == 1) or (self.tile_x % 2 == 1 and self.tile_y % 2 == 0):
            pygame.draw.rect(surf, (150, 150, 150), self.rect)
        else:
            pygame.draw.rect(surf, (200, 200, 200), self.rect)
        surf.blit(self._get_resource(resources, num_width, num_height), self.rect)

    def _get_resource(self, resources, num_width, num_height):
        if self.tile_x == 0 and self.tile_y == 0:
            return resources["home_left"]
        if self.tile_x == num_width - 1 and self.tile_y == num_height - 1:
            return resources["home_right"]
        if self.own is True:
            return resources["room_left"]
        if self.own is False:
            return resources["room_right"]
        return pygame.Surface((0, 0))

    def __repr__(self):
        return "tile at (%s, %s), owned by %s" % (self.tile_x, self.tile_y, self.own)

    __str__ = __repr__


class Board(object):  # TODO on board obj
    def __init__(self, board_width, board_height, board_origin, num_board_width, num_board_height):  # TODO make them keyword
        tiles = [[[] for _ in range(num_board_height)] for __ in range(num_board_width)]
        for x in range(num_board_width):
            for y in range(num_board_height):
                tile_origin_x = board_origin[0] + x * board_width
                tile_origin_y = board_origin[1] + y * board_height
                tiles[x][y] = Tile(board_width, board_height, (tile_origin_x, tile_origin_y), x, y)  # note
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


def show_win_screen(surf, color_, win, pos, fps):
    player_name = "Red" if win is True else "Blue"

    font = pygame.font.Font("fonts\\Mojangles.ttf", 50)
    font_surf = font.render("Player %s wins! " % player_name, True, color_)
    font_rect = font_surf.get_rect()
    font_rect.center = pos

    font2 = pygame.font.Font("fonts\\Lucida.ttf", 32)
    button_surf = font2.render("New Game", True, (0, 255, 0), (50, 50, 255))
    button_rect = button_surf.get_rect()
    button_rect.center = (pos[0], pos[1] + 100)

    fps_clock = pygame.time.Clock()

    while True:
        surf.fill((255, 255, 255))
        surf.blit(font_surf, font_rect)
        surf.blit(button_surf, button_rect)
        pygame.display.update()

        check_quit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if button_rect.collidepoint(event.pos):
                    main()

        fps_clock.tick(fps)


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
    pygame.display.set_caption("Blockin' Blocks 0.0.1 Beta - By Zyzzyva038 & CG Studio")
    pygame.display.set_icon(pygame.image.load("resources\\logo.jpg"))

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

    resources = {
        "home_left": pygame.transform.scale(pygame.image.load("resources\\home_left.png"),
                                            (board_width, board_height), ),
        "home_right": pygame.transform.scale(pygame.image.load("resources\\home_right.png"),
                                             (board_width, board_height), ),
        "room_left": pygame.transform.scale(pygame.image.load("resources\\room_left.png"),
                                            (board_width, board_height), ),
        "room_right": pygame.transform.scale(pygame.image.load("resources\\room_right.png"),
                                             (board_width, board_height), ),
        "block": pygame.transform.scale(pygame.image.load("resources\\block.png"),
                                        (board_width, board_height), ),
    }

    tiles = [[[] for _ in range(num_board_height)] for __ in range(num_board_width)]
    for x in range(num_board_width):
        for y in range(num_board_height):
            tile_origin_x = board_origin[0] + x * board_width
            tile_origin_y = board_origin[1] + y * board_height
            tiles[x][y] = Tile(board_width, board_height, (tile_origin_x, tile_origin_y), x, y)
    tiles[0][0].own = True
    tiles[-1][-1].own = False

    turn = Turn(("Left", "Right"), True, (225, 0, 0), ((100, 300), (700, 300)), 5)

    old_tile_clicked = None

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
                            turn.make_move()  # TODO detect invalid moves

        # UPDATE GAME STATE
        connections1 = connection.connection2(tiles, lambda a: a.own is True)
        connections2 = connection.connection2(tiles, lambda a: a.own is False)
        if tile_clicked:
            zero_reverted = False
            if turn.move == 0:
                if tiles[tile_clicked[0]][tile_clicked[1]].own == "neutral":
                    revert_zero = True
                    for connect in connections1 if turn.turn is True else connections2:
                        if any(((tile_clicked[0] - 1, tile_clicked[1]) in connect,
                                (tile_clicked[0] + 1, tile_clicked[1]) in connect,
                                (tile_clicked[0], tile_clicked[1] - 1) in connect,
                                (tile_clicked[0], tile_clicked[1] + 1) in connect,)):
                            if (0, 0) in connect or (num_board_width - 1, num_board_height - 1) in connect:
                                revert_zero = False
                                break
                    if revert_zero:
                        turn.revert_move()
                        zero_reverted = True
            if turn.move == 1 and tile_clicked == last_clicked and not zero_reverted:
                if tiles[tile_clicked[0]][tile_clicked[1]].own == "neutral":
                    for connect in connections1 if turn.turn is True else connections2:
                        if any(((tile_clicked[0] - 1, tile_clicked[1]) in connect,
                                (tile_clicked[0] + 1, tile_clicked[1]) in connect,
                                (tile_clicked[0], tile_clicked[1] - 1) in connect,
                                (tile_clicked[0], tile_clicked[1] + 1) in connect,)):
                            if (0, 0) in connect or (num_board_width - 1, num_board_height - 1) in connect:
                                tiles[tile_clicked[0]][tile_clicked[1]].own = turn.turn
                                break
                else:
                    turn.revert_move()
                    turn.revert_move()

            elif turn.move == 1 and not zero_reverted:
                find = False
                p1_tile, p1_tiles, p2_tile, p2_tiles = None, None, None, None
                for i in connections1:
                    if tile_clicked in i:
                        p1_tiles = i
                        p1_tile = tile_clicked
                        find = True
                        break
                if find:
                    for i in connections2:
                        if last_clicked in i:
                            p2_tiles = i
                            p2_tile = last_clicked
                else:
                    for i in connections2:
                        if tile_clicked in i:
                            p2_tiles = i
                            p2_tile = tile_clicked
                            break
                    for i in connections1:
                        if last_clicked in i:
                            p1_tiles = i
                            p1_tile = last_clicked

                if (all((p1_tile, p1_tiles, p2_tile, p2_tiles))
                    and p1_tile in ((p2_tile[0] - 1, p2_tile[1]), (p2_tile[0] + 1, p2_tile[1]),
                                    (p2_tile[0], p2_tile[1] - 1), (p2_tile[0], p2_tile[1] + 1))):
                    p1_len = len(p1_tiles)
                    p2_len = len(p2_tiles)
                    rand = random.randint(1, p1_len + p2_len)
                    if rand <= p1_len:
                        p1_win = True
                    else:
                        p1_win = False
                    if p1_win:
                        tiles[p2_tile[0]][p2_tile[1]].own = True
                    else:
                        tiles[p1_tile[0]][p1_tile[1]].own = False
                else:
                    turn.revert_move()
                    turn.revert_move()

        #  DRAW SCREEN
        screen.fill(white)  # fill screen

        for line in tiles:  # draw board
            for tile in line:
                tile.draw(screen, black, resources, num_board_width, num_board_height)

        turn.draw_sign(screen)

        pygame.display.update()

        # check if won
        if tiles[0][1].own is False or tiles[1][0].own is False:
            print("Player right wins. ")
            pygame.time.wait(1000)
            show_win_screen(screen, red, False, (winwidth / 2, winheight / 2), fps)
        if tiles[-1][-2].own is True or tiles[-2][-1].own is True:
            print("Player left wins. ")
            pygame.time.wait(1000)
            show_win_screen(screen, red, True, (winwidth / 2, winheight / 2), fps)

        # TICK FPS
        fpsclock.tick(fps)


if __name__ == "__main__":
    main()
