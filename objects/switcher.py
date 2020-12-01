import pygame


from objects.base import DrawableObject
from objects.button import ButtonObject
from objects.text import TextObject


class ArrowSwitcher(DrawableObject):
    def __init__(self, game,
                 x: int, y: int, width: int, height: int,
                 text_color: pygame.color.Color = (255, 255, 255),
                 color: pygame.color.Color = None,
                 start_index: int = 0, *args) -> None:
        super().__init__(game)
        self.values = args
        self.current_index = start_index
        self.color = color
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.text_area = TextObject(
            game,
            'Consolas', 32, True, False,
            self.values[self.current_index],
            text_color,
            x + width // 2, y + height // 2
        )
        self.button_back = ButtonObject(
            self.game,
            x, y, 50, height,
            color=self.color,
            function=self.switch_back,
            text="<"
        )
        self.button_next = ButtonObject(
            self.game,
            x + width - 50, y, 50, height,
            color=self.color,
            function=self.switch_next,
            text=">"
        )

    def switch_back(self) -> None:
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.values) - 1
        self.set_text(self.values[self.current_index])

    def switch_next(self) -> None:
        self.current_index += 1
        if self.current_index > len(self.values)-1:
            self.current_index = 0
        self.set_text(self.values[self.current_index])

    def set_center(self, x: int, y: int) -> None:
        super(self).set_center(x, y)
        self.text_area.rect = self.rect
        self.button_back.rect = self.rect
        self.button_next.rect = self.rect

    def set_position(self, x: int, y: int) -> None:
        super().set_position(x, y)
        self.text_area.rect = self.rect
        self.button_back.rect = self.rect
        self.button_next.rect = self.rect

    def switch_to(self, new_index):
        if 0 <= new_index < len(self.values):
            self.current_index = new_index
            self.set_text(self.values[new_index])

    def set_text(self, text) -> None:
        self.text = text
        self.text_area.text = text
        self.text_area.update_text(text)

    def process_event(self, event) -> None:
        self.button_back.process_event(event)
        self.button_next.process_event(event)

    def process_draw(self) -> None:
        self.text_area.process_draw()
        self.button_back.process_draw()
        self.button_next.process_draw()

    def get_current_value(self) -> str:
        return self.values[self.current_index]

