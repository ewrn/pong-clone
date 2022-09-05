import pygame, sys
import util
import pong_ball, pong_paddle

# Game Variables
pygame.init() # initialize pygame
screen = pygame.display.set_mode((900, 650)) # screen size
clock = pygame.time.Clock()
game_running = False

# Background
background_surface = pygame.image.load('assets/background.png').convert()

# Ball
ball_surface = pygame.image.load('assets/ball.png').convert_alpha()
ball = pong_ball.Ball(0, 0)
ball_rect = ball_surface.get_rect(center=(ball.x, ball.y))

# Paddle
paddle_surface = pygame.image.load('assets/paddle.png').convert()
paddle1 = pong_paddle.Paddle(0, 325, 0)
paddle2 = pong_paddle.Paddle(900, 325, 0)

paddle_rect_1 = paddle_surface.get_rect(midleft=(paddle1.x, paddle1.y))
paddle_rect_2 = paddle_surface.get_rect(midright=(paddle2.x, paddle2.y))

# Score
player_1_score = 0
player_2_score = 0
score_font = pygame.font.Font('assets/minecraft.ttf', 45)

# Instruction
instruction_font = pygame.font.Font('assets/minecraft.ttf', 25)

# Audio
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
collide_sound = pygame.mixer.Sound('assets/collide.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # quit program
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_running is False:
                # User press space to start the game
                ball.x_movement = util.generate_movement_speed()
                ball.y_movement = util.generate_movement_speed()
                game_running = True
            if event.key == pygame.K_w:
                # User press w key
                paddle1.movement = -10
            if event.key == pygame.K_s:
                # User press s key
                paddle1.movement = 10
            if event.key == pygame.K_UP:
                # User press up arrow key
                paddle2.movement = -10
            if event.key == pygame.K_DOWN:
                # User press down arrow key
                paddle2.movement = 10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                # User release w or s key
                paddle1.movement = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                # User release up or down arrow key
                paddle2.movement = 0

    # draw background
    screen.blit(background_surface, (0, 0))

    if game_running:
        # if ball hit boundary, bounce back from the wall
        if util.ball_hit_boundary(ball_rect):
            ball.y_movement *= -1
            collide_sound.play()

        # draw the ball moving
        ball.x += ball.x_movement
        ball.y += ball.y_movement
        util.draw_ball(screen, ball_rect, ball_surface, ball.x, ball.y)

        # draw the left paddle moving
        paddle1.y += paddle1.movement
        util.stop_paddle_out_of_bound(paddle1) # stops left paddle from going over boundary
        util.draw_paddle(screen, paddle_rect_1, paddle_surface, paddle1.x, paddle1.y, True)

        # draw the right paddle moving
        paddle2.y += paddle2.movement
        util.stop_paddle_out_of_bound(paddle2) # stops right paddle from going over boundary
        util.draw_paddle(screen, paddle_rect_2, paddle_surface, paddle2.x, paddle2.y, False)

        # if ball hit paddle, bounce back from paddle
        if util.check_collision(paddle_rect_1, paddle_rect_2, ball_rect):
            ball.x_movement *= -1
            collide_sound.play()

        # if ball goes out of bounds, add score
        winner = util.check_out_of_bound(ball_rect)
        if winner == 1:
            player_1_score += 1
            game_running = False
            ball.reset_ball_position()
        elif winner == 2:
            player_2_score += 1
            game_running = False
            ball.reset_ball_position()

    elif game_running is False:
        # draw starting position
        util.draw_ball(screen, ball_rect, ball_surface, ball.x, ball.y)

        # draw the left paddle moving
        paddle1.y += paddle1.movement
        util.stop_paddle_out_of_bound(paddle1) # stops left paddle from going over boundary
        util.draw_paddle(screen, paddle_rect_1, paddle_surface, paddle1.x, paddle1.y, True)

        # draw the right paddle moving
        paddle2.y += paddle2.movement
        util.stop_paddle_out_of_bound(paddle2) # stops right paddle from going over boundary
        util.draw_paddle(screen, paddle_rect_2, paddle_surface, paddle2.x, paddle2.y, False)

        # only show instruction when game is not active
        util.show_instructions(screen, instruction_font)

    # show score at all times
    util.show_scores(screen, score_font, player_1_score, player_2_score)

    pygame.display.update()
    clock.tick(120) # to control fps