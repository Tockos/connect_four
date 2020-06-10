#! python

import numpy as np
import pygame
import sys
import math
import random

ROW_COUNT = 6
COL_COUNT = 7
WIN_COUNT = 4

BLUE = (0, 50, 150)
BLACK = (10, 10, 10)
RED = (150, 0, 30)
YELLOW = (210, 180, 0)
RED_WINS_COLOR = (250, 10, 10)
YELLOW_WINS_COLOR = (250, 210, 0)

PLAYER = 1
AI = 2
WINNING_PATTERN_RED = 3
WINNING_PATTERN_YELLOW = 4


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

    winning_horiz = [starting_point]
    winning_vert = [starting_point]
    winning_pos = [starting_point]
    winning_neg = [starting_point]

    while not (end_plus_plus and
               end_minus_minus and
               end_plus_minus and
               end_minus_plus and
               end_plus_const and
               end_minus_const and
               end_const_plus and
               end_const_minus):

        # vertical
        if plus_const[0] + 1 < ROW_COUNT and not end_plus_const:
            plus_const[0] += 1
            if state_in_board[plus_const[0]][plus_const[1]] == player_id:
                counter_plus_const += 1
                winning_vert.append(plus_const.copy())
            else:
                end_plus_const = 1
        else:
            end_plus_const = 1

        if minus_const[0] - 1 > -1 and not end_minus_const:
            minus_const[0] -= 1
            if state_in_board[minus_const[0]][minus_const[1]] == player_id:
                counter_minus_const += 1
                winning_vert.append(minus_const.copy())
            else:
                end_minus_const = 1
        else:
            end_minus_const = 1

        if 1 + counter_plus_const + counter_minus_const >= WIN_COUNT:
            return True, winning_vert

        # horizontal
        if const_plus[1] + 1 < COL_COUNT and not end_const_plus:
            const_plus[1] += 1
            if state_in_board[const_plus[0]][const_plus[1]] == player_id:
                counter_const_plus += 1
                winning_horiz.append(const_plus.copy())
            else:
                end_const_plus = 1
        else:
            end_const_plus = 1

        if const_minus[1] - 1 > -1 and not end_const_minus:
            const_minus[1] -= 1
            if state_in_board[const_minus[0]][const_minus[1]] == player_id:
                counter_const_minus += 1
                winning_horiz.append(const_minus.copy())
            else:
                end_const_minus = 1
        else:
            end_const_minus = 1

        if 1 + counter_const_plus + counter_const_minus >= WIN_COUNT:
            return True, winning_horiz

        # negative slope up
        if plus_plus[0] + 1 < ROW_COUNT and plus_plus[1] + 1 < COL_COUNT and not end_plus_plus:
            plus_plus[0] += 1
            plus_plus[1] += 1
            if state_in_board[plus_plus[0]][plus_plus[1]] == player_id:
                counter_plus_plus += 1
                winning_neg.append(plus_plus.copy())
            else:
                end_plus_plus = 1
        else:
            end_plus_plus = 1

        if minus_minus[0] - 1 > -1 and minus_minus[1] - 1 > -1 and not end_minus_minus:
            minus_minus[0] -= 1
            minus_minus[1] -= 1
            if state_in_board[minus_minus[0]][minus_minus[1]] == player_id:
                counter_minus_minus += 1
                winning_neg.append(minus_minus.copy())
            else:
                end_minus_minus = 1
        else:
            end_minus_minus = 1

        if 1 + counter_plus_plus + counter_minus_minus >= WIN_COUNT:
            # print("negative slope\n")
            # print(winning_neg)
            return True, winning_neg

        # positive slope
        if plus_minus[0] + 1 < ROW_COUNT and plus_minus[1] - 1 > -1 and not end_plus_minus:
            plus_minus[0] += 1
            plus_minus[1] -= 1
            if state_in_board[plus_minus[0]][plus_minus[1]] == player_id:
                counter_plus_minus += 1
                winning_pos.append(plus_minus.copy())
            else:
                end_plus_minus = 1
        else:
            end_plus_minus = 1

        if minus_plus[0] - 1 > -1 and minus_plus[1] + 1 < COL_COUNT and not end_minus_plus:
            minus_plus[0] -= 1
            minus_plus[1] += 1
            if board[minus_plus[0]][minus_plus[1]] == player_id:
                counter_minus_plus += 1
                winning_pos.append(minus_plus.copy())
            else:
                end_minus_plus = 1
        else:
            end_minus_plus = 1

        if 1 + counter_plus_minus + counter_minus_plus >= WIN_COUNT:
            # print("positive slope\n")
            # print(winning_pos)
            return True, winning_pos

    return False, 0


def eval_window(window, piece):
    opp_piece = PLAYER
    if piece == PLAYER:
        opp_piece = AI
    score = 0
    window = np.array(window)
    if np.count_nonzero(window == piece) == 4:
        score += 100
    elif np.count_nonzero(window == piece) == 3 and np.count_nonzero(window) == 3:
        score += 10
    elif np.count_nonzero(window == piece) == 2 and np.count_nonzero(window) == 2:
        score += 5

    if np.count_nonzero(window == opp_piece) == 3 and np.count_nonzero(window) == 3:
        score -= 80
    return score


