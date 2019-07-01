import pygame


class VirusGraphic:
    """ can create and return key Virus graphics"""
    def __init__(self, renderer):
        self.renderer = renderer

        self.name = ""
        self.resolution = pygame.display.Info()
        self.resolution = (self.resolution.current_w, self.resolution.current_h)
        self.impact, self.virulence, self.detectability = 0, 0, 0

        self.card = pygame.Surface((900, 300))

        self.update(self.resolution)

    def update_stats(self, name, impact, virulence, detectability):
        self.name = name
        self.impact = impact
        self.virulence = virulence
        self.detectability = detectability
        self.update(self.resolution)

    def update(self, resolution):
        """ updates graphical elements when resolution or virus stats change """
        self.resolution = resolution

        colours = {
            "outline": (200, 200, 200),
            "internal": (75, 75, 75),
            "text": (255, 255, 255),
            "impact": (255, 50, 50),
            "virulence": (50, 255, 50),
            "detectability": (50, 50, 255)
        }

        self.card.fill(colours["outline"])
        internal_bg = pygame.Rect(25, 25, 500, 250)

        name_text = self.renderer.fonts["main"].render(self.name, colours["text"], size=60)

        impact_icon = pygame.Rect(530, 25, 80, 80)
        virulence_icon = pygame.Rect(530, 110, 80, 80)
        detectability_icon = pygame.Rect(530, 195, 80, 80)

        impact_bar_bg = pygame.Rect(615, 25, 260, 80)
        virulence_bar_bg = pygame.Rect(615, 110, 260, 80)
        detectability_bar_bg = pygame.Rect(615, 195, 260, 80)

        impact_text = self.renderer.fonts["main"].render("I", colours["text"], size=80)
        virulence_text = self.renderer.fonts["main"].render("V", colours["text"], size=80)
        detectability_text = self.renderer.fonts["main"].render("D", colours["text"], size=80)

        impact_bar = pygame.Rect(615, 25, 260*self.impact//100, 80)
        virulence_bar = pygame.Rect(615, 110, 260*self.virulence//100, 80)
        detectability_bar = pygame.Rect(615, 195, 260*self.detectability//100, 80)

        pygame.draw.rect(self.card, colours["internal"], internal_bg)

        pygame.draw.rect(self.card, colours["internal"], impact_icon)
        pygame.draw.rect(self.card, colours["internal"], virulence_icon)
        pygame.draw.rect(self.card, colours["internal"], detectability_icon)

        pygame.draw.rect(self.card, colours["internal"], impact_bar_bg)
        pygame.draw.rect(self.card, colours["internal"], virulence_bar_bg)
        pygame.draw.rect(self.card, colours["internal"], detectability_bar_bg)

        self.card.blit(name_text[0], (40, 40))

        self.card.blit(impact_text[0], impact_text[0].get_rect(center=(570, 65)))
        self.card.blit(virulence_text[0], virulence_text[0].get_rect(center=(570, 150)))
        self.card.blit(detectability_text[0], detectability_text[0].get_rect(center=(570, 235)))

        pygame.draw.rect(self.card, colours["impact"], impact_bar)
        pygame.draw.rect(self.card, colours["virulence"], virulence_bar)
        pygame.draw.rect(self.card, colours["detectability"], detectability_bar)


class Virus:
    """ Main Virus class """
    def __init__(self, renderer):
        self.blocks = []
        self.impact, self.virulence, self.detectability = 0, 0, 0
        self.graphic = VirusGraphic(renderer)
        self.name = ""

    def update_stats(self):
        """ updates a virus's key stats to current block values"""
        # reset values
        self.impact, self.virulence, self.detectability = 0, 0, 0

        # read each block and add respective values
        for block in self.blocks:
            self.impact += block.impact
            self.virulence += block.virulence
            self.detectability += block.detectability

        self.graphic.update_stats(self.name, self.impact, self.virulence, self.detectability)

    def valid(self):
        """ checks whether the virus is valid or not """
        if len(self.blocks) > 0:
            return True
        else:
            return False

    def add_block(self, block):
        """ adds a block to the virus"""
        self.blocks.append(block)
        self.update_stats()

    def remove_block(self, block):
        """ removes a block from a virus"""
        self.blocks.remove(block)
        self.update_stats()

    def update_name(self, name):
        if len(name) > 15:
            self.name = name[:15]
        else:
            self.name = name
        self.update_stats()
