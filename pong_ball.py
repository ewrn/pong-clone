class Ball():
    x = 450
    y = 325
    x_movement = 0
    y_movement = 0

    # constructor
    def __init__(self, x_movement, y_movement):
        self.x_movement = x_movement
        self.y_movement = y_movement

    def reset_ball_position(self):
        self.x = 450
        self.y = 325
