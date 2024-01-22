# =============================================================================
# Custom Game Events
# Author: Michael Sumaya
# =============================================================================
import pygame as gm


class GameEvents():
    """Custom Event Handler"""

    # Maintain custom events function name here
    EVENT_LIST = (
        "event_newhigh",
    )

    def __init__(
            self,
            screen: gm.Surface,
    ) -> None:
        self.screen = screen
        self.user_event_count = gm.USEREVENT
        self.eventdict = self._load_events()

    def _load_events(self) -> dict:
        loaded_events = {}
        for event in self.EVENT_LIST:
            self._add_event(event, self.user_event_count, loaded_events)
        return loaded_events

    def _add_event(
            self,
            event_name: str,
            event_counter: int,
            eventdict: dict,
    ) -> int:
        event_counter += 1
        eventdict[event_name] = event_counter
        return event_counter

    def parse_event(
            self,
            event_type: int,
            **kwargs
    ) -> None:
        """Check custom events dictionary"""
        for key, val in self.eventdict.items():
            if event_type == val:
                self.execute(key, **kwargs)

    def execute(
            self,
            event_name,
            **kwargs
    ) -> None:
        """Call event_name as a function"""
        try:
            exec_fxn = getattr(self, event_name)
            exec_fxn(**kwargs)
        except:
            print(f"Unhandled event: {event_name}")

    # Custom functions based on list
    def start_event_newhigh(
            self,
            millis: int,
            loops: int,
    ) -> None:
        """Triggers event when user reached new high score
        - millis: Millisecond delay before executing logic
        - loops: How many times to repeat (needed for blink effect);
        must be multiple of 2
        """
        self.newhigh_counter = loops
        gm.time.set_timer(self.eventdict["event_newhigh"], millis, loops)

    def event_newhigh(
            self,
            **kwargs
    ) -> None:
        HIGHSCORE_HIGHLIGHT_COLOR = "red"
        scoreboard = kwargs["scoreboard"]
        if not scoreboard.settings.Font.color_high == HIGHSCORE_HIGHLIGHT_COLOR:
            self.newhigh_oldcolor = scoreboard.settings.Font.color_high
        if self.newhigh_counter % 2:
            scoreboard.settings.Font.color_high = self.newhigh_oldcolor
        else:
            scoreboard.settings.Font.color_high = HIGHSCORE_HIGHLIGHT_COLOR
        if self.newhigh_counter == 1:
            screen = kwargs["screen"]
            settings = kwargs["settings"]
            if settings.save_screenshot:
                gm.image.save(screen, f"highscore_{scoreboard.score_high}.png")
        self.newhigh_counter -= 1
