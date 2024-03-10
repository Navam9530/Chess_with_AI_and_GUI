"""This module runs the game"""

import sys
import pygame as pg
import chess as ch
from chess import svg
from cairosvg import svg2png
import algo as al

def check_quit():
    """Checks if clicked on close button"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

def display_state_1(human_color, state_1_displayed):
    """Displaying State-1: Color choosing"""
    screen.blit(state_1_title, state_1_title.get_rect(center=(320, 180)))
    screen.blit(state_1_option_1, state_1_option_1.get_rect(center=(320, 320)))
    screen.blit(state_1_option_2, state_1_option_2.get_rect(center=(320, 430)))
    keys_pressed = pg.key.get_pressed()
    if keys_pressed[pg.K_w]:
        screen.fill('#000000')
        click_sound.play()
        human_color = ch.WHITE
        state_1_displayed = True
    elif keys_pressed[pg.K_b]:
        screen.fill('#000000')
        click_sound.play()
        human_color = ch.BLACK
        state_1_displayed = True
    return (human_color, state_1_displayed)

def display_state_2(ai_level, state_2_displayed):
    """Displaying State-2: Level choosing"""
    screen.blit(state_2_title, state_2_title.get_rect(center=(320, 120)))
    screen.blit(state_2_option_1, state_2_option_1.get_rect(center=(320, 300)))
    screen.blit(state_2_option_2, state_2_option_2.get_rect(center=(320, 400)))
    screen.blit(state_2_option_3, state_2_option_3.get_rect(center=(320, 500)))
    keys_pressed = pg.key.get_pressed()
    if keys_pressed[pg.K_1]:
        screen.fill('#000000')
        ai_level = 3
        state_2_displayed = True
    elif keys_pressed[pg.K_2]:
        screen.fill('#000000')
        ai_level = 4
        state_2_displayed = True
    elif keys_pressed[pg.K_3]:
        screen.fill('#000000')
        ai_level = 5
        state_2_displayed = True
    return (ai_level, state_2_displayed)

def display_state_3(countdown_index, state_3_displayed):
    """Displaying State-3: Counting down"""
    count_sound.play()
    state_3_title = large_font.render(f'{countdown_list[countdown_index]}', False, '#ffffff')
    screen.blit(state_3_title, state_3_title.get_rect(center=(320, 320)))
    countdown_index += 1
    if countdown_index % 60 == 0:
        screen.fill('#000000')
        if countdown_index == 180:
            state_3_displayed = True
    return (countdown_index, state_3_displayed)

def update_board(human_color, fill_boxes):
    """Updates board whenever wanted"""
    last_move = bd.peek() if bd.move_stack else None
    check = bd.king(bd.turn) if bd.is_check() else None
    game_svg = svg.board(bd,
                         orientation = human_color,
                         lastmove = last_move,
                         check = check,
                         fill = fill_boxes,
                         size = 640,
                         coordinates = False,
                         colors = colors)
    svg2png(bytestring=game_svg, write_to='game.png')
    game_png = pg.image.load('game.png').convert()
    screen.blit(game_png, (0, 0))
    return False

def human_move(fill_boxes, fill_list, possible_moves_indices, previous_box, possible_moves):
    """Plays the Human move"""
    keys_pressed = pg.mouse.get_pressed()
    if keys_pressed[0]:
        pos = pg.mouse.get_pos()
        if human_color == ch.WHITE:
            box = ch.square(pos[0] // 80, 7 - pos[1] // 80)
        else:
            box = ch.square(7 - pos[0] // 80, pos[1] // 80)
        if bd.color_at(box) == human_color:
            if previous_box != box:
                fill_boxes = {}
                fill_list = []
                possible_moves = []
                possible_moves_indices = []
            previous_box = box
            possible_moves = list(bd.legal_moves)
            for i in possible_moves:
                if i.from_square == box:
                    fill_list.append(i.to_square)
                    possible_moves_indices.append(i)
            fill_boxes = dict.fromkeys(ch.SquareSet(fill_list), '#ff000080')
        else:
            if box in fill_list:
                index = fill_list.index(box)
                move = possible_moves_indices[index]
                bd.push(move)
                move_sound.play()
                if bd.is_check():
                    check_sound.play()
            fill_boxes = {}
            fill_list = []
            possible_moves_indices = []
            possible_moves = []
        return (fill_boxes, fill_list, possible_moves_indices, previous_box, possible_moves, True)
    return (fill_boxes, fill_list, possible_moves_indices, previous_box, possible_moves, False)

def ai_move():
    """Plays the AI move"""
    ai = al.Search(bd, ai_level, human_color)
    bd.push(ai.min_max(None, 1)) # type: ignore
    move_sound.play()
    if bd.is_check():
        check_sound.play()
    return True

def announce_results():
    """Displays the result"""
    screen.fill('#000000')
    if bd.outcome().winner == human_color: # type: ignore
        result = 'YOU WON'
        win_sound.play()
    elif bd.outcome().winner == None: # type: ignore
        result = 'DRAW'
        win_sound.play()
    else:
        result = 'YOU LOST'
        lose_sound.play()
    outcome = large_font.render(f'{result}', False, '#ffffff')
    screen.blit(outcome, outcome.get_rect(center=(320, 320)))
    return True

# Initialising Pygame
pg.init()
screen = pg.display.set_mode((640, 640))
pg.display.set_caption('CHESS')
clock = pg.time.Clock()
small_font = pg.font.Font(None, 50)
medium_font = pg.font.Font(None, 100)
large_font = pg.font.Font(None, 150)
click_sound = pg.mixer.Sound('sounds/click.wav')
count_sound = pg.mixer.Sound('sounds/count.wav')
move_sound = pg.mixer.Sound('sounds/move.wav')
check_sound = pg.mixer.Sound('sounds/capture.wav')
win_sound = pg.mixer.Sound('sounds/win.wav')
lose_sound = pg.mixer.Sound('sounds/lose.wav')

# Displaying State-1: Color choosing
state_1_displayed = False
human_color = None
state_1_title = medium_font.render('Press:', False, '#ffffff')
state_1_option_1 = small_font.render('W - To Play as WHITE!', False, '#ffffff')
state_1_option_2 = small_font.render('B - To Play as BLACK!', False, '#ffffff')

# Displaying State-2: Level choosing
state_2_displayed = False
ai_level = None
state_2_title = medium_font.render('Press:', False, '#ffffff')
state_2_option_1 = small_font.render('1 - To Play with a NOOB AI!', False, '#ffffff')
state_2_option_2 = small_font.render('2 - To Play with an EXPERT AI!', False, '#ffffff')
state_2_option_3 = small_font.render('3 - To Play with a PRO AI!', False, '#ffffff')

# Displaying State-3: Counting down
state_3_displayed = False
countdown_list = [3 - (i // 60) for i in range(180)]
countdown_index = 0

# Initializing Chess
bd = ch.Board()
colors = {
    'square light': '#eeeed2',
    'square dark': '#769656',
    'square light lastmove': '#baca44',
    'square dark lastmove': '#baca44'
}
need_update = True
fill_boxes = {}

# Moving by Human
possible_moves = []
fill_list = []
possible_moves_indices = []
previous_box = None

# Announcing the Results
announced = False

# Game Loop
while True:
    check_quit()
    if not state_1_displayed:
        (human_color, state_1_displayed) = display_state_1(human_color, state_1_displayed)
    elif not state_2_displayed:
        (ai_level, state_2_displayed) = display_state_2(ai_level, state_2_displayed)
    elif not state_3_displayed:
        (countdown_index, state_3_displayed) = display_state_3(countdown_index, state_3_displayed)
    elif not (bd.is_checkmate() or bd.is_stalemate()):
        if need_update:
            need_update = update_board(human_color, fill_boxes)
        if bd.turn == human_color:
            (fill_boxes,
             fill_list,
             possible_moves_indices,
             previous_box,
             possible_moves,
             need_update) = human_move(fill_boxes,
                                       fill_list,
                                       possible_moves_indices,
                                       previous_box,
                                       possible_moves)
            need_update = update_board(human_color, fill_boxes)
        else:
            need_update = ai_move()
    else:
        if not announced:
            announced = announce_results()
    pg.display.update()
    clock.tick(60)
