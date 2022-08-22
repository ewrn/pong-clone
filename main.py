import pygame, sys, random
import pong_ball

def draw_paddle_1(paddle_1_x, paddle_1_y):
    paddle_rect_1.midleft = (paddle_1_x, paddle_1_y)
    screen.blit(paddle_surface, paddle_rect_1)


def draw_paddle_2(paddle_2_x, paddle_2_y):
    paddle_rect_2.midright = (paddle_2_x, paddle_2_y)
    screen.blit(paddle_surface, paddle_rect_2)


def draw_ball(ball_x, ball_y):
    ball_rect.center = (ball_x, ball_y)
    screen.blit(ball_surface, ball_rect)


def check_collision(paddle_rect_1, paddle_rect_2, ball_rect):
    if paddle_rect_2.colliderect(ball_rect) or paddle_rect_1.colliderect(ball_rect):
        return True


def ball_hit_boundary(ball_rect):
    if ball_rect.midtop[1] <= 0 or ball_rect.midbottom[1] >= 650:
        return True


def check_out_of_bound(ball_rect):
    if ball_rect.midright[0] <= 0:
        return 2 # Player 2 wins
    elif ball_rect.midright[0] >= 900:
        return 1 # Player 1 wins
    else:
        return 0


def generate_movement_speed():
    random_speed = [-7, -6.5, 6.5, 7]
    return random.choice(random_speed)


if __name__ == '__main__':
    # Game Variables
    pygame.init() # initialize pygame
    screen = pygame.display.set_mode((900, 650)) # screen size
    clock = pygame.time.Clock()
    game_running = False

    # Background
    background_surface = pygame.image.load('assets/background.png').convert()

    # Ball
    ball_surface = pygame.image.load('assets/ball.png').convert_alpha()
    ball = pong_ball.Ball(450, 325, 0, 0)
    ball_rect = ball_surface.get_rect(center=(ball.x, ball.y))

    # Paddle
    paddle_surface = pygame.image.load('assets/paddle.png').convert()

    paddle_1_x = 0
    paddle_1_y = 325
    paddle_rect_1 = paddle_surface.get_rect(midleft=(paddle_1_x, paddle_1_y))
    paddle_1_movement = 0

    paddle_2_x = 900
    paddle_2_y = 325
    paddle_rect_2 = paddle_surface.get_rect(midright=(paddle_2_x, paddle_2_y))
    paddle_2_movement = 0

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
                if event.key == pygame.K_SPACE and game_running is False: # User press space to start the game
                    ball.x_movement = generate_movement_speed()
                    ball.y_movement = generate_movement_speed()
                    game_running = True
                if event.key == pygame.K_w:
                    paddle_1_movement = -10
                if event.key == pygame.K_s:
                    paddle_1_movement = 10
                if event.key == pygame.K_UP:
                    paddle_2_movement = -10
                if event.key == pygame.K_DOWN:
                    paddle_2_movement = 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    paddle_1_movement = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle_2_movement = 0

        # Background
        screen.blit(background_surface, (0, 0))

        if game_running:
            # Ball
            if ball_hit_boundary(ball_rect):
                # if ball hit boundary, bounce back
                ball.y_movement *= -1
                collide_sound.play()

            ball.x += ball.x_movement
            ball.y += ball.y_movement
            draw_ball(ball.x, ball.y)

            # Player 1 Paddle
            paddle_1_y += paddle_1_movement

            # Paddle Boundary
            if paddle_1_y >= 580:
                paddle_1_y = 580
            elif paddle_1_y <= 70:
                paddle_1_y = 70

            draw_paddle_1(paddle_1_x, paddle_1_y)

            # Player 2 Paddle
            paddle_2_y += paddle_2_movement

            # Paddle Boundary
            if paddle_2_y >= 580:
                paddle_2_y = 580
            elif paddle_2_y <= 70:
                paddle_2_y = 70

            draw_paddle_2(paddle_2_x, paddle_2_y)

            # Collision
            if check_collision(paddle_rect_1, paddle_rect_2, ball_rect):
                ball.x_movement *= -1
                collide_sound.play()

            # Ball goes out of bounds
            winner = check_out_of_bound(ball_rect)
            if winner == 1:
                player_1_score += 1
                game_running = False
                # reset ball's position
                ball.x = 450
                ball.y = 325
            elif winner == 2:
                player_2_score += 1
                game_running = False
                ball.x = 450
                ball.y = 325

        elif game_running is False:
            # draw starting position
            draw_ball(ball.x, ball.y)

            paddle_1_y += paddle_1_movement
            paddle_2_y += paddle_2_movement

            # Paddle Boundary
            if paddle_1_y >= 580:
                paddle_1_y = 580
            elif paddle_1_y <= 70:
                paddle_1_y = 70

            if paddle_2_y >= 580:
                paddle_2_y = 580
            elif paddle_2_y <= 70:
                paddle_2_y = 70

            draw_paddle_1(paddle_1_x, paddle_1_y)
            draw_paddle_2(paddle_2_x, paddle_2_y)

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