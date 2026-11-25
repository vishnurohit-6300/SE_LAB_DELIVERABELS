import pygame


class Block:
    def __init__(self, x, y, width, height, color, speed=0,
                 is_debris=False, velocity_y=0, rotation=0, rotation_speed=0):
        self.x, self.y = float(x), float(y)
        self.width, self.height = float(width), float(height)
        self.color, self.speed = color, speed
        self.direction = 1
        self.is_debris = is_debris
        self.velocity_y = float(velocity_y)
        self.rotation = float(rotation)
        self.rotation_speed = float(rotation_speed)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), max(1, int(self.width)),
                           max(1, int(self.height)))

    def update(self, screen_width):
        if self.is_debris:
            self.velocity_y += 0.45
            self.y += self.velocity_y
            self.rotation += self.rotation_speed
            self.x += 0.5
        elif self.speed:
            self.x += self.speed * self.direction
            if self.x <= 20:
                self.x, self.direction = 20, 1
            elif self.x + self.width >= screen_width - 20:
                self.x = screen_width - 20 - self.width
                self.direction = -1

    def render(self, surface):
        if not self.is_debris:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
            pygame.draw.rect(surface, (245, 245, 250), self.rect,
                             width=2, border_radius=4)
            return
        image = pygame.Surface((max(1, int(self.width)), max(1, int(self.height))),
                               pygame.SRCALPHA)
        pygame.draw.rect(image, self.color, image.get_rect(), border_radius=4)
        pygame.draw.rect(image, (245, 245, 250), image.get_rect(), width=2,
                         border_radius=4)
        rotated = pygame.transform.rotate(image, self.rotation)
        surface.blit(rotated, rotated.get_rect(center=(
            int(self.x + self.width / 2), int(self.y + self.height / 2))))
