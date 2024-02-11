from dataclasses import dataclass
import pygame


@dataclass
class Ball:
    x: int
    y: int
    vx: int
    vy: int


@dataclass
class Bar:
    w: int = 100
    h: int = 10
    b: int = 50  # margin bottom

    @property
    def x(self):
        return pygame.mouse.get_pos()[0] - self.w / 2

    @property
    def y(self):
        return screen.get_height() - self.h / 2 - self.b


width = 640
height = 480
dt = 0
sleep_seconds = 3
ball_p = (width / 2, height / 2)
ball_v = (100, 200)
running = True

pygame.init()
init = True
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

ball = Ball(*ball_p, *ball_v)
bar = Bar()


def outside_screen_x(x: int) -> bool:
    return x < 0 or x > screen.get_width()


def outside_screen_y(y: int) -> bool:
    return y < 0 or y > screen.get_height()


def ball_hits_bar_x(ball: Ball, bar: Bar) -> bool:
    return ball.x > bar.x and ball.x < bar.x + bar.w


def ball_hits_bar_y(ball: Ball, bar: Bar) -> bool:
    return ball.y > bar.y and ball.y < bar.y + bar.h


def ball_hits_bar(ball: Ball, bar: Bar) -> bool:
    return ball_hits_bar_x(ball, bar) and ball_hits_bar_y(ball, bar)


def move_ball(ball: Ball) -> None:
    ball.x += ball.vx * dt
    ball.y += ball.vy * dt


time_passed = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000
    screen.fill("white")

    pygame.draw.rect(screen, "black", (bar.x, bar.y, bar.w, bar.h))
    pygame.draw.circle(screen, "black", (ball.x, ball.y), 5)
    pygame.display.flip()

    if time_passed < sleep_seconds:
        time_passed += dt
        continue

    move_ball(ball)

    if outside_screen_x(ball.x):
        ball.vx *= -1
    if outside_screen_y(ball.y):
        ball.vy *= -1
    if ball_hits_bar(ball, bar):
        ball.vy *= -1


pygame.quit()
