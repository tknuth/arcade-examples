from dataclasses import dataclass
from arcade.color import BLACK, WHITE
import arcade


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 320
SCREEN_TITLE = "Ping Pong"
SLEEP_SECONDS = 3
BALL_POSITION = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
BALL_VELOCITY = (3, 5)


@dataclass
class Ball:
    x: int
    y: int
    vx: int
    vy: int
    r: int = 5

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, BLACK)


@dataclass
class Bar:
    x: int = SCREEN_WIDTH / 2
    w: int = 100
    h: int = 10
    b: int = 50  # margin bottom

    @property
    def y(self):
        return self.h / 2 + self.b

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.w, self.h, BLACK)


def outside_screen_x(x: int) -> bool:
    return x < 0 or x > SCREEN_WIDTH


def outside_screen_y(y: int) -> bool:
    return y < 0 or y > SCREEN_HEIGHT


def ball_hits_bar_x(ball: Ball, bar: Bar) -> bool:
    return ball.x < bar.x + bar.w / 2 and ball.x > bar.x - bar.w / 2


def ball_hits_bar_y(ball: Ball, bar: Bar) -> bool:
    return ball.y < bar.y + bar.h / 2 and ball.y > bar.y - bar.h / 2


def ball_hits_bar(ball: Ball, bar: Bar) -> bool:
    return ball_hits_bar_x(ball, bar) and ball_hits_bar_y(ball, bar)


def move_ball(ball: Ball) -> None:
    ball.x += ball.vx
    ball.y += ball.vy


def handle_collision(ball: Ball, bar: Bar) -> None:
    if outside_screen_x(ball.x):
        ball.vx *= -1
    if outside_screen_y(ball.y):
        ball.vy *= -1
    if ball_hits_bar(ball, bar):
        ball.vy *= -1


class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.set_mouse_visible(False)
        arcade.set_background_color(WHITE)

    def setup(self):
        self.ball = Ball(*BALL_POSITION, *BALL_VELOCITY)
        self.bar = Bar()

    def on_draw(self):
        self.clear()

        self.bar.draw()
        self.ball.draw()

        move_ball(self.ball)
        handle_collision(self.ball, self.bar)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.bar.x = x - self.bar.w / 2


def main():
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
