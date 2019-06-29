import pygame
import logging


class MainMenu:
    def __init__(self, renderer):
        self.renderer = renderer
        self.log = logging.getLogger("main.menu.MainMenu")
        self.log.setLevel(logging.INFO)
        self.graphics = [[
            {"type": "bg", "colour": (255, 255, 255)}
        ],
            []  # list edited by self.resolution_change()
        ]
        self.resolution_change()

    def resolution_change(self):
        # get the display size
        resolution = pygame.display.get_surface()
        resolution = (resolution.get_width(), resolution.get_height())
        self.log.debug("resolution: " + str(resolution))

        # title
        title = self.renderer.fonts["main"].render(
            text="Anthropodemics",
            size=1000
        )
        title_size = title[1][2:]

        title = pygame.transform.scale(title[0], (
            resolution[0]//5*4,
            int(resolution[0]//5*4*title_size[1]/title_size[0])
        ))
        # get the new title size after transformation
        title_rect = title.get_rect()
        title_size = (title_rect.width, title_rect.height)

        # menu buttons
        # play
        play_button = pygame.Rect(
            resolution[0]//5*2,
            title_size[1] + 40,
            resolution[0]//5,
            50
        )
        play_text = self.renderer.fonts["main"].render(
            text="Play",
            size=40
        )[0]
        play_text_loc = play_text.get_rect(center=(resolution[0]/2, title_size[1] + 65))

        # options
        options_button = pygame.Rect(
            resolution[0] // 5 * 2,
            title_size[1] + 100,
            resolution[0] // 5,
            50
        )
        options_text = self.renderer.fonts["main"].render(
            text="Options",
            size=40
        )[0]
        options_text_loc = options_text.get_rect(center=(resolution[0] / 2, title_size[1] + 125))

        # puts elements in graphics to be rendered
        self.graphics[1] = [
            {"type": "surface", "surface": title, "dest": (resolution[0]//10, 20)},
            {"type": "rect", "rect": play_button, "colour": (234, 124, 176)},
            {"type": "surface", "surface": play_text, "dest": play_text_loc},
            {"type": "rect", "rect": options_button, "colour": (234, 124, 176)},
            {"type": "surface", "surface": options_text, "dest": options_text_loc}
        ]

    def display(self, events):
        # make a copy of graphics for editing
        graphics = self.graphics

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse = pygame.Rect(event.pos[0], event.pos[1], 1, 1)
        self.renderer.update(graphics)


class Options:
    def __init__(self, renderer):
        self.renderer = renderer
        self.log = logging.getLogger("main.menu.OptionMenu")
        self.log.setLevel(logging.INFO)
        self.graphics = [[
            {"type": "bg", "colour": (255, 5, 255)}
        ]]
        self.resolution_change()

    def resolution_change(self):
        # get the display size
        resolution = pygame.display.get_surface()
        resolution = (resolution.get_width(), resolution.get_height())
        self.log.debug("resolution: " + str(resolution))

    def display(self):
        pass
