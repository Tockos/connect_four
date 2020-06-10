#! python

import numpy as np
import pygame
import sys
import math

ROW_COUNT = 6
COL_COUNT = 7
WIN_COUNT = 4

BLUE = (0, 50, 150)
BLACK = (10, 10, 10)
RED = (150, 0, 30)
YELLOW = (210, 180, 0)


def drop_piece(board, row, col, player_id):
    board[row][col] = player_id
    return board


def is_valid_col(board, col):
    return board[0][col] == 0


def get_next_open_row(board, col):
    for r in reversed(range(ROW_COUNT)):
        if board[r][col] == 0:
            return r


def is_win(state_in_board, player_id, starting_point):
    # counters of pieces found next to each other in certain directions
    counter_plus_plus = 0
    counter_minus_minus = 0
    counter_plus_minus = 0
    counter_minus_plus = 0
    counter_plus_const = 0
    counter_minus_const = 0
    counter_const_plus = 0
    counter_const_minus = 0

    # SET THE STARTING POINTS TO THE LAST DROPPED PIECE
    # negative slope
    plus_plus = starting_point.copy()
    minus_minus = starting_point.copy()

    # positive slope
    plus_minus = starting_point.copy()
    minus_plus = starting_point.copy()

    # vertical
    plus_const = starting_point.copy()
    minus_const = starting_point.copy()

    # horizontal
    const_plus = starting_point.copy()
    const_minus = starting_point.copy()

    end_plus_plus = 0
    end_minus_minus = 0
    end_plus_minus = 0
    end_minus_plus = 0
    end_plus_const = 0
    end_minus_const = 0
    end_const_plus = 0
    end_const_minus = 0

    while not (end_plus_plus and
               end_minus_minus and
               end_plus_minus and
               end_minus_plus and
               end_plus_const and
               end_minus_const and
               end_const_plus and
               end_const_minus):

        # vertical
        if plus_const[0] + 1 < ROW_COUNT:
            plus_const[0] += 1
            if state_in_board[plus_const[0]][plus_const[1]] == player_id:
                counter_plus_const += 1
            else:
                end_plus_const = 1
        else:
            end_plus_const = 1

        if minus_const[0] - 1 > -1:
            minus_const[0] -= 1
            if state_in_board[minus_const[0]][minus_const[1]] == player_id:
                counter_minus_const += 1
            else:
                end_minus_const = 1
        else:
            end_minus_const = 1

        # horizontal
        if const_plus[1] + 1 < COL_COUNT:
            const_plus[1] += 1
            if state_in_board[const_plus[0]][const_plus[1]] == player_id:
                counter_const_plus += 1
            else:
                end_const_plus = 1
        else:
            end_const_plus = 1

        if const_minus[1] - 1 > -1:
            const_minus[1] -= 1
            if state_in_board[const_minus[0]][const_minus[1]] == player_id:
                counter_const_minus += 1
            else:
                end_const_minus = 1
        else:
            end_const_minus = 1

        # negative slope up
        if plus_plus[0] + 1 < ROW_COUNT and plus_plus[1] + 1 < COL_COUNT:
            plus_plus[0] += 1
            plus_plus[1] += 1
            if state_in_board[plus_plus[0]][plus_plus[1]] == player_id:
                counter_plus_plus += 1
            else:
                end_plus_plus = 1
        else:
            end_plus_plus = 1

        if minus_minus[0] - 1 > -1 and minus_minus[1] - 1 > -1:
            minus_minus[0] -= 1
            minus_minus[1] -= 1
            if state_in_board[minus_minus[0]][minus_minus[1]] == player_id:
                counter_minus_minus += 1
            else:
                end_minus_minus = 1
        else:
            end_minus_minus = 1

        # positive slope
        if plus_minus[0] + 1 < ROW_COUNT and plus_minus[1] - 1 > -1:
            plus_minus[0] += 1
            plus_minus[1] -= 1
            if state_in_board[plus_minus[0]][plus_minus[1]] == player_id:
                counter_plus_minus += 1
            else:
                end_plus_minus = 1
        else:
            end_plus_minus = 1

        if minus_plus[0] - 1 > -1 and minus_plus[1] + 1 < COL_COUNT:
            minus_plus[0] -= 1
            minus_plus[1] += 1
            if board[minus_plus[0]][minus_plus[1]] == player_id:
                counter_minus_plus += 1
            else:
                end_minus_plus = 1
        else:
            end_minus_plus = 1

        if (1 + counter_plus_plus + counter_minus_minus >= WIN_COUNT) or (
                1 + counter_plus_minus + counter_minus_plus >= WIN_COUNT) or (
                1 + counter_plus_const + counter_minus_const >= WIN_COUNT) or (
                1 + counter_const_plus + counter_const_minus >= WIN_COUNT):
            return True
    return False


# GRAPHIC
def draw_board(board):
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK,
                                   (int((c + 1 / 2) * SQUARE_SIZE), int((r + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED,
                                   (int((c + 1 / 2) * SQUARE_SIZE), int((r + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW,
                                   (int((c + 1 / 2) * SQUARE_SIZE), int((r + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
                pygame.display.update()


board = np.zeros((ROW_COUNT, COL_COUNT))
print(board)

# graphic
pygame.init()
pygame.font.init()

SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)

width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
my_font = pygame.font.SysFont("Arial", 75)
# logic
game_over = False
player_to_turn = 1

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if player_to_turn == 1:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            if player_to_turn == 1:
                posx = event.pos[0]
                selection = int(math.floor(posx / SQUARE_SIZE))
                # selection = input("Player " + str(player_to_turn) + " Make your Selection (0-6): ")

                selection = int(selection)
                if is_valid_col(board, selection):
                    row = get_next_open_row(board, selection)
                    board = drop_piece(board.copy(), row, selection, player_to_turn)
                    # print(board)
                    draw_board(board)
                    last_piece = [row, selection]
                    if is_win(board, player_to_turn, last_piece.copy()):
                        label = my_font.render("Player 1 wins.", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    else:
                        player_to_turn = 2
                else:
                    print("This column is full.")

            else:
                posx = event.pos[0]
                selection = int(math.floor(posx / SQUARE_SIZE))
                # selection = input("Player " + str(player_to_turn) + " Make your Selection (0-6): ")

                selection = int(selection)
                if is_valid_col(board, selection):
                    row = get_next_open_row(board, selection)
                    board = drop_piece(board.copy(), row, selection, player_to_turn)
                    # print(board)
                    draw_board(board)
                    last_piece = [row, selection]
                    if is_win(board, player_to_turn, last_piece.copy()):
                        label = my_font.render("Player 2 wins.", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True
                    else:
                        player_to_turn = 1
                    # print(board)
                else:
                    print("This column is full.")

                if np.count_nonzero(board[0]) == COL_COUNT:
                    game_over = True
                    print("Draw")

        if game_over:
            pygame.time.wait(4000)