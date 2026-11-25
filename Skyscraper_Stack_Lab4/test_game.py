"""Run from personal repo root after applying the patch."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import pygame
from game.game_engine import GameEngine

pygame.init()
try:
    engine = GameEngine(480, 560)
    engine.active_block.x = engine.stack[-1].x + 20
    engine.drop_block()
    assert not engine.game_over and len(engine.stack) == 2
    assert engine.stack[-1].width == 160 and len(engine.debris) == 1
    debris = engine.debris[0]
    angle = debris.rotation
    for _ in range(20):
        engine.update()
    assert debris.rotation != angle
    initial = engine.stack[-1].width
    for _ in range(3):
        engine.active_block.x = engine.stack[-1].x
        engine.drop_block()
    assert engine.stack[-1].width > initial and engine.perfect_popup_timer > 0
    assert engine.score == 10
    engine.active_block.x = -1000
    engine.drop_block()
    assert engine.game_over
    engine.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    assert not engine.game_over and len(engine.stack) == 1
    color = engine.get_background_color()
    for _ in range(10):
        engine.active_block.x = engine.stack[-1].x
        engine.drop_block()
    assert engine.get_background_color() != color
    screen = pygame.Surface((480, 560))
    engine.render(screen)
    assert screen.get_at((0, 0)) != screen.get_at((0, 559))
    print('All checks passed: overlap, trim, debris, perfect combo, miss, restart, sky gradient.')
finally:
    pygame.quit()
