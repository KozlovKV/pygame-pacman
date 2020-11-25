import datetime

import pygame


class BaseScene:
    def __init__(self, game) -> None:
        self.game = game
        self.screen = self.game.screen
        self.objects = []
        self.create_objects()

    def create_objects(self) -> None:
        pass

    def on_activate(self) -> None:
        pass

    def on_window_resize(self) -> None:
        pass

    def process_event(self, event: pygame.event.Event) -> None:
        # timer = datetime.datetime.now()
        for item in self.objects:
            item.process_event(event)
        self.additional_event_check(event)
        # delta = datetime.datetime.now() - timer
        # print(f'EVENT: {delta.total_seconds()}')

    def additional_event_check(self, event: pygame.event.Event) -> None:
        pass

    def process_logic(self) -> None:
        # timer = datetime.datetime.now()
        for item in self.objects:
            item.process_logic()
        self.additional_logic()
        # delta = datetime.datetime.now() - timer
        # print(f'LOGIC: {delta.total_seconds()}')

    def additional_logic(self) -> None:
        pass

    def process_draw(self) -> None:
        timer = datetime.datetime.now()
        for item in self.objects:
            item.process_draw()
        self.additional_draw()
        delta = datetime.datetime.now() - timer
        print(f'DRAWING: {delta.total_seconds()}')

    def additional_draw(self) -> None:
        pass

    def on_deactivate(self) -> None:
        pass
