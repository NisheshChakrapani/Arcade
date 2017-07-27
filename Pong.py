import pygame
from random import randint

pygame.init()
pygame.mixer.init()

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)

windowSize = (800, 600)
screen = pygame.display.set_mode(windowSize)

agencyFB = pygame.font.SysFont("Agency FB", 40)
textColor = (66, 244, 78)
textColor2 = (255,0,0)
clock = pygame.time.Clock()
running = 1

player_one_score = 0
player_two_score = 0

# Paddle size: 16x50
paddle_width = 16
paddle_height = 50
paddle_color = (0,255,255)

paddle_one_x = 2
paddle_one_y = int((windowSize[1]/2)-(paddle_height/2))

paddle_two_x = int(windowSize[0]-2-paddle_width)
paddle_two_y = int((windowSize[1]/2)-(paddle_height/2))

ball_radius = 10
ball_color = (255,255,0)
ball_x_speed = 5
direction = randint(0,1)
if direction == 0:
    ball_x_speed*=-1
ball_y_speed = 5
ball_x = int((windowSize[0]/2)-ball_radius)
ball_y = int((windowSize[1]/2)-ball_radius)

pygame.mouse.set_visible(0)

rally_count = 0
speed_updated = 0
moved = 0
difficulty = 1

# TODO: Add angle of bounce depending on where on the paddle the ball hits

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

        if event.type == pygame.MOUSEMOTION:
            coordinates = pygame.mouse.get_pos()
            paddle_one_y = coordinates[1]
            if paddle_one_y < 0:
                paddle_one_y = 0
            elif paddle_one_y > screen.get_height() - paddle_height:
                paddle_one_y = screen.get_height() - paddle_height

    if paddle_two_y < 0:
        paddle_two_y = 0
    elif paddle_two_y > screen.get_height() - paddle_height:
        paddle_two_y = screen.get_height() - paddle_height

    screen.fill((0,0,0))

    score_label_1 = agencyFB.render("SCORE: " + str(player_one_score), 1, textColor, (0,0,0))
    score_label_2 = agencyFB.render("SCORE: " + str(player_two_score), 1, textColor, (0,0,0))
    rally_count_label = agencyFB.render("Rally Count: " + str(rally_count), 1, textColor2, (0,0,0))
    screen.blit(score_label_1, (30, 0))
    screen.blit(score_label_2, (650, 0))
    screen.blit(rally_count_label, (265, 0))

    pygame.draw.circle(screen, ball_color, [int(ball_x),int(ball_y)], ball_radius, 0)
    pygame.draw.rect(screen, paddle_color, [paddle_one_x,paddle_one_y,paddle_width,paddle_height], 0)
    pygame.draw.rect(screen, paddle_color, [paddle_two_x, paddle_two_y, paddle_width, paddle_height], 0)

    paddle_one_hitbox = pygame.Rect(paddle_one_x, paddle_one_y, paddle_width, paddle_height)
    paddle_two_hitbox = pygame.Rect(paddle_two_x, paddle_two_y, paddle_width, paddle_height)
    ball_hitbox = pygame.Rect(ball_x-ball_radius, ball_y-ball_radius, ball_radius*2, ball_radius*2)

    if ball_y > screen.get_height() - ball_radius or ball_y < ball_radius:
        ball_y_speed*=-1

    if ball_x > screen.get_width() - ball_radius:
        rally_count = 0
        ball_x_speed = -5
        ball_y_speed = 5
        ball_x = int((windowSize[0] / 2) - ball_radius)
        ball_y = int((windowSize[1] / 2) - ball_radius)
        pygame.time.wait(3000)
        paddle_two_x = int(windowSize[0] - 2 - paddle_width)
        paddle_two_y = int((windowSize[1] / 2) - (paddle_height / 2))
        player_one_score += 1
    elif ball_x < ball_radius:
        rally_count = 0
        ball_x_speed = 5
        ball_y_speed = 5
        ball_x = int((windowSize[0] / 2) - ball_radius)
        ball_y = int((windowSize[1] / 2) - ball_radius)
        pygame.time.wait(3000)
        paddle_two_x = int(windowSize[0] - 2 - paddle_width)
        paddle_two_y = int((windowSize[1] / 2) - (paddle_height / 2))
        player_two_score += 1

    # AI Functionality
    if ball_x_speed > 0 and ball_x >= 500 and moved == 0:
        if paddle_two_y + (paddle_height/2) < ball_y:
            paddle_two_y += 7*difficulty
        elif paddle_two_y + (paddle_height/2) > ball_y:
            paddle_two_y -= 7*difficulty
        moved = 1

    if ball_hitbox.colliderect(paddle_one_hitbox) or ball_hitbox.colliderect(paddle_two_hitbox):
        rally_count+=1
        if ball_hitbox.collidepoint(paddle_one_hitbox.midtop) or ball_hitbox.collidepoint(
                paddle_one_hitbox.midbottom) or ball_hitbox.collidepoint(
                paddle_two_hitbox.midtop) or ball_hitbox.collidepoint(paddle_two_hitbox.midbottom):
            ball_y_speed*=-1
        else:
            ball_x_speed = -ball_x_speed

    ball_x += ball_x_speed
    ball_y += ball_y_speed

    if rally_count % 5 == 1:
        speed_updated = 0

    if rally_count % 5 == 0 and rally_count > 0 and speed_updated == 0:
        ball_x_speed *= 1.2
        speed_updated = 1

    moved = 0

    pygame.display.update()