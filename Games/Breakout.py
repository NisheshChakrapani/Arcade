import pygame, random, math

class Brick:
    def __init__(self, position, powerup, color):
        self.position = position
        self.powerup = powerup
        self.color = color

        if powerup:
            image = pygame.image.load("Explode.png")
        else:
            image = pygame.image.load("brick.png")

        self.image = image

        self.x = position[0]
        self.y = position[1]
        self.rect = pygame.Rect(self.x, self.y, 50, 16)
        self.top_rect = pygame.Rect(self.x, self.y, 50, 1)
        self.bottom_rect = pygame.Rect(self.x, self.y+16, 50, 1)

class BrickArray:
    def __init__(self, num_rows, powerup_prob):
        self.num_rows = num_rows
        self.__powerup_prob = powerup_prob
        self.load_bricks()

    def load_bricks(self):
        self.brick_array = []

        colors = []
        for i in range(1, self.num_rows):
            brick_row = []
            rand = random.randint(0, 9)
            while rand in colors:
                rand = random.randint(1, 9)
            colors.append(rand)
            for j in range(0, 13):
                if rand == 1:
                    color = (155, 0, 0)
                elif rand == 2:
                    color = (0, 255, 0)
                elif rand == 3:
                    color = (0, 0, 255)
                elif rand == 4:
                    color = (255, 255, 0)
                elif rand == 5:
                    color = (255, 0, 255)
                elif rand == 6:
                    color = (0, 255, 255)
                elif rand == 7:
                    color = (135, 0, 255)
                elif rand == 8:
                    color = (255, 135, 0)
                elif rand == 9:
                    color = (195, 0, 195)

                if random.uniform(0, 1) < self.__powerup_prob and self.num_rows - 1 > i > 1 and 12 > j > 0:
                    brick = Brick((50*j, 16*i), self.__powerup_prob, color)
                else:
                    brick = Brick((50*j, 16*i), 0, color)
                brick_row.append(brick)
            self.brick_array.append(brick_row)


class Breakout:
    def __init__(self, difficulty):
        if not isinstance(difficulty, int):
            raise ValueError('Difficulty must be an integer')
        elif difficulty < 1 or difficulty > 3:
            raise ValueError('Difficulty must be between 1 and 3')
        self.__difficulty = difficulty
        self.play_game()

    def play_game(self):
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)
        pygame.init()
        agencyFB = pygame.font.SysFont("Agency FB", 40)
        bricks = BrickArray((3*(self.__difficulty)+1), (0.1/self.__difficulty))

        screen = pygame.display.set_mode([650, 480])
        running = 1
        clock = pygame.time.Clock()
        gameLives = 0
        ball_x = 50
        ball_y = 250
        ball_radius = 10
        ball_color = [220, 50, 50]
        ball_speed_x = self.__difficulty*2
        ball_speed_y = self.__difficulty*2+2
        ball_angle = 0

        paddle_x = 120
        paddle_y = 450
        paddle_width = 60
        paddle_height = 20
        paddle_color = [20, 180,180]
        score = 0

        pygame.mouse.set_visible(0)
        waiting = 0

        pygame.time.wait(3000)
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                if event.type == pygame.MOUSEMOTION:
                    coordinates = pygame.mouse.get_pos()  # gives (x,y) coordinates
                    paddle_x = coordinates[0] - paddle_width/2
                    if paddle_x < 0:
                       paddle_x = 0
                    if paddle_x > screen.get_width() - paddle_width:
                        paddle_x = screen.get_width() - paddle_width

            screen.fill((0, 0, 0))

            if ball_y > screen.get_height() - ball_radius:
                gameLives+=1
                ball_x = 50
                ball_y = 250
                ball_speed_x = self.__difficulty*2
                ball_speed_y = self.__difficulty*2+2
                paddle_x = 150
                paddle_y = 450
                pygame.time.wait(1000)

            # check if the ball hit the top of the screen
            if ball_y < 0:
                ball_speed_y*=-1
            # check if the ball hit the left side of the screen
            if ball_x < 0:
                ball_speed_x*=-1
            # check if the ball hit the right side of the screen
            if ball_x > screen.get_width() - ball_radius:
                ball_speed_x*=-1

            ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
            paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)

            pygame.draw.circle(screen, ball_color, [int(ball_x), int(ball_y)], ball_radius, 0)
            pygame.draw.rect(screen, paddle_color, [paddle_x, paddle_y, paddle_width, paddle_height], 0)
            #pygame.draw.rect(screen, (255,0,0), paddle_rect, 2)

            if ball_rect.collidepoint(paddle_rect.midleft) or ball_rect.collidepoint(paddle_rect.midright):
                ball_speed_x*=-1
            elif ball_rect.colliderect(paddle_rect):
                ball_speed_y*=-1
                ball_angle = 90 + (paddle_rect.midtop[0] - ball_rect.midbottom[0])
                ball_speed_x = 0
                ball_speed_x = math.cos(ball_angle)*5
                if ball_angle < 90:
                    ball_speed_x = abs(ball_speed_x)
                elif ball_angle > 90:
                    ball_speed_x = -abs(ball_speed_x)

            for row_index in range(0, len(bricks.brick_array)):
                for column_index in range(0, len(bricks.brick_array[row_index])):
                    brick = bricks.brick_array[row_index][column_index]
                    if brick is not None and brick.rect.colliderect(ball_rect):
                        if brick.powerup:
                            if bricks.brick_array[row_index][column_index] is not None:
                                bricks.brick_array[row_index][column_index] = None
                                score += 1
                            if row_index > 0 and bricks.brick_array[row_index - 1][column_index] is not None:
                                bricks.brick_array[row_index - 1][column_index] = None
                                score += 1
                            if row_index < bricks.num_rows - 1:
                                if bricks.brick_array[row_index + 1][column_index] is not None:
                                    bricks.brick_array[row_index + 1][column_index] = None
                                    score += 1
                            if column_index > 0 and bricks.brick_array[row_index][column_index - 1] is not None:
                                bricks.brick_array[row_index][column_index - 1] = None
                                score += 1
                            if column_index < 2 and bricks.brick_array[row_index][column_index + 1] is not None:
                                bricks.brick_array[row_index][column_index + 1] = None
                                score += 1
                        else:
                            score += 1
                            bricks.brick_array[row_index][column_index] = None

                        if brick.rect.collidepoint(ball_rect.midleft) or brick.rect.collidepoint(ball_rect.midright):
                            ball_speed_x*=-1
                        else:
                            if brick.bottom_rect.colliderect(ball_rect):
                                ball_speed_y = abs(ball_speed_y)
                                ball_y -= 10
                            else:
                                ball_speed_y = -abs(ball_speed_y)
                        continue
                    continue

            score_label = agencyFB.render("Score: " + str(score), 1, (0,255,0))
            lives_label = agencyFB.render("Deaths: " + str(gameLives), 1, (0,255,0))
            screen.blit(score_label, (10, 200))
            screen.blit(lives_label, (510, 200))
            for row in bricks.brick_array:
                for brick in row:
                    if brick is not None:
                        if brick.powerup:
                            screen.blit(brick.image, brick.rect)
                        else:
                            pygame.draw.rect(screen, brick.color, brick.rect, 0)

            ball_y = ball_y + ball_speed_y
            ball_x = ball_x + ball_speed_x

            pygame.display.update()

            max_score = (bricks.num_rows-1)*13
            if score == max_score:
                win_label = agencyFB.render("You win!", 1, (0,255,0))
                screen.blit(win_label, (200, 200))
                running = 0

        pygame.time.wait(2000)