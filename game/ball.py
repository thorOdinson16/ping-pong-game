import pygame
import random
import os

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # ✅ Initialize sounds
        pygame.mixer.init()
        sound_path = os.path.join(os.path.dirname(__file__), "..", "sounds")
        self.paddle_sound = pygame.mixer.Sound(os.path.join(sound_path, "paddle_hit.wav"))
        self.wall_sound = pygame.mixer.Sound(os.path.join(sound_path, "wall_bounce.wav"))
        self.score_sound = pygame.mixer.Sound(os.path.join(sound_path, "score.wav"))

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            self.wall_sound.play()  # 🔊 Wall bounce sound

    def check_collision(self, player, ai):
        if self.rect().colliderect(player.rect()) or self.rect().colliderect(ai.rect()):
            self.velocity_x *= -1
            self.paddle_sound.play()  # 🔊 Paddle hit sound

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        self.score_sound.play()  # 🔊 Scoring sound

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)