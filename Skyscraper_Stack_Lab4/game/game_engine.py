import random
import pygame
from game.block import Block


class GameEngine:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.block_height, self.base_width = 28, 180
        self.font_title = pygame.font.SysFont(None, 38)
        self.font_hud = pygame.font.SysFont(None, 28)
        self.font_big = pygame.font.SysFont(None, 46)
        self.font_perfect = pygame.font.SysFont(None, 42)
        self.reset()

    def get_color(self, index):
        palette = [(230, 75, 75), (240, 140, 45), (245, 210, 50),
                   (60, 195, 110), (50, 150, 240), (165, 80, 225)]
        return palette[index % len(palette)]

    def reset(self):
        self.score = 0
        self.game_over = False
        self.perfect_streak = self.perfect_popup_timer = 0
        self.debris = []
        self.stack = [Block((self.width - self.base_width) // 2,
                            self.height - 60, self.base_width,
                            self.block_height, self.get_color(0))]
        self.spawn_active_block()

    def spawn_active_block(self):
        top = self.stack[-1]
        speed = min(10.0, 4.5 + len(self.stack) * 0.35)
        start_x = 25 if random.choice([True, False]) else self.width - 25 - top.width
        self.active_block = Block(start_x, top.y - self.block_height - 4,
                                  top.width, self.block_height,
                                  self.get_color(len(self.stack)), speed=speed)

    def create_debris(self, x, y, width, color):
        if width > 0:
            self.debris.append(Block(x, y, width, self.block_height, color,
                                     is_debris=True, velocity_y=-2.0,
                                     rotation_speed=random.choice([-6, -4, 4, 6])))

    def drop_block(self):
        if self.game_over:
            return
        top, act = self.stack[-1], self.active_block
        left = max(act.x, top.x)
        right = min(act.x + act.width, top.x + top.width)
        overlap = right - left
        if overlap <= 0:
            self.game_over = True
            self.perfect_streak = 0
            return
        if abs(act.x - top.x) <= 3:
            new_block = Block(top.x, act.y, top.width, self.block_height, act.color)
            self.score += 3
            self.perfect_streak += 1
            self.perfect_popup_timer = 45
            if self.perfect_streak >= 3:
                expanded = min(self.base_width, new_block.width + 10)
                new_block.x = max(20, min(self.width - 20 - expanded,
                                  new_block.x - (expanded - new_block.width) / 2))
                new_block.width = expanded
                self.perfect_streak = 0
        else:
            self.perfect_streak = 0
            if act.x < left:
                self.create_debris(act.x, act.y, left - act.x, act.color)
            if act.x + act.width > right:
                self.create_debris(right, act.y, act.x + act.width - right, act.color)
            new_block = Block(left, act.y, overlap, self.block_height, act.color)
            self.score += 1
        self.stack.append(new_block)
        if new_block.y < 180:
            for block in self.stack + self.debris:
                block.y += self.block_height + 4
        self.spawn_active_block()

    def handle_event(self, event):
        click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        space = event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
        if self.game_over:
            if click or space or (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                self.reset()
        elif click or space:
            self.drop_block()

    def update(self):
        if not self.game_over:
            self.active_block.update(self.width)
        for debris in self.debris:
            debris.update(self.width)
        self.debris = [d for d in self.debris if d.y < self.height + 100]
        self.perfect_popup_timer = max(0, self.perfect_popup_timer - 1)

    def get_background_color(self):
        height = len(self.stack) - 1
        stages = [(0, (24, 27, 36)), (8, (45, 55, 100)), (16, (75, 55, 120)),
                  (25, (35, 25, 75)), (35, (8, 10, 25)), (50, (2, 4, 12))]
        for (low, a), (high, b) in zip(stages, stages[1:]):
            if height <= high:
                fraction = (height - low) / (high - low)
                return tuple(int(x + (y - x) * fraction) for x, y in zip(a, b))
        return stages[-1][1]

    def draw_label(self, screen, font, text, color, y):
        label = font.render(text, True, color)
        screen.blit(label, (self.width // 2 - label.get_width() // 2, y))

    def render(self, screen):
        background = self.get_background_color()
        for y in range(self.height):
            fraction = y / max(1, self.height - 1)
            color = tuple(int(c * (0.45 + 0.55 * fraction)) for c in background)
            pygame.draw.line(screen, color, (0, y), (self.width - 1, y))
        # Deterministic star positions avoid flickering as the tower climbs.
        height = len(self.stack) - 1
        if height >= 25:
            brightness = min(180, (height - 24) * 8)
            for i in range(35):
                x, y = (i * 137 + 17) % self.width, (i * 83 + 19) % self.height
                pygame.draw.circle(screen, (brightness,) * 3, (x, y), 1)
        self.draw_label(screen, self.font_title, 'Skyscraper Stack', (245, 245, 245), 16)
        self.draw_label(screen, self.font_hud, f'Height: {height} | Score: {self.score}',
                        (255, 220, 80), 54)
        for block in self.stack + self.debris:
            block.render(screen)
        if not self.game_over:
            self.active_block.render(screen)
        if self.perfect_popup_timer:
            self.draw_label(screen, self.font_perfect, 'PERFECT!', (255, 215, 0),
                            100 - (45 - self.perfect_popup_timer))
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 195))
            screen.blit(overlay, (0, 0))
            self.draw_label(screen, self.font_big, 'TOWER COLLAPSED!', (240, 75, 75),
                            self.height // 2 - 40)
            self.draw_label(screen, self.font_hud, f'Final Height: {height} | Score: {self.score}',
                            (255, 255, 255), self.height // 2 + 10)
            self.draw_label(screen, self.font_hud, 'Press [Space] or [R] to Play Again',
                            (200, 200, 200), self.height // 2 + 50)
