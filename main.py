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

    # Background
    screen.blit(background_surface, (0, 0))

    if game_running:
        # Ball
        if util.ball_hit_boundary(ball_rect):
            # if ball hit boundary, bounce back
            ball.y_movement *= -1
            collide_sound.play()

        ball.x += ball.x_movement
        ball.y += ball.y_movement
        util.draw_ball(screen, ball_rect, ball_surface, ball.x, ball.y)

        # Player 1 Paddle
        paddle1.y += paddle1.movement

        # Paddle Boundary
        if paddle1.y >= 580:
            paddle1.y = 580
        elif paddle1.y <= 70:
            paddle1.y = 70

        util.draw_paddle(screen, paddle_rect_1, paddle_surface, paddle1.x, paddle1.y, True)

        # Player 2 Paddle
        paddle2.y += paddle2.movement

        # Paddle Boundary
        if paddle2.y >= 580:
            paddle2.y = 580
        elif paddle2.y <= 70:
            paddle2.y = 70

        util.draw_paddle(screen, paddle_rect_2, paddle_surface, paddle2.x, paddle2.y, False)

        # Collision
        if util.check_collision(paddle_rect_1, paddle_rect_2, ball_rect):
            ball.x_movement *= -1
            collide_sound.play()

        # Ball goes out of bounds
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

        paddle1.y += paddle1.movement
        paddle2.y += paddle2.movement

        # Paddle Boundary
        if paddle1.y >= 580:
            paddle1.y = 580
        elif paddle1.y <= 70:
            paddle1.y = 70

        if paddle2.y >= 580:
            paddle2.y = 580
        elif paddle2.y <= 70:
            paddle2.y = 70

        util.draw_paddle(screen, paddle_rect_1, paddle_surface, paddle1.x, paddle1.y, True)
        util.draw_paddle(screen, paddle_rect_2, paddle_surface, paddle2.x, paddle2.y, False)

        # Instruction
        # Only show instruction when game is not active
        instruction_surface = instruction_font.render(f'Press Space to Start!', True, (255, 255, 255))
        instruction_rect = instruction_surface.get_rect(center=(450, 500))
        screen.blit(instruction_surface, instruction_rect)

    # Score
    score_surface = score_font.render(f'{player_1_score}     SCORE     {player_2_score}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(450, 100))
    screen.blit(score_surface, score_rect)

    pygame.display.update()
    clock.tick(120) # to control fps