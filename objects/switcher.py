import pygame

from constants import Color, MAIN_FONT
from objects import ButtonObject
from third_party.button import Button


class ArrowSwitcher(ButtonObject):
    def __init__(self, game,
                 x: int, y: int, width: int, height: int,
                 color: pygame.color.Color = None,
                 start_index: int = 0, *args) -> None:
        self.arguments = args
        self.args_index = start_index
        self.all_rect = pygame.rect.Rect(x, y, width, height)
        self.mid_rect = pygame.rect.Rect(x + width // 4, y, width // 2, height)
        self.left_rect = pygame.rect.Rect(x, y, width // 4, height)
        self.right_rect = pygame.rect.Rect(x + (width // 4 * 3), y, width // 4, height)
        super().__init__(game, x + width // 4, y, width // 2, height, color, None, args[start_index])
        self.left_button = Button(
            rect=self.left_rect,
            color=self.color,
            function=self.dec_arg,
            text="<",
            **self.BUTTON_STYLE
        )
        self.right_button = Button(
            rect=self.right_rect,
            color=self.color,
            function=self.inc_arg,
            text=">",
            **self.BUTTON_STYLE
        )

    def dec_arg(self) -> None:
        self.args_index -= 1
        if self.args_index < 0:
            self.args_index = len(self.arguments)-1
        self.set_text(self.arguments[self.args_index])

    def inc_arg(self) -> None:
        self.args_index += 1
        if self.args_index > len(self.arguments)-1:
            self.args_index = 0
        self.set_text(self.arguments[self.args_index])

    def set_center(self, x: int, y: int) -> None:
        super(ButtonObject, self).set_center(x, y)
        self.button.rect = self.rect
        self.left_button.rect = self.rect
        self.right_button.rect = self.rect

    def set_position(self, x: int, y: int) -> None:
        super().set_position(x, y)
        self.button.rect = self.rect
        self.left_button.rect = self.rect
        self.right_button.rect = self.rect

    def set_text(self, text) -> None:
        self.text = text
        self.button.text = text
        self.button.render_text()

    def process_event(self, event) -> None:
        self.left_button.check_event(event)
        self.right_button.check_event(event)

    def process_draw(self) -> None:
        self.button.update(self.game.screen)
        self.left_button.update(self.game.screen)
        self.right_button.update(self.game.screen)
