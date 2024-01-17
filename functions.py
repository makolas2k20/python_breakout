# =============================================================================
# Game Logic + Physics
# Author: Michael Sumaya
# =============================================================================
import pygame as gm
import pygame.freetype as ftype
import sys
from pygame.sprite import Group, GroupSingle

# Custom modules
import functions as gfn
from settings import Settings
from paddle import Paddle
from targets import Target
from score import Scoring
from game_events import GameEvents


def block_events():
    blocked_events = [
        gm.MOUSEMOTION,
    ]
    gm.event.set_blocked(blocked_events)


def check_events(
        screen: gm.Surface,
        settings: Settings,
        paddle: Paddle,
        ball: GroupSingle,
        scoreboard: Scoring,
        eventhndl: GameEvents,
) -> None:
    for event in gm.event.get():
        if event.type == gm.QUIT:
            scoreboard._save_highscore()
            gm.quit()
            sys.exit()

        elif event.type == gm.KEYDOWN:
            check_events_keydown(
                screen,
                settings,
                paddle,
                ball,
                event,
            )

        elif event.type == gm.KEYUP:
            check_events_keyup(
                screen,
                settings,
                paddle,
                ball,
                event,
            )

        else:
            eventhndl.parse_event(
                event.type,
                scoreboard=scoreboard,
            )


def check_events_keydown(
        screen: gm.Surface,
        settings: Settings,
        paddle: Paddle,
        ball: GroupSingle,
        event: gm.event.Event,
) -> None:
    if event.key in settings.event_key_left:
        paddle.ismoving_left = True
    elif event.key in settings.event_key_right:
        paddle.ismoving_right = True
    else:
        # Ignore
        pass


def check_events_keyup(
        screen: gm.Surface,
        settings: Settings,
        paddle: Paddle,
        ball: GroupSingle,
        event: gm.event.Event,
) -> None:
    if event.key in settings.event_key_left:
        paddle.ismoving_left = False
    elif event.key in settings.event_key_right:
        paddle.ismoving_right = False
    elif event.key == gm.K_SPACE:
        if ball.sprite.isDropped:
            ball.sprite.isDropped = False
    else:
        # Ignore
        pass


def draw_field(
        screen: gm.Surface,
        settings: Settings,
) -> None:
    gm.draw.rect(
        surface=screen,
        color=settings.field_border_color,
        rect=settings.field_rect,
        width=settings.field_border_width,
    )


def draw_fps(
        screen: gm.Surface,
        fps: float,
) -> None:
    fps_font = ftype.SysFont("ubuntumono", 18)
    fps_val = round(fps, 0)
    xpos = 10
    ypos = screen.get_rect().bottom - 25
    fps_font.render_to(
        screen,
        (xpos, ypos),
        f"FPS: {fps_val}",
        fgcolor=(0, 255, 0),
    )


def draw_prompt(
        screen: gm.Surface,
        settings: Settings.Prompt,
        message: str,
        color: any,
) -> None:
    prompt = ftype.SysFont(settings.font_type, settings.size)
    screen_rect = screen.get_rect()
    prompt_scr, prompt_rect = prompt.render(
        message,
        fgcolor=color,
    )
    prompt_rect.centerx = screen_rect.centerx
    prompt_rect.centery = screen_rect.centery + 50
    screen.blit(prompt_scr, prompt_rect)



def create_targets(
        screen: gm.Surface,
        settings: Settings,
) -> [Group, float]:
    target_collection = Group()
    # Calculate max targets per row based on screen width
    target_template = Target(screen, settings)
    screen_rect = screen.get_rect()
    max_columns = (screen_rect.width // target_template.rect.width) - 1
    spacer = target_template.rect.width // max_columns
    # Create targets up to max rows in settings
    max_rows = settings.target_rows
    y_offset = settings.field_ypos

    for row in range(0, max_rows):
        for col in range(0, max_columns):
            add_target(
                screen,
                settings,
                row,
                col,
                spacer,
                y_offset,
                target_collection,
            )

    bottom_ypos = ((target_template.rect.height * (max_rows + 1))
                   + (max_rows * spacer)
                   + y_offset)
    return target_collection, bottom_ypos


def add_target(
        screen: gm.Surface,
        settings: Settings,
        row: int,
        col: int,
        spacer: int,
        y_offset,
        target_collection: Group,
) -> None:
    target = Target(screen, settings)
    width = target.rect.width
    height = target.rect.height
    xspacer = ((col + 1) * spacer)
    yspacer = ((row + 1) * spacer)
    target.move(
        xpos=(col * width) + xspacer,
        ypos=y_offset + (row * height) + yspacer,
    )
    target_collection.add(target)


def update_targets(
        ball: GroupSingle,
        targets: Group,
        scoreboard: Scoring,
) -> None:
    HIT_THRESHOLD = ball.sprite.speed
    # Check collision with ball
    collisions = gm.sprite.groupcollide(
        ball,
        targets,
        False,
        True,
    )
    if collisions:
        # Update score
        scoreboard.add_combo()

        # Check how to bounce
        for ball_c, target_c in collisions.items():
            for target in target_c:
                ball_rect = ball_c.rect
                target_rect = target.rect
                ball.sprite.color = target.color
                # Ball hits above/below
                if ((abs(ball_rect.bottom - target_rect.top) <= HIT_THRESHOLD
                     and ball.sprite.diry > 0)
                        or (abs(ball_rect.top - target_rect.bottom) <= HIT_THRESHOLD
                            and ball.sprite.diry < 0)):
                    ball.sprite.bounce_y()
                # If ball hits the sides
                if ((abs(ball_rect.right - target_rect.left) <= HIT_THRESHOLD
                    and ball.sprite.dirx > 0)
                    or (abs(ball_rect.left - target_rect.right) <= HIT_THRESHOLD
                        and ball.sprite.dirx < 0)):
                    ball.sprite.bounce_x()


def new_level(
        screen: gm.Surface,
        settings: Settings,
        ball: GroupSingle,
) -> Group:
    targets, bottom_y = gfn.create_targets(
        screen,
        settings,
    )
    ball.sprite.move(
        ball.sprite.rect.centerx,
        bottom_y + ball.sprite.rect.height,
    )
    return targets


def update_screen(
        screen: gm.Surface,
        settings: Settings,
        paddle: Paddle,
        ball: GroupSingle,
        targets: Group,
        fps: float,
        scoreboard: Scoring,
        eventhndl: GameEvents,
) -> None:
    # Flood screen to clear all drawings
    screen.fill(settings.screen_bgcolor)

    # Redraw playing field
    draw_field(screen, settings)

    # Update paddle
    paddle.update()

    # Update ball
    ball.update(paddle)
    if ball.sprite.paddle_hit:
        scoreboard.reset_combo_point()

    # Targets
    targets.update()

    # Show FPS
    if settings.show_fps:
        draw_fps(screen, fps)

    # Update scores
    scoreboard.update()

    # Check if ball dropped below paddle/screen
    if ball.sprite.isDropped:
        if scoreboard.update_scoreboardhigh():
            eventhndl.start_event_newhigh(250, 6)
        ball.sprite.ball_dropped()
        paddle.to_center()
        draw_prompt(
            screen,
            settings.Prompt,
            "Press 'spacebar' to continue.",
            settings.Prompt.COLOR_WARNING,
        )

    gm.display.flip()
