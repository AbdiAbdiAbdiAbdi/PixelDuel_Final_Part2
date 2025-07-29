import pygame

class HitEffect:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 10
        self.max_radius = 50
        self.alpha = 255
        self.surface = pygame.Surface((self.max_radius*2, self.max_radius*2), pygame.SRCALPHA)

    def update(self):
        self.radius += 5
        self.alpha -= 30
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))  # Clear previous frame
        color_with_alpha = (*self.color, self.alpha)
        pygame.draw.circle(self.surface, color_with_alpha, (self.max_radius, self.max_radius), self.radius)
        screen.blit(self.surface, (self.x - self.max_radius, self.y - self.max_radius))

    def is_finished(self):
        return self.alpha == 0 or self.radius >= self.max_radius
