import pygame


class AnimationPreset:
    def __init__(self, f_c, f_n):
        self.frames_count = f_c
        self.frame_name = f_n
        self.current_frame_index = 0
        self.frames_list = []
        self.generate_frames_list()

    def generate_frames_list(self):
        for i in range(self.frames_count):
            current_frame_name = self.frame_name.replace('[F]', str(i))
            frame = pygame.image.load(current_frame_name)
            self.frames_list.append(frame)

    def get_next_frame(self):
        self.current_frame_index = (self.current_frame_index + 1) % \
                                   self.frames_count
        return self.frames_list[self.current_frame_index]