def score_position(state_in_board, piece):
    score = 0

    center_array = state_in_board[:, COL_COUNT // 2]
    center_count = (center_array == piece).sum()
    if piece == AI:
        score += center_count * 6
    else:
        score -= center_count * 6
    for r in range(ROW_COUNT):
        row_array = state_in_board[r, :]
        for col in range(COL_COUNT - WIN_COUNT + 1):
            window = row_array[col:col + WIN_COUNT]
            if piece == AI:
                score = score + eval_window(window, piece)
            else:
                score = score - eval_window(window, piece)

    for c in range(COL_COUNT):
        col_array = state_in_board[:, c]
        for row in range(ROW_COUNT - WIN_COUNT + 1):
            window = col_array[row:row + WIN_COUNT]
            score = score + eval_window(window, piece)

    for r in range(ROW_COUNT - WIN_COUNT + 1):
        for c in range(COL_COUNT - WIN_COUNT + 1):
            window = [state_in_board[r + i][c + i] for i in range(WIN_COUNT)]
            score = score + eval_window(window, piece)

    for r in range(ROW_COUNT - WIN_COUNT + 1):
        for c in range(COL_COUNT - WIN_COUNT + 1):
            window = [state_in_board[r + 3 - i][c + i] for i in range(WIN_COUNT)]
            score = score + eval_window(window, piece)

    return score


def mini_max(position, depth, maximizing_player, last_move):
    # if depth == 0 or is_win(position):
    # if TERMINAL NODE
    try:
        winning_position = is_win(position.copy(), position[last_move[0]][last_move[1]], last_move)[0]
    except:
        winning_position = False
    if winning_position:
        if maximizing_player == AI:
            score = -10000000000
            return score, None
        else:
            score = 10000000000
            return score, None
    elif depth == 0:
        score = score_position(position.copy(), AI)
        return score, None
    elif np.count_nonzero(board[0]) == COL_COUNT:
        score = 0
        return score, None

    else:
        if maximizing_player == AI:
            max_eval = float("-inf")
            best_column = 0
            for col in range(COL_COUNT):
                if is_valid_col(position.copy(), col):
                    first_empty_row = get_next_open_row(position.copy(), col)
                    child = drop_piece(position.copy(), first_empty_row, col, AI)
                    curr_eval = mini_max(child, depth - 1, PLAYER, [first_empty_row, col])[0]
                    if curr_eval > max_eval:
                        max_eval = curr_eval
                        best_column = col
            return max_eval, best_column

        else:
            min_eval = float("inf")
            best_column = 0
            for col in range(COL_COUNT):
                if is_valid_col(position.copy(), col):
                    first_empty_row = get_next_open_row(position.copy(), col)
                    child = drop_piece(position.copy(), first_empty_row, col, PLAYER)
                    curr_eval = mini_max(child, depth - 1, AI, [first_empty_row, col])[0]
                    if curr_eval < min_eval:
                        min_eval = curr_eval
                        best_column = col
            return min_eval, best_column


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
            elif board[r][c] == WINNING_PATTERN_RED:
                pygame.draw.circle(screen, RED_WINS_COLOR,
                                   (int((c + 1 / 2) * SQUARE_SIZE), int((r + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
            elif board[r][c] == WINNING_PATTERN_YELLOW:
                pygame.draw.circle(screen, YELLOW_WINS_COLOR,
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
player_to_turn = random.randint(PLAYER, AI)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]

            if player_to_turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            selection = int(math.floor(posx / SQUARE_SIZE))

            if player_to_turn == PLAYER:
                if is_valid_col(board, selection):
                    row = get_next_open_row(board, selection)
                    board = drop_piece(board.copy(), row, selection, player_to_turn)
                    # print(board)
                    draw_board(board)
                    last_piece = [row, selection]
                    win, pattern = is_win(board, player_to_turn, last_piece.copy())
                    if win:
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                        label = my_font.render("You won.", 1, RED)
                        screen.blit(label, (200, 10))
                        for i in range(len(pattern)):
                            piece_to_highlight = pattern[i]
                            board[piece_to_highlight[0]][piece_to_highlight[1]] = WINNING_PATTERN_RED
                            draw_board(board)
                        pygame.display.update()
                        game_over = True
                    else:
                        player_to_turn = AI
                        # pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                        # pygame.display.update()

        if player_to_turn == AI and not game_over:
            # print(event.pos)
            depth = 4
            try:
                score, selection = mini_max(board.copy(), depth, player_to_turn, last_piece)
            except NameError:
                score, selection = mini_max(board.copy(), depth, player_to_turn, None)
            print(selection)
            if is_valid_col(board, selection):
                pygame.time.wait(600)
                row = get_next_open_row(board, selection)
                board = drop_piece(board.copy(), row, selection, player_to_turn)
                # print(board)
                draw_board(board)
                last_piece = [row, selection]
                win, pattern = is_win(board.copy(), player_to_turn, last_piece.copy())
                if win:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                    label = my_font.render("You lost.", 1, YELLOW)
                    screen.blit(label, (200, 10))
                    for i in range(len(pattern)):
                        piece_to_highlight = pattern[i]
                        board[piece_to_highlight[0]][piece_to_highlight[1]] = WINNING_PATTERN_YELLOW
                        draw_board(board)
                    pygame.display.update()
                    game_over = True
                else:
                    player_to_turn = PLAYER
                    # pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                    # pygame.display.update()
                    # print(board)

                if np.count_nonzero(board[0]) == COL_COUNT:
                    game_over = True
                    print("Draw")

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit(), sys.exit()
