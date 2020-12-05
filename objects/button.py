from typing import Callable

import pygame

from constants import Color, MAIN_FONT
from third_party.button import Button
from objects.base import DrawableObject


class ButtonObject(DrawableObject):
    def __init__(self, game,
                 x: int, y: int, width: int, height: int,
                 function: Callable[[None], None] = None,
                 text: str = 'Define me!',
                 button_type: str = 'multi',
                 color: pygame.color.Color = None) -> None:
        super().__init__(game)
        # if color is None:
        #     color = self.game.settings[button_type + '_btn_style']["bg_color"]
        button_style = {
            "hover_color": self.game.settings[button_type + '_btn_style']["hover_color"],
            "clicked_color": self.game.settings[button_type + '_btn_style']["clicked_color"],
            "font_color": self.game.settings[button_type + '_btn_style']["font_color"],
            "clicked_font_color": self.game.settings[button_type + '_btn_style']["clicked_font_color"],
            "hover_font_color": self.game.settings[button_type + '_btn_style']["hover_font_color"],
            "font": pygame.font.SysFont(self.game.settings[button_type + '_btn_style']["font"],
                                        self.game.settings[button_type + '_btn_style']["font_size"],
                                        self.game.settings[button_type + '_btn_style']["font_bold"],
                                        self.game.settings[button_type + '_btn_style']["font_italic"], )
        }
        self.color = color if color else self.game.settings[button_type + '_btn_style']["bg_color"]
        self.function = function if function else ButtonObject.no_action
        self.text = text
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.button = Button(
            rect=self.rect,
            color=self.color,
            function=self.function,
            text=self.text,
            **button_style
        )

    def set_center(self, x: int, y: int) -> None:
        super(ButtonObject, self).set_center(x, y)
        self.button.rect = self.rect

    def set_position(self, x: int, y: int) -> None:
        super().set_position(x, y)
        self.button.rect = self.rect

    @staticmethod
    def no_action() -> None:
        pass

    def set_text(self, text) -> None:
        self.text = text
        self.button.text = text
        self.button.render_text()

    def process_event(self, event) -> None:
        self.button.check_event(event)

    def process_draw(self) -> None:
        self.button.update(self.game.screen)
