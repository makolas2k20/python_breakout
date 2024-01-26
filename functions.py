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
from life import Life
from soundsys import SoundSystem


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
        life: Life,
        sounds: SoundSystem,
) -> None:
    for event in gm.event.get():
        if event.type == gm.QUIT:
            scoreboard._save_highscore()
            sounds.quit()
            gm.quit()
            sys.exit()

        elif event.type == gm.KEYDOWN:
            check_events_keydown(
                screen,
                settings,
                paddle,
                ball,
                event,
                scoreboard,
                life,
            )

        elif event.type == gm.KEYUP:
            check_events_keyup(
                screen,
                settings,
                paddle,
                ball,
                event,
                scoreboard,
                life,
            )

        else:
            eventhndl.parse_event(
                event.type,
                screen=screen,
                settings=settings,
                scoreboard=scoreboard,
            )


def check_events_keydown(
        screen: gm.Surface,
        settings: Settings,
        paddle: Paddle,
        ball: GroupSingle,
        event: gm.event.Event,
        scoreboard: Scoring,
        life: Life,
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
        scoreboard: Scoring,
        life: Life,
) -> None:
    if event.key in settings.event_key_left:
        paddle.ismoving_left = False
    elif event.key in settings.event_key_right:
        paddle.ismoving_right = False
    elif event.key == gm.K_SPACE:
        if not settings.game_on and life.count > 0:
            settings.game_on = True
        elif settings.game_on and life.count == 0:
            reset_game(
                scoreboard,
                life,
            )

        if ball.sprite.isDropped:
            ball.sprite.isDropped = False
    else:
        # Ignore
        pass


def reset_game(
        scoreboard: Scoring,
        life: Life,
):
    scoreboard.reset_score()
    life.reset()


def draw_field(
        screen: gm.Surface,
        settings: Settings,
) -> None:
    screen.blit(
        settings.assets.wallpaper,
        settings.field_rect,
    )
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
    fps_font = ftype.SysFont(None, 12)
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
    prompt = ftype.Font(settings.font,
                        settings.size,)
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
) -> [Group, float, int]:
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

    max_count = max_columns * max_rows
    return target_collection, bottom_ypos, max_count


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
        settings: Settings,
        ball: GroupSingle,
        targets: Group,
        scoreboard: Scoring,
        sounds: SoundSystem,
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
        # Check how to bounce
        for ball_c, target_c in collisions.items():
            for target in target_c:
                # Play sound
                sounds.play_target()

                # Update score
                scoreboard.add_combo()
                ball_rect = ball_c.rect
                target_rect = target.rect
                if settings.ball_copy_target_color:
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
    targets, bottom_y, _ = gfn.create_targets(
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
        life: Life,
) -> None:
    # Flood screen to clear all drawings
    screen.fill(settings.screen_bgcolor)

    # Redraw playing field
    draw_field(screen, settings)

    # Update paddle
    paddle.update()

    # Update ball
    ball.update(paddle, life)
    if ball.sprite.paddle_hit:
        scoreboard.reset_combo_point()

    # Targets
    targets.update()

    # Show FPS
    if settings.show_fps:
        draw_fps(screen, fps)

    # Update scores
    scoreboard.update()

    # Update life status on screen
    life.update()

    # Check if ball dropped below paddle/screen
    if ball.sprite.isDropped:
        if settings.game_on:
            if scoreboard.update_scoreboardhigh():
                eventhndl.start_event_newhigh(250, 6)
            if life.count > 0:
                prompt_str = "Press 'spacebar' to continue."
                prompt_color = settings.Prompt.COLOR_WARNING
            else:
                prompt_str = "Game Over! Press 'spacebar' to restart."
                prompt_color = settings.Prompt.COLOR_ERROR
        else:
            prompt_str = "Press 'spacebar' to start."
            prompt_color = settings.Prompt.COLOR_NORMAL
        ball.sprite.ball_dropped()
        paddle.to_center()
        draw_prompt(
            screen,
            settings.Prompt,
            prompt_str,
            prompt_color,
        )

    gm.display.flip()
